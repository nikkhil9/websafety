"""
WebSafety Multilingual Text Classifier - Kaggle Training Script
Fine-tunes XLM-RoBERTa on 9K multilingual dataset

This script is designed to run on Kaggle with GPU acceleration.
"""

import json
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from transformers import (
    XLMRobertaTokenizer, 
    XLMRobertaForSequenceClassification,
    Trainer, 
    TrainingArguments,
    EarlyStoppingCallback
)
from datasets import Dataset
import matplotlib.pyplot as plt
import seaborn as sns

# Label mapping
LABEL_MAP = {
    "safe": 0,
    "phishing": 1,
    "malware": 2,
    "hate_speech": 3,
    "cyberbullying": 4,
    "sexual_content": 5,
    "violence": 6
}

ID_TO_LABEL = {v: k for k, v in LABEL_MAP.items()}

class WebSafetyDataset:
    def __init__(self, tokenizer, max_length=256):
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def load_jsonl(self, file_path):
        """Load JSONL file"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
        return data
    
    def prepare_dataset(self, file_path):
        """Prepare dataset for training"""
        print(f"📂 Loading {file_path}...")
        raw_data = self.load_jsonl(file_path)
        
        # Convert to format for transformers
        texts = [item['text'] for item in raw_data]
        labels = [LABEL_MAP[item['primary_label']] for item in raw_data]
        languages = [item['language'] for item in raw_data]
        
        # Create HuggingFace Dataset
        dataset = Dataset.from_dict({
            'text': texts,
            'label': labels,
            'language': languages
        })
        
        # Tokenize
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                padding='max_length',
                truncation=True,
                max_length=self.max_length
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        print(f"   ✅ Loaded {len(tokenized_dataset)} samples")
        
        return tokenized_dataset

def compute_metrics(eval_pred):
    """Compute metrics for evaluation"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    # F1 scores
    f1_macro = f1_score(labels, predictions, average='macro')
    f1_weighted = f1_score(labels, predictions, average='weighted')
    
    # Accuracy
    accuracy = (predictions == labels).mean()
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted
    }

def plot_confusion_matrix(trainer, test_dataset, output_path):
    """Plot confusion matrix"""
    predictions = trainer.predict(test_dataset)
    y_pred = np.argmax(predictions.predictions, axis=1)
    y_true = predictions.label_ids
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=list(LABEL_MAP.keys()),
        yticklabels=list(LABEL_MAP.keys())
    )
    plt.title('Confusion Matrix - WebSafety Classifier')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"📊 Confusion matrix saved to {output_path}")

def train_model(
    train_file,
    val_file,
    test_file,
    output_dir='./websafety-model',
    model_name='xlm-roberta-base',
    epochs=4,
    batch_size=16,
    learning_rate=2e-5
):
    """Main training function"""
    
    print("🚀 Starting WebSafety Model Training")
    print(f"Model: {model_name}")
    print(f"Epochs: {epochs}, Batch Size: {batch_size}, LR: {learning_rate}\n")
    
    # Check GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"💻 Using device: {device}")
    if device == 'cuda':
        print(f"   GPU: {torch.cuda.get_device_name(0)}\n")
    
    # Load tokenizer
    print("📥 Loading tokenizer...")
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
    
    # Prepare datasets
    dataset_loader = WebSafetyDataset(tokenizer)
    train_dataset = dataset_loader.prepare_dataset(train_file)
    val_dataset = dataset_loader.prepare_dataset(val_file)
    test_dataset = dataset_loader.prepare_dataset(test_file)
    
    # Load model
    print(f"\n🤖 Loading model: {model_name}...")
    model = XLMRobertaForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(LABEL_MAP),
        problem_type="single_label_classification"
    )
    model.to(device)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        warmup_steps=500,
        logging_dir=f'{output_dir}/logs',
        logging_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model='f1_macro',
        greater_is_better=True,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),  # Mixed precision if GPU available
        report_to='none'  # Disable wandb/tensorboard
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    # Train
    print("\n🏋️ Training started...\n")
    trainer.train()
    
    # Evaluate on test set
    print("\n📊 Evaluating on test set...")
    test_results = trainer.evaluate(test_dataset)
    print("\nTest Results:")
    for key, value in test_results.items():
        print(f"  {key}: {value:.4f}")
    
    # Detailed classification report
    predictions = trainer.predict(test_dataset)
    y_pred = np.argmax(predictions.predictions, axis=1)
    y_true = predictions.label_ids
    
    print("\n📋 Classification Report:")
    print(classification_report(
        y_true, 
        y_pred, 
        target_names=list(LABEL_MAP.keys()),
        digits=4
    ))
    
    # Plot confusion matrix
    plot_confusion_matrix(trainer, test_dataset, f'{output_dir}/confusion_matrix.png')
    
    # Save model
    print(f"\n💾 Saving model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save label mapping
    with open(f'{output_dir}/label_mapping.json', 'w') as f:
        json.dump(LABEL_MAP, f, indent=2)
    
    print("\n✅ Training complete!")
    print(f"📁 Model saved to: {output_dir}")
    
    return trainer, test_results

if __name__ == "__main__":
    # Kaggle paths (adjust if needed)
    TRAIN_FILE = "/kaggle/input/websafety-9k/train_9k.jsonl"
    VAL_FILE = "/kaggle/input/websafety-9k/validation_9k.jsonl"
    TEST_FILE = "/kaggle/input/websafety-9k/test_9k.jsonl"
    OUTPUT_DIR = "/kaggle/working/websafety-xlm-roberta"
    
    # Train
    trainer, results = train_model(
        train_file=TRAIN_FILE,
        val_file=VAL_FILE,
        test_file=TEST_FILE,
        output_dir=OUTPUT_DIR,
        model_name='xlm-roberta-base',
        epochs=4,
        batch_size=16,
        learning_rate=2e-5
    )
    
    print("\n🎉 All done! Model ready for deployment.")

"""
Training Script for Custom WebSafety Dataset

Fine-tunes transformer models on the custom dataset.

Usage:
    python -m dataset.training.train_custom \
        --train dataset/processed/train.jsonl \
        --val dataset/processed/validation.jsonl \
        --model distilbert-base-uncased \
        --output models/websafety-custom/
"""

import json
import os
import argparse
from typing import List, Dict
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import numpy as np


class WebSafetyDataset(Dataset):
    """PyTorch Dataset for WebSafety data"""
    
    def __init__(self, filepath: str, tokenizer, max_length=512):
        self.samples = []
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Load samples
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                self.samples.append(json.loads(line))
        
        # Create label mapping
        self.label2id = {
            'safe': 0,
            'phishing': 1,
            'malware': 2,
            'hate_speech': 3,
            'cyberbullying': 4,
            'sexual_content': 5,
            'violence': 6
        }
        self.id2label = {v: k for k, v in self.label2id.items()}
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        text = sample['text']
        label = self.label2id[sample['primary_label']]
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def compute_metrics(pred):
    """Compute metrics for evaluation"""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='weighted', zero_division=0
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def train_model(
    train_file: str,
    val_file: str,
    model_name: str,
    output_dir: str,
    epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5
):
    """Train the model"""
    
    print("="*70)
    print("WebSafety Custom Model Training")
    print("="*70)
    print(f"\nModel: {model_name}")
    print(f"Train data: {train_file}")
    print(f"Val data: {val_file}")
    print(f"Output: {output_dir}")
    print(f"Epochs: {epochs}, Batch size: {batch_size}, LR: {learning_rate}")
    
    # Load tokenizer and model
    print("\nLoading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=7,  # 7 primary categories
        problem_type="single_label_classification"
    )
    
    # Create datasets
    print("Loading datasets...")
    train_dataset = WebSafetyDataset(train_file, tokenizer)
    val_dataset = WebSafetyDataset(val_file, tokenizer)
    
    print(f"✓ Train samples: {len(train_dataset)}")
    print(f"✓ Val samples: {len(val_dataset)}")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{output_dir}/logs',
        logging_steps=100,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",  # Disable wandb/tensorboard for simplicity
    )
    
    # Create Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    # Train
    print("\nStarting training...")
    print("="*70)
    trainer.train()
    
    # Save
    print("\nSaving model...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save label mapping
    label_mapping = {
        'label2id': train_dataset.label2id,
        'id2label': train_dataset.id2label
    }
    with open(os.path.join(output_dir, 'label_mapping.json'), 'w') as f:
        json.dump(label_mapping, f, indent=2)
    
    print(f"✓ Model saved to {output_dir}")
    
    # Final evaluation
    print("\nFinal evaluation on validation set:")
    results = trainer.evaluate()
    print("="*70)
    for key, value in results.items():
        print(f"{key}: {value:.4f}")
    print("="*70)
    
    return trainer


def main():
    parser = argparse.ArgumentParser(
        description='Train custom model on WebSafety Dataset'
    )
    parser.add_argument(
        '--train',
        type=str,
        required=True,
        help='Training data file (JSONL)'
    )
    parser.add_argument(
        '--val',
        type=str,
        required=True,
        help='Validation data file (JSONL)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='distilbert-base-uncased',
        help='Pretrained model name (default: distilbert-base-uncased)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='models/websafety-custom',
        help='Output directory for trained model'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=3,
        help='Number of training epochs'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=16,
        help='Batch size'
    )
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=2e-5,
        help='Learning rate'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate data loading without training'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE - Validating data loading...")
        tokenizer = AutoTokenizer.from_pretrained(args.model)
        train_dataset = WebSafetyDataset(args.train, tokenizer)
        val_dataset = WebSafetyDataset(args.val, tokenizer)
        print(f"✓ Successfully loaded {len(train_dataset)} train and {len(val_dataset)} val samples")
        print("✓ Data validation complete!")
        return
    
    # Train
    train_model(
        args.train,
        args.val,
        args.model,
        args.output,
        args.epochs,
        args.batch_size,
        args.learning_rate
    )


if __name__ == '__main__':
    main()

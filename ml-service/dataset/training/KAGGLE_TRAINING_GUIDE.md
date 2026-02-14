# WebSafety Model Training on Kaggle - Complete Guide

## 📋 Prerequisites

1. Kaggle account (free)
2. Our 9K multilingual dataset
3. Kaggle notebook with GPU enabled

## 🚀 Step-by-Step Instructions

### Step 1: Upload Dataset to Kaggle

1. **Prepare dataset files**:
   - Navigate to: `ml-service/dataset/processed/`
   - You need these 3 files:
     - `train_9k.jsonl` (6,294 samples)
     - `validation_9k.jsonl` (1,347 samples)
     - `test_9k.jsonl` (1,359 samples)

2. **Create Kaggle Dataset**:
   - Go to [kaggle.com/datasets](https://www.kaggle.com/datasets)
   - Click "New Dataset"
   - Upload all 3 .jsonl files
   - Title: `WebSafety 9K Multilingual Dataset`
   - Description: `Multilingual web safety classification dataset with 9K samples across English, Hinglish, and Telenglish`
   - Click "Create"

3. **Note your dataset path**: It will be something like:
   ```
   /kaggle/input/websafety-9k/train_9k.jsonl
   ```

### Step 2: Create Kaggle Notebook

1. Go to [kaggle.com/code](https://www.kaggle.com/code)
2. Click "New Notebook"
3. **Important**: Enable GPU
   - Click "Settings" (right sidebar)
   - Accelerator → Select **GPU T4 x2** (free tier)
   - Internet → **ON** (to download models)
   - Click "Save"

### Step 3: Install Dependencies

In the first cell of your notebook:

```python
# Install required packages
!pip install -q transformers datasets sentencepiece
```

### Step 4: Copy Training Code

Create a new cell and paste the entire content from `train_kaggle.py`

### Step 5: Update File Paths

Make sure the paths match your dataset:

```python
TRAIN_FILE = "/kaggle/input/websafety-9k/train_9k.jsonl"
VAL_FILE = "/kaggle/input/websafety-9k/validation_9k.jsonl"
TEST_FILE = "/kaggle/input/websafety-9k/test_9k.jsonl"
```

### Step 6: Run Training

Click "Run All" or run cells sequentially.

**Expected Runtime**: ~30-45 minutes with GPU

### Step 7: Download Trained Model

After training completes:

1. Check the output folder: `/kaggle/working/websafety-xlm-roberta/`
2. Download the following files:
   - `pytorch_model.bin` (model weights)
   - `config.json` (model config)
   - `tokenizer_config.json` (tokenizer config)
   - `sentencepiece.bpe.model` (tokenizer model)
   - `label_mapping.json` (label mapping)
   - `confusion_matrix.png` (performance visualization)

## 📊 Expected Results

### Target Metrics
- **Accuracy**: >85%
- **F1 Score (Macro)**: >0.85
- **F1 Score (Weighted)**: >0.87

### Per-Language Performance
- English: >90% F1
- Hinglish: >78% F1
- Telenglish: >78% F1

## 🔍 Troubleshooting

### Out of Memory Error
- Reduce `batch_size` from 16 to 8
- Reduce `max_length` from 256 to 128

### Slow Training
- Ensure GPU is enabled (check "Accelerator" in settings)
- Verify with: `!nvidia-smi` in a cell

### Import Errors
- Re-run pip install cell
- Restart kernel and run again

## 📥 Alternative: Notebook Template

I've also created a ready-to-use Kaggle notebook template at:
```
training/kaggle_training_notebook.ipynb
```

You can upload this directly to Kaggle!

## 🎯 Next Steps After Training

1. **Evaluate Performance**: Review classification report and confusion matrix
2. **Download Model**: Save all model files locally
3. **Update ml-service**: Replace existing text classifier with new model
4. **Test API**: Run comprehensive tests
5. **Deploy**: Push to production

## 💡 Tips

- **Monitor Training**: Watch the validation loss - should decrease steadily
- **Early Stopping**: Training stops automatically if validation doesn't improve for 2 epochs
- **Save Outputs**: Download confusion matrix and logs for your research paper
- **Experiment**: Try different learning rates (1e-5 to 5e-5)

## 📝 Dataset Citation

```bibtex
@dataset{websafety9k2026,
  title={WebSafety 9K: Multilingual Web Safety Classification Dataset},
  author={Your Name},
  year={2026},
  publisher={Kaggle},
  version={1.0}
}
```

---

**Questions?** Check the training logs in `/kaggle/working/websafety-xlm-roberta/logs/`

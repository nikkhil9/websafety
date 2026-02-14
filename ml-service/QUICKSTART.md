# Quick Start Guide - ML Service

## 🚀 Get Your ML Service Running in 5 Minutes!

### Step 1: Open Terminal in ml-service folder

```bash
cd "C:\Users\Nikhil Adapureddy\OneDrive\Desktop\WebSafety\ml-service"
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

⏰ **This will take 5-10 minutes** - It's downloading ML models from the internet (~500MB-1GB)

**Don't panic if you see warnings!** As long as it doesn't error out, you're fine.

### Step 5: Create .env file

```bash
copy .env.example .env
```

### Step 6: Run the Server!

```bash
python app.py
```

You should see:
```
==================================================
🛡️  Web Safety ML Service
==================================================
Server running on: http://localhost:5001
Debug mode: True
==================================================
```

### Step 7: Test It! (Open a NEW terminal)

In a **new terminal window** (keep the server running):

```bash
cd "C:\Users\Nikhil Adapureddy\OneDrive\Desktop\WebSafety\ml-service"
venv\Scripts\activate
python test_api.py
```

You should see test results! 🎉

---

## ⚠️ Common Issues

### "python is not recognized"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

### "pip install" is very slow
- Be patient! First time downloads large ML models
- Need stable internet connection

### Port 5001 already in use
- Edit `.env` file and change PORT to 5002

### ModuleNotFoundError
- Make sure virtual environment is activated (you should see `(venv)`)
- Run `pip install -r requirements.txt` again

---

## 🎯 What You Just Built

You now have a working ML service that can:
- ✅ Detect toxic text
- ✅ Analyze URLs for malicious content
- ✅ (Placeholder) Detect unsafe images

This is the **brain** of your Web Safety project! 🧠

---

## 📝 Next Steps

1. Keep the ML service running
2. Build the backend API (Week 3-5)
3. Connect backend to this ML service
4. Build frontend to display results
5. Create browser extension

You're making great progress! 🚀

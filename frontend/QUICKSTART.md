# 🚀 Quick Start - Frontend

## Run the Web Application

### Step 1: Make Sure ML Service is Running

In the ml-service terminal (should already be running):
```powershell
# If not running:
cd "C:\Users\Nikhil Adapureddy\OneDrive\Desktop\WebSafety\ml-service"
venv\Scripts\activate
python app.py
```

You should see: `Server running on: http://localhost:5001`

### Step 2: Start the Frontend

Open a NEW PowerShell terminal:

```powershell
cd "C:\Users\Nikhil Adapureddy\OneDrive\Desktop\WebSafety\frontend"
npm run dev
```

The app will start on `http://localhost:3000`

### Step 3: Open in Browser

Your browser should automatically open, or navigate to:
```
http://localhost:3000
```

---

## What You'll See

### Beautiful Dark Theme Interface
- Gradient logo and headers
- Animated components
- Responsive design

### Two Main Features:

**1. Text Analysis Tab**
- Enter any text
- Click "Analyze Text"
- See AI-powered threat detection
- View category breakdown (toxic, hate, threat, etc.)

**2. URL Scanner Tab**
- Enter any URL
- Click "Scan URL"  
- See security assessment
- View domain information and threat categories

### Real-Time Stats
- Total scans counter
- Safe content detected
- Threats found

---

## Try These Examples:

### Text Analysis
```
Safe: "Hello! Have a great day!"
Toxic: "I hate you stupid idiot"
Threat: "I will hurt you"
```

### URL Scanner
```
Safe: https://google.com
Suspicious: http://phishing-login.tk
Malicious: http://192.168.1.1/admin.php
```

---

## Troubleshooting

### "Error analyzing" message
- Make sure ML service is running on port 5001
- Check the ml-service terminal for errors

### Blank white page
- Open browser DevTools (F12)
- Check Console for errors
- Make sure `npm install` completed successfully

### Port 3000 already in use
- Stop other apps using port 3000
- Or change port in `vite.config.js`

---

## 🎉 You're Done!

You now have a **complete, working AI-powered web application**!

**What you've built:**
- ✅ ML Service (Text + URL analysis)
- ✅ Beautiful React Frontend
- ✅ Real-time demonstration platform

**Total project completion: ~60%!** 🚀

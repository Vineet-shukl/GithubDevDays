# 🚀 Quick Start Guide - Phishing Email Classifier

## ⚡ 5-Minute Setup

### Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and paste your API key
# GEMINI_API_KEY=your_actual_key_here
```

### Step 4: Run the App

**Option A: Streamlit Dashboard (Recommended for beginners)**
```bash
streamlit run ui.py
```
Then open `http://localhost:8501` in your browser

**Option B: FastAPI Backend (For developers)**
```bash
uvicorn main:app --reload
```
Then visit `http://localhost:8000/docs` for API documentation

**Option C: Jupyter Notebook (For learning)**
```bash
jupyter notebook PhishingEmailClassifier.ipynb
```

## 🎯 What to Try First

### 1. In Streamlit Dashboard:
- Click any of the "Quick Load Examples" buttons
- Click "🔍 Analyze Email"
- See the threat analysis with severity badges!

### 2. In API:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "raw_email": "From: security@paypa1-alerts.com\nSubject: URGENT: Your account has been limited!\n\nYour PayPal account access is limited. Verify immediately..."
  }'
```

### 3. In Jupyter Notebook:
- Run cells sequentially from top to bottom
- Follow the step-by-step tutorial
- Learn how it works under the hood!

## 🎓 Learning Path

### Beginner → Intermediate → Advanced

1. **Start Here**: Run Streamlit UI and test with sample emails
2. **Next**: Open Jupyter notebook and follow Part 1 (From Scratch)
3. **Then**: Explore Parts 2-3 (Pydantic AI + Tools)
4. **Advanced**: Try the FastAPI backend and integrate with your apps

## 🐛 Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"GEMINI_API_KEY not set"**
```bash
# Check your .env file
cat .env
# Make sure it has: GEMINI_API_KEY=your_key_here
```

**"Port already in use"**
```bash
# For Streamlit, use a different port:
streamlit run ui.py --server.port 8502

# For FastAPI:
uvicorn main:app --port 8001
```

## 📚 Next Steps

- **Customize**: Edit `agent.py` to add more detection rules
- **Extend**: Add new tools in `agent.py` (WHOIS lookup, SSL check)
- **Deploy**: Use Railway, Render, or Vercel for hosting
- **Integrate**: Call the API from your email client or security tools

## 💡 Pro Tips

1. **Start with the notebook** - Best way to understand how it works
2. **Test all 5 samples** - See different attack types detected
3. **Try your own emails** - Paste real emails (remove sensitive data!)
4. **Read the tools** - Check `agent.py` to see domain checking logic
5. **Customize the UI** - Edit `ui.py` for your branding

## 🎉 You're Ready!

Now you have a working AI-powered phishing detector. Happy detecting! 🛡️

Need help? Open an issue on GitHub or check the full README.md

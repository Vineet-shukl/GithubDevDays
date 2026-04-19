# 🛡️ PhishGuard — AI Phishing Email Classifier

> An AI-powered phishing email classifier built with **Pydantic AI** + **Groq (LLaMA 3.3 70B)**. Paste any email → get an instant threat report with severity, confidence score, red flags, and recommended action.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pydantic AI](https://img.shields.io/badge/Pydantic_AI-Agent_Framework-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?logo=groq)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-teal?logo=fastapi)

---

## 🎯 What Does It Do?

PhishGuard takes a **raw email** as input and uses an **AI agent** to determine:

| Output Field | Description |
|---|---|
| **Is Phishing?** | `true` / `false` classification |
| **Confidence Score** | 0.0 – 1.0 (how sure the AI is) |
| **Severity** | `low` · `medium` · `high` · `critical` |
| **Attack Type** | credential harvesting, malware link, BEC, fake invoice, or none |
| **Red Flags** | List of specific suspicious patterns found |
| **Spoofed Brand** | Which brand is being impersonated (if any) |
| **Recommended Action** | What the user should do |
| **Explanation** | Detailed reasoning from the AI |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | [Groq](https://groq.com/) (LLaMA 3.3 70B) | Fast AI inference (free API key) |
| **Agent Framework** | [Pydantic AI](https://ai.pydantic.dev/) | Structured output + tool calling |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Type-safe models & schemas |
| **Dashboard** | [Streamlit](https://streamlit.io/) | Interactive web UI |
| **REST API** | [FastAPI](https://fastapi.tiangolo.com/) | Backend API endpoints |

---

## ⚡ Quick Start (3 Steps)

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/PhishGuard.git
cd PhishGuard
pip install -r requirements.txt
```

### 2. Get Your Free Groq API Key

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Create a free account
3. Generate an API key
4. Create a `.env` file:

```bash
cp .env.example .env
```

Then paste your key inside `.env`:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 3. Run the App

**Option A: Streamlit Dashboard (Recommended)**
```bash
streamlit run ui.py
```
Opens at → `http://localhost:8501`

**Option B: FastAPI Backend**
```bash
uvicorn main:app --reload
```
Opens at → `http://localhost:8000` (Docs: `http://localhost:8000/docs`)

---

## 📁 Project Structure

```
PhishGuard/
├── agent.py           # AI agent with Groq + phishing detection tools
├── models.py          # Pydantic models (EmailInput, ThreatReport)
├── samples.py         # 5 sample phishing emails for testing
├── ui.py              # Streamlit dashboard (frontend)
├── main.py            # FastAPI server (REST API)
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── README.md          # This file
```

---

## 🧠 How It Works

```
┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│  User pastes │────▶│  Pydantic AI   │────▶│  Groq LLaMA  │
│  raw email   │     │  Agent         │     │  3.3 70B     │
└──────────────┘     │                │     └──────┬───────┘
                     │  Tools:        │            │
                     │  • extract_urls│◀───────────┘
                     │  • check_domain│     Structured
                     │  • header_check│     JSON output
                     └───────┬────────┘
                             │
                     ┌───────▼────────┐
                     │ ThreatReport   │
                     │ (Pydantic)     │
                     │ • is_phishing  │
                     │ • severity     │
                     │ • red_flags    │
                     │ • confidence   │
                     └────────────────┘
```

1. **User** pastes an email into the Streamlit UI (or sends via API)
2. **Pydantic AI Agent** receives the email and calls its tools:
   - `extract_urls()` — finds all URLs in the email body
   - `check_domain_suspicion()` — detects typosquatting (e.g. `paypa1.com`)
   - `analyze_header_mismatch()` — checks From vs Reply-To domains
3. **Groq LLM** analyzes everything and returns a structured `ThreatReport`
4. **Pydantic** validates the output automatically (type-safe, guaranteed schema)
5. **Result** is displayed with severity badges, confidence bar, and red flags

---

## 📊 Severity Levels

| Level | Emoji | Meaning | Example |
|---|---|---|---|
| **Critical** | 🔴 | Spoofed brand + credential harvesting | Fake PayPal login page |
| **High** | 🟠 | Malware link or BEC attempt | CEO fraud wire transfer |
| **Medium** | 🟡 | Suspicious but unclear intent | Vague urgency, odd domain |
| **Low** | 🟢 | Mild spam, unlikely phishing | Marketing email with typos |

---

## 🔌 API Usage

### Analyze an Email (POST)

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "raw_email": "From: security@paypa1-alerts.com\nSubject: URGENT...\n\nVerify at http://paypa1-alerts.com/verify"
  }'
```

### Response

```json
{
  "report": {
    "is_phishing": true,
    "confidence_score": 0.92,
    "attack_type": "credential_harvesting",
    "severity": "critical",
    "red_flags": [
      "Typosquatting domain: paypa1-alerts.com",
      "Urgency language: URGENT",
      "Suspicious URL pattern"
    ],
    "spoofed_brand": "PayPal",
    "recommended_action": "Delete immediately and report to IT",
    "explanation": "Classic credential harvesting attempt..."
  },
  "analyzed_at": "2024-01-15T10:30:00",
  "model_used": "groq:llama-3.3-70b-versatile"
}
```

---

## 🧪 Built-in Test Samples

The app comes with 5 pre-loaded emails you can test instantly:

| # | Sample | Type |
|---|---|---|
| 1 | PayPal Spoofing | Credential Harvesting |
| 2 | CEO Wire Transfer | Business Email Compromise |
| 3 | Google Security Alert | Domain Spoofing |
| 4 | Microsoft Invoice | Fake Invoice Scam |
| 5 | GitHub Newsletter | Legitimate (control test) |

---

## 🤝 Contributing

PRs welcome! Fork → Branch → Commit → PR.

## 📝 License

MIT License

---

> **⚠️ Disclaimer:** This tool is for educational purposes. It should not be the sole method of email security. Always follow your organization's security policies.

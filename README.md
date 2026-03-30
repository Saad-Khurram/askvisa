# AskVisa 🇩🇪

A plain-English chatbot for international students navigating German student visas and bureaucracy.

Built with Python, Claude API, and Streamlit. Part of the [GermGuide AI](https://germguide.ai) portfolio.

> *"I'm an international student in Germany. I built this because I needed it myself."*

---

## Live Demo

🔗 **[Live demo link — add after deploying to Streamlit Cloud]**

---

## What It Does

Ask any German student visa question in plain English:

- *"Can I work more than 20 hours a week?"*
- *"What documents do I need to extend my residence permit?"*
- *"What is the Rundfunkbeitrag and do I have to pay it?"*
- *"How do I register my address in Germany?"*

The assistant answers based on a knowledge-rich system prompt covering visa types, work rights, Ausländerbehörde processes, blocked accounts, health insurance, and more.

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.10+ |
| UI | Streamlit |
| AI | Claude API (Anthropic) |
| Deployment | Streamlit Community Cloud |

---

## Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/askvisa.git
cd askvisa
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
# Get one at https://console.anthropic.com
```

**4. Run the app**
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. In **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "your_key_here"
   ```
4. Click **Deploy** — your live URL is ready in ~2 minutes

---

## Project Context

This is Week 1-2 of the GermGuide AI portfolio — a suite of AI tools helping international students navigate Germany:

| Project | What It Does | Status |
|---------|-------------|--------|
| **AskVisa** | Visa Q&A chatbot | ✅ Live |
| DecipherDE | Upload German letter → plain English | Planned |
| GermBridge | Write formal German emails | Planned |

---

## License

MIT

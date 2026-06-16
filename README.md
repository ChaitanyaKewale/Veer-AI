# ⚔️ VeerAI — Your Personal Defence Mentor

**AI-powered Defence Preparation Chatbot** for NDA, CDS, AFCAT, Agniveer, TES, SSB, Indian Army, Navy & Air Force aspirants.

---
Developer: Chaitanya Kewale INTERN ID - CITS1513

## 🚀 HOW TO RUN (Step-by-Step)

### Prerequisites
- Python 3.8 – 3.10 installed (Python 3.11+ may have ChatterBot issues)
- VS Code installed
- Internet connection (for first-time pip install)

---

### Step 1 — Open in VS Code
1. Extract the ZIP file
2. Open VS Code → **File → Open Folder** → Select the `VeerAI` folder

---

### Step 2 — Create Virtual Environment
Open the **VS Code Terminal** (`Ctrl + \``) and run:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

---

### Step 3 — Run Setup (Installs all dependencies + initialises DB)

```bash
python setup.py
```

This will:
- Install Flask, SQLAlchemy, and other packages
- Attempt to install ChatterBot (optional — app works without it)
- Create and seed the SQLite database with current affairs data

---

### Step 4 — Start the App

```bash
python app.py
```

You should see:
```
🎖️  Starting VeerAI - Defence Aspirant Chatbot
🌐 Open your browser at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

---

### Step 5 — Open in Browser
Go to: **http://localhost:5000**

---

## 📁 Project Structure

```
VeerAI/
├── app.py                  ← Flask backend (main entry point)
├── setup.py                ← One-time setup script
├── requirements.txt        ← Package list
├── modules/
│   ├── chatbot.py          ← ChatterBot engine + defence KB
│   ├── database.py         ← SQLite database layer
│   └── quiz.py             ← Quiz, WAT, SRT, TAT, OLQ, BMI logic
├── templates/
│   ├── base.html           ← Base layout with navbar
│   ├── index.html          ← Homepage
│   ├── chat.html           ← AI Chat interface
│   ├── ssb.html            ← SSB Interview Simulator
│   ├── quiz.html           ← Daily Quiz
│   ├── olq.html            ← OLQ Analyzer
│   ├── psychology.html     ← WAT / SRT / TAT Practice
│   ├── fitness.html        ← BMI + Fitness Guide
│   ├── current_affairs.html← Defence News
│   └── career.html         ← Career Navigator + Study Planner
├── static/
│   ├── css/style.css       ← Military-themed CSS
│   └── js/main.js          ← Frontend JavaScript
├── data/
│   └── defence_training.yml← ChatterBot training data
└── database/
    └── veerai.db           ← SQLite database (auto-created)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **AI Chat** | ChatterBot-powered defence Q&A on NDA, CDS, AFCAT, SSB, military tech |
| 🎖️ **SSB Simulator** | Personal, Defence, Current Affairs & Situational questions with feedback |
| 📋 **Daily Quiz** | 5-category quiz (NDA, CDS, SSB, Defence GK, Current Affairs) with scoring |
| 🧠 **OLQ Analyzer** | 8-question assessment across 7 Officer Like Qualities with report |
| 🔬 **Psychology Tests** | WAT (word timer), SRT (situation timer), TAT (4-min story) with feedback |
| 💪 **Fitness Guide** | BMI calculator, fitness standards table, 12-week training plan |
| 📰 **Current Affairs** | 10+ defence news items with category filter (Operations, Exercises, etc.) |
| 🗺️ **Career Navigator** | Army/Navy/Air Force entry routes, rank progressions, eligibility |
| 📅 **Study Planner** | Personalized weekly/daily plan for NDA/CDS/AFCAT |

---

## 🔧 Troubleshooting

**ChatterBot install fails:**
No problem! The app uses its own built-in defence knowledge base as fallback. All features work normally.

**Port 5000 already in use:**
```bash
# Change port in app.py last line:
app.run(debug=True, host='0.0.0.0', port=5001)
# Then visit http://localhost:5001
```

**"Module not found" error:**
Make sure your virtual environment is activated (`venv\Scripts\activate` on Windows).

**Database errors:**
Delete `database/veerai.db` and run `python setup.py` again.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask 2.3
- **Chatbot Engine:** ChatterBot 1.0.4 (with built-in KB fallback)
- **Database:** SQLite via SQLAlchemy
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Fonts:** Rajdhani + Exo 2 (Google Fonts)
- **Theme:** Military Olive Green / Army Dark / Gold

---

## 🎖️ Jai Hind! 🇮🇳
*"The Nation comes first, always and every time." — Field Marshal Sam Manekshaw*

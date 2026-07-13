<div align="center">

<!-- Animated Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a6b4a,100:00c896&height=200&section=header&text=TalentSync%20%E2%80%94%20HireAI&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20Resume%20Screening%20%26%20Smart%20Hiring%20Platform&descAlignY=58&descSize=18&animation=fadeIn"/>

<!-- Typing animation -->
<a href="https://github.com/hetvi-prajapati/HireAI_Website">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00C896&center=true&vCenter=true&width=600&lines=AI+Resume+Screening+System;Smart+ATS+Scoring+Engine;Real-time+Candidate+Matching;Built+with+Flask+%2B+spaCy+%2B+ML" alt="Typing SVG" />
</a>

<br/><br/>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HTML5](https://img.shields.io/badge/HTML5-45.8%25-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-17.4%25-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![CSS3](https://img.shields.io/badge/CSS3-12.8%25-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/hetvi-prajapati/HireAI_Website?style=flat-square&color=gold)](https://github.com/hetvi-prajapati/HireAI_Website/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/hetvi-prajapati/HireAI_Website?style=flat-square&color=blue)](https://github.com/hetvi-prajapati/HireAI_Website/network)
![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-ff69b4?style=flat-square)

</div>

---

## 🧠 What is TalentSync?

> **TalentSync** is a full-stack AI-powered hiring platform that automates resume screening, scores candidates using ATS algorithms, extracts skills via NLP (spaCy), and matches candidates to job descriptions using TF-IDF and ML models — all wrapped in a beautiful, responsive single-page web app.

No more manual resume filtering. No more guesswork. **Let AI do the heavy lifting.**

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🤖 AI Resume Screening
- **spaCy NER** model extracts real skills from uploaded resumes (PDF / DOCX)
- Context-aware extraction — filters noise and irrelevant tokens
- Supports 500+ technical and soft skills

### 📊 ATS Scoring Engine
- Scores every resume **out of 100**
- Matches candidate skills vs. job requirements
- Instant feedback with grade labels (Excellent / Good / Average)

### 🎯 Smart Job Matching
- TF-IDF vectorizer + sklearn cosine similarity
- Matches candidates to **109+ real job listings**
- Ranked recommendations with match % score

</td>
<td width="50%">

### 👤 Candidate Dashboard
- Upload resume → instant skill extraction
- See ATS score, matched skills, job recommendations
- Real-time notifications

### 🏢 HR / Admin Panel
- View all candidates with scores and status
- Shortlist ✅ or Reject ❌ candidates
- Manage job listings (add / edit / delete)
- Dashboard with hiring pipeline stats

### 🔐 Security Hardened
- bcrypt password hashing
- Rate limiting (10 req/min per IP)
- SQL injection protected (parameterized queries)
- CSRF & XSS mitigations
- Session cookie hardening (HTTPOnly, SameSite)

</td>
</tr>
</table>

---

## 🏗️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, Flask 2.x |
| **NLP / ML** | spaCy (NER), scikit-learn (TF-IDF), NLTK |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (SPA) |
| **Database** | SQLite3 (upgradeable to PostgreSQL) |
| **Auth** | Flask Sessions + Werkzeug bcrypt |
| **Resume Parsing** | PyMuPDF (PDF), python-docx (DOCX) |
| **Security** | Flask-Limiter, OWASP hardening |

</div>

---

## 📁 Project Structure

```
HireAI_Website/
├── AI-Resume-Screening-System/
│   ├── app/
│   │   ├── __init__.py              # App factory
│   │   ├── config/
│   │   │   └── settings.py          # Environment config
│   │   ├── routes/
│   │   │   ├── admin_routes.py      # HR/Admin API
│   │   │   ├── user_routes.py       # Candidate API
│   │   │   └── auth_routes.py       # Auth (login/register/logout)
│   │   ├── controllers/
│   │   │   ├── auth_controller.py
│   │   │   └── resume_controller.py
│   │   ├── ml/
│   │   │   ├── skill_extraction/
│   │   │   │   └── extract_skills.py   # spaCy NER skill extractor
│   │   │   ├── ats/
│   │   │   │   └── ats_checker.py      # ATS scoring engine
│   │   │   ├── parsers/
│   │   │   │   ├── pdf_parser.py
│   │   │   │   └── resume_parser.py
│   │   │   └── recommendation/
│   │   │       └── recommend_jobs.py   # TF-IDF job matcher
│   │   ├── models/
│   │   │   └── database.py
│   │   ├── static/
│   │   │   ├── css/style.css
│   │   │   ├── js/app.js            # SPA router + all UI logic
│   │   │   └── img/
│   │   └── templates/
│   │       └── index.html           # Single Page Application
│   ├── trained_models/
│   │   ├── spacy_skill_ner/         # Custom trained spaCy NER
│   │   └── tfidf_recommender/       # TF-IDF vectorizer + model
│   └── run.py                       # Entry point
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.11+
pip
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hetvi-prajapati/HireAI_Website.git
cd HireAI_Website/AI-Resume-Screening-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy model
python -m spacy download en_core_web_sm

# 4. Run the app
python run.py
```

### 5. Open your browser

```
http://127.0.0.1:5000
```

---

## 🔑 Default Accounts

| Role | Email | Password |
|------|-------|----------|
| **HR / Admin** | admin@talentsync.com | admin123 |
| **Candidate** | Register a new account | — |

> ⚠️ Change admin credentials before deploying to production.

---

## 🖼️ Screenshots

<div align="center">

| Landing Page | Candidate Dashboard |
|:---:|:---:|
| <img src="AI-Resume-Screening-System/app/static/img/hero_img.png" width="400" alt="Landing Page"/> | _Upload resume to see AI analysis_ |

| Admin Panel | Candidate Profile Modal |
|:---:|:---:|
| _HR view with all candidates_ | _ATS score, skills, shortlist/reject_ |

</div>

---

## 🧬 How the AI Works

```
📄 Resume Upload (PDF/DOCX)
         │
         ▼
🔍 Text Extraction  ──────────────── PyMuPDF / python-docx
         │
         ▼
🧠 Skill NER Model  ──────────────── spaCy custom NER (500+ skills)
         │
         ▼
📊 ATS Scoring      ──────────────── Skill-to-JD matching algorithm
         │
         ▼
🎯 Job Matching     ──────────────── TF-IDF cosine similarity (109 jobs)
         │
         ▼
✅ Ranked Results   ──────────────── Top matches with % score
```

---

## 🛡️ Security

- ✅ **Bcrypt** password hashing (no plain-text passwords ever)
- ✅ **Parameterized SQL** queries (zero SQL injection risk)
- ✅ **Rate limiting** — 10 login attempts/min per IP
- ✅ **HTTPOnly + SameSite** session cookies
- ✅ **IDOR protection** — users can only access their own data
- ✅ **File upload validation** — PDF/DOCX only, 5MB limit
- ✅ **No hardcoded secrets** — environment variable driven

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔁 Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<!-- Footer wave -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:00c896,50:1a6b4a,100:0d1117&height=120&section=footer"/>

**Made with ❤️ by [Hetvi Prajapati](https://github.com/hetvi-prajapati)**

⭐ **Star this repo if you found it helpful!** ⭐

[![GitHub](https://img.shields.io/badge/GitHub-hetvi--prajapati-181717?style=for-the-badge&logo=github)](https://github.com/hetvi-prajapati)

</div>

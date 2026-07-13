<div align="center">

<!-- Beast Mode Banner -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,50:0a2e22,100:00ff88&height=250&section=header&text=TALENTSYNC&fontSize=70&fontColor=ffffff&fontAlignY=35&desc=THE%20ULTIMATE%20AI%20RECRUITMENT%20ENGINE&descAlignY=55&descSize=20&animation=twinkling"/>

<!-- Aggressive Typing Animation -->
<a href="https://github.com/hetvi-prajapati/HireAI_Website">
  <img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=800&size=24&pause=1000&color=00FF88&center=true&vCenter=true&width=800&lines=NEXT-GEN+AI+RESUME+SCREENING;POWERED+BY+SPACY+NLP;HYPER-OPTIMIZED+ATS+ALGORITHM;REAL-TIME+TF-IDF+MATCHING" alt="Typing SVG" />
</a>

<br/><br/>

<!-- Premium Dark Badges -->
[![Python](https://img.shields.io/badge/Python_3.11-000000?style=for-the-badge&logo=python&logoColor=00FF88)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask_Core-000000?style=for-the-badge&logo=flask&logoColor=00FF88)](https://flask.palletsprojects.com)
[![spaCy](https://img.shields.io/badge/spaCy_NLP-000000?style=for-the-badge&logo=spacy&logoColor=00FF88)](https://spacy.io/)
[![SQLite](https://img.shields.io/badge/SQLite_DB-000000?style=for-the-badge&logo=sqlite&logoColor=00FF88)](https://sqlite.org)
[![JavaScript](https://img.shields.io/badge/Vanilla_JS-000000?style=for-the-badge&logo=javascript&logoColor=00FF88)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Security](https://img.shields.io/badge/OWASP_Secured-000000?style=for-the-badge&logo=owasp&logoColor=00FF88)](https://owasp.org/)

<br/>

[![License](https://img.shields.io/badge/LICENSE-MIT-00FF88?style=for-the-badge&labelColor=000000)](LICENSE)
[![Stars](https://img.shields.io/github/stars/hetvi-prajapati/HireAI_Website?style=for-the-badge&color=00FF88&labelColor=000000)](https://github.com/hetvi-prajapati/HireAI_Website/stargazers)
[![Status](https://img.shields.io/badge/STATUS-ACTIVE-00FF88?style=for-the-badge&labelColor=000000)](#)

</div>

<br/>

> **TalentSync** isn't just an ATS. It's a highly aggressive, precision-engineered AI recruitment engine. It rips through resumes, extracts raw skills using custom NLP models, calculates brutal ATS scores, and executes hyper-accurate candidate-to-job matching using Machine Learning. Built for speed, accuracy, and dominance.

---

## 🔥 ARCHITECTURE & PIPELINE

```mermaid
graph TD
    classDef black fill:#000000,stroke:#00FF88,stroke-width:2px,color:#FFFFFF,font-weight:bold;
    classDef green fill:#00FF88,stroke:#000000,stroke-width:2px,color:#000000,font-weight:bold;
    
    A[Raw Resume Upload PDF/DOCX]:::black --> B(PyMuPDF / docx Parser):::black
    B --> C{spaCy NER Engine}:::green
    C -->|Extracts 500+ Skills| D[Noise Filter & Normalizer]:::black
    D --> E((ATS Scoring Engine)):::green
    E -->|Calculates /100| F[Candidate Profile Built]:::black
    
    F --> G{TF-IDF Vectorizer}:::green
    H[(109+ Job Listings)]:::black --> G
    G -->|Cosine Similarity| I[Ranked Job Matches]:::green
```

---

## ⚡ LETHAL FEATURES

### 🧠 Custom NLP Skill Extraction
- Driven by a custom-trained **spaCy Named Entity Recognition (NER)** model.
- Aggressive noise-filtering context engine ensures fake/fluff words are ignored.
- Parses deeply nested structures inside PDFs and Word documents instantaneously.

### 💀 Ruthless ATS Scoring
- Every candidate is subjected to a strict algorithm evaluating experience, keyword density, and formatting.
- Instant, unforgiving grade labels: **Excellent**, **Good**, or **Average**.

### 🎯 Hyper-Accurate Job Matching
- Machine Learning powered by **scikit-learn** TF-IDF vectorization.
- Computes multi-dimensional cosine similarity across 109+ real-world tech jobs in milliseconds.
- Outputs ranked arrays of exact match percentages.

### 🛡️ Iron-Clad Security
- **Bcrypt** cryptographic password hashing.
- Brutal rate-limiting (10 strikes/min ban).
- Zero-tolerance parameterized SQL queries.
- Hardened OWASP session cookies (HTTPOnly, SameSite).

---

## 💻 BEAST MODE DASHBOARDS

<div align="center">
  <img src="https://raw.githubusercontent.com/hetvi-prajapati/HireAI_Website/main/AI-Resume-Screening-System/app/static/img/hero_img.png" width="800" style="border: 2px solid #00FF88; border-radius: 0px; box-shadow: 0px 0px 20px rgba(0, 255, 136, 0.2);"/>
  <br/><br/>
  <i>The uncompromising split-screen SPA interface. Zero bloat. Pure performance.</i>
</div>

---

## 🛠️ DEPLOYMENT INSTRUCTIONS

Execute the following commands to initialize the engine on your local machine.

```bash
# 1. Clone the repository
git clone https://github.com/hetvi-prajapati/HireAI_Website.git
cd HireAI_Website/AI-Resume-Screening-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download base spaCy models
python -m spacy download en_core_web_sm

# 4. Ignite the server
python run.py
```

Access the terminal at `http://127.0.0.1:5000`

---

## 🔑 SYSTEM ACCESS

| Authority Level | Email | Password |
|:---|:---|:---|
| **COMMAND (HR/Admin)** | `admin@talentsync.com` | `admin123` |
| **OPERATIVE (Candidate)** | Register a new identity | — |

---

<div align="center">

<!-- Beast Mode Footer Wave -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:00ff88,50:0a2e22,100:000000&height=120&section=footer"/>

**BUILT WITH PURE CODE & MACHINE LEARNING BY [HETVI PRAJAPATI](https://github.com/hetvi-prajapati)**

[![GitHub](https://img.shields.io/badge/GITHUB-HETVI_PRAJAPATI-000000?style=for-the-badge&logo=github&logoColor=00FF88)](https://github.com/hetvi-prajapati)

</div>

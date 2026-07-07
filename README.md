<div align="center">

# 🚀 HireAI — Next-Gen Candidate Recommendation & Screening Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange)
![NLP](https://img.shields.io/badge/NLP-spaCy-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg)

An enterprise-grade, AI-powered recruitment platform designed to automate resume parsing, skill extraction, candidate ranking, ATS scoring, and intelligent job matchmaking using Natural Language Processing (NLP) and Machine Learning.

[**Explore the Docs**](#-documentation) · [**Report Bug**](#-contributing) · [**Request Feature**](#-contributing)

</div>

---

## ✨ Features at a Glance

* 🧠 **Intelligent Resume Parsing:** Automatically extracts skills, education, and experience from unstructured PDF resumes using advanced NLP (`spaCy`).
* 🎯 **Smart Job Matchmaking:** Employs TF-IDF Vectorization and Cosine Similarity to find the perfect candidate-to-job fit.
* 📊 **ATS Compatibility Scoring:** Scores applicant resumes out of 100 based on key recruitment metrics.
* 🏆 **Automated Candidate Ranking:** Ranks applicants using a weighted multi-factor algorithm (Skills, Experience, Education, ATS Score).
* 📈 **Interactive HR Dashboards:** Visualizes hiring pipelines, candidate analytics, and KPIs in real-time.

---

## 🏗️ System Architecture

HireAI is built using a modern, scalable tech stack, split into clearly defined layers:

| Component | Technology Used |
| :--- | :--- |
| **Backend API** | Python, Flask, Werkzeug |
| **Machine Learning** | Scikit-Learn (TF-IDF, Cosine Similarity) |
| **NLP Engine** | spaCy (Named Entity Recognition) |
| **Data Processing** | Pandas, NumPy, PyPDF2 |
| **Database** | SQLite (Production-ready for PostgreSQL/MySQL) |
| **Frontend UI** | HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js |

---

## 📂 Repository Structure

This repository is structured as a monorepo containing the core application and related sub-projects.

```text
HireAI_Website/
├── AI-Resume-Screening-System/    # Main backend application, ML models & API
│   ├── app/                       # Flask core, blueprints, business logic
│   ├── datasets/                  # Training data for skill extraction
│   ├── notebooks/                 # Jupyter notebooks for EDA and Model Prototyping
│   ├── tests/                     # Unit test suites
│   └── run.py                     # Entry point to run the server
├── projects/                      # Additional side projects and microservices
└── data/                          # Shared data resources
```

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
Make sure you have Python (>= 3.8) and `pip` installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hetvi-prajapati/HireAI_Website.git
   cd HireAI_Website/AI-Resume-Screening-System
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

---

## 🧪 Machine Learning Pipeline

1. **Text Extraction:** `PyPDF2` extracts raw text from candidate PDF submissions.
2. **Text Cleaning:** Custom preprocessing pipelines remove stop words, URLs, and perform tokenization.
3. **Skill Extraction:** `spaCy` NER models cross-reference text against an extensive internal skills taxonomy.
4. **Vectorization & Matching:** Resumes and Job Descriptions are converted into high-dimensional vectors via `TF-IDF`. We calculate the `Cosine Similarity` to generate a match percentage.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<div align="center">
<b>Made with ❤️ by <a href="https://github.com/hetvi-prajapati">Hetvi Prajapati</a></b>
</div>

# 🖥️ Customer Experience Analytics for Fintech Apps

### 10 Academy – Week 2 Challenge

#### *Initial Project Setup — Terminal Style README*

```
┌──────────────────────────────────────────────────────────────┐
│     Customer Review Analytics • Fintech • NLP • PostgreSQL    │
└──────────────────────────────────────────────────────────────┘
```

## ⚡ Project Boot Sequence

```
$ initializing project...
$ environment: python3 activated
$ loading challenge specification...
$ status: READY
```

This repository marks the **starting point** of a data-driven investigation into customer satisfaction for three major Ethiopian banking apps:

* Commercial Bank of Ethiopia (CBE)
* Bank of Abyssinia (BOA)
* Dashen Bank

Your mission over the week:

> Scrape → Clean → Analyze → Store → Visualize → Recommend

This README represents the **initial commit** and will evolve as the project advances.

---

## 🚀 Project Roadmap (Planned Execution)

```
[Task 1] === Web Scraping & Preprocessing
    ↳ google-play-scraper
    ↳ 1200+ reviews target

[Task 2] === Sentiment & NLP Themes
    ↳ DistilBERT (HuggingFace)
    ↳ VADER / TextBlob
    ↳ spaCy + TF-IDF

[Task 3] === PostgreSQL Integration
    ↳ Create DB
    ↳ Insert cleaned reviews
    ↳ Verify integrity

[Task 4] === Insights & Visualizations
    ↳ Rating distributions
    ↳ Sentiment bars
    ↳ Keyword extractions
    ↳ Business recommendations
```

Each block will be updated, documented, and committed as development continues.

---

## 📁 Current Repository Structure

```
fintech-review-analytics/
├── data/
│   ├── raw/        # scraped data will land here
│   └── clean/      # cleaned & structured outputs
├── scripts/
│   ├── scrape_reviews.py         # (to be created)
│   ├── preprocess.py             # (to be created)
│   ├── sentiment_analysis.py     # (to be created)
│   ├── theme_extraction.py       # (to be created)
│   ├── db_insert.py              # (to be created)
│   └── insights.py               # (to be created)
├── requirements.txt
├── README.md
└── .gitignore
```

> 📝 *Additional directories (e.g., `/reports`, `/notebooks`) will be added as the project matures.*

---

## ⚙️ Installation & Setup

### 🔧 Clone Repository

```bash
git clone <https://github.com/Miftah-Ebrahim/Fintech-Mobile-CX-Analytics>
cd Fintech-Mobile-CX-Analytics
```

### 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔧 Run First Script (Coming Soon)

```bash
python scripts/scrape_reviews.py
```

---

## 🧰 Technology Stack (Planned)

```
[ Data Collection ]
    └─ google-play-scraper

[ Data Processing ]
    └─ pandas, numpy

[ NLP / ML ]
    ├─ HuggingFace transformers (DistilBERT)
    ├─ spaCy
    ├─ scikit-learn
    ├─ VADER, TextBlob

[ Database Layer ]
    └─ PostgreSQL + psycopg2

[ Visualization ]
    └─ matplotlib, seaborn
```

---

## 📅 Challenge Timeline (Week 2)

```
26 Nov  — Challenge Kickoff
30 Nov  — Interim Report (Scraping + Early Analysis)
02 Dec  — Final Submission (All tasks + Report)
```

---

## 👨‍💻 Contributors

```
Facilitators: Kerod • Mahbubah • Filimon
Developer:   Miftah E
```

---

## 📄 Notes

This README is a **first-stage blueprint**.
As the project progresses, additional sections will be appended:

```
+ Data Dictionary
+ SQL Schema
+ Pipeline Diagrams
+ Final Visualizations
+ Insights & Recommendations
+ PDF Reports
```

Stay tuned for updates as the project evolves from **prototype → production-ready analysis**.

```
$ exiting README...
$ progress saved successfully.
```

<div align="center">

# 📱 Fintech Mobile CX Analytics
### *Unlocking Customer Insights through Data*

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=2E86C1&background=FFFFFF00&center=true&vCenter=true&width=500&lines=Sentiment+Analysis+Pipeline;Google+Play+Store+Scraping;Natural+Language+Processing;Actionable+Business+Insights)](https://git.io/typing-svg)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[View Demo](#-visualizations) • [Report Bug](issues) • [Request Feature](issues)

</div>

---

## 🚀 **Project Overview**

**Fintech Mobile CX Analytics** is an end-to-end automated pipeline designed to analyze customer sentiment for Ethiopia's top banking applications: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank**.

By leveraging **Natural Language Processing (NLP)** and **Machine Learning**, this project transforms raw Google Play Store reviews into actionable business strategies, helping banks reduce churn and improve user satisfaction.

---

## 💎 **Key Features**

| Feature | Description |
| :--- | :--- |
| 🕷️ **Automated Scraping** | Fetches thousands of real-time reviews using `google-play-scraper`. |
| 🧹 **Smart Preprocessing** | Advanced cleaning pipeline (Deduplication, Normalization, Lemmatization). |
| 🧠 **Sentiment Engine** | Powered by **VADER** to classify feedback as Positive, Neutral, or Negative. |
| 🔍 **Topic Modeling** | Extracts hidden themes and N-grams to identify specific pain points. |
| 🗄️ **Data Warehousing** | Robust storage using **PostgreSQL** for scalable analytics. |
| 📊 **Interactive Dashboard** | Beautiful visualizations generated via Matplotlib & Seaborn. |

---

## 🏗️ **Architecture**

```mermaid
graph LR
    A[Google Play Store] -->|Scraper| B(Raw Data)
    B -->|Preprocessing| C{Clean Data}
    C -->|VADER Engine| D[Sentiment Scores]
    C -->|NLP| E[Keywords & Themes]
    D --> F[(PostgreSQL DB)]
    E --> F
    F --> G[Visualizations & Reports]
```

---

## 📂 **Project Structure**

```bash
project/
├── 📂 data/                 # Data storage
│   ├── 📂 raw/              # Raw scraped reviews
│   ├── 📂 clean/            # Preprocessed datasets
│   └── 📂 processed/        # Sentiment analysis results
│
├── 📂 database/             # Database scripts
│   ├── schema.sql           # Table definitions
│   └── queries.sql          # Analytical queries
│
├── 📂 notebooks/            # Interactive Analysis
│   ├── 01_scraping.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_sentiment_analysis.ipynb
│   ├── 04_topic_modeling.ipynb
│   └── 05_visualizations.ipynb
│
├── 📂 scripts/              # Production Pipeline
│   ├── scraper.py
│   ├── preprocess.py
│   ├── sentiment_analysis.py
│   ├── keyword_thematic.py
│   ├── db_upload.py
│   └── main_pipeline.py     # 🚀 ORCHESTRATOR
│
├── 📂 reports/              # Final Deliverables
│   ├── 📂 dashboard/        # Generated Plots
│   └── final_report.md      # Executive Summary
│
└── README.md                # You are here!
```

---

## ⚡ **Getting Started**

### **Prerequisites**
*   Python 3.8+
*   PostgreSQL

### **Installation**

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Miftah-Ebrahim/Fintech-Mobile-CX-Analytics.git
    cd Fintech-Mobile-CX-Analytics
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Database**
    *   Create a database named `bank_reviews` in PostgreSQL.
    *   Update `.env` file with your credentials:
        ```ini
        DB_HOST=localhost
        DB_NAME=bank_reviews
        DB_USER=postgres
        DB_PASS=your_password
        ```

---

## 🏃 **Usage**

### **Option 1: Run Full Pipeline**
Execute the master script to run all stages (Preprocessing → Analysis → Database Upload):
```bash
python scripts/main_pipeline.py
```

### **Option 2: Interactive Notebooks**
Explore the data step-by-step using Jupyter:
```bash
jupyter notebook notebooks/
```

---

## 📊 **Visualizations**

<div align="center">
  <img src="reports/dashboard/rating_distribution.png" alt="Rating Distribution" width="45%">
  <img src="reports/dashboard/sentiment_trend.png" alt="Sentiment Trend" width="45%">
</div>

> *Sample insights generated from the analysis pipeline.*

---

## 🏆 **Results & Insights**

*   **CBE:** High friction in login processes (`"Connection Error"`).
*   **BOA:** Recent updates caused stability issues (`"App Crash"`).
*   **Dashen:** Strong feature set but integration issues with Amole (`"Wallet Sync"`).

👉 **[Read the Full Report](reports/final_report.md)**

---

<div align="center">

### *Built with ❤️ by Mifta Y*

</div>

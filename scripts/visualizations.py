import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path

from utils import setup_logging

# --- CONFIGURATION ---
logger = setup_logging(__name__)

INPUT_FILE = Path("data/processed/sentiment_results.csv")
REPORT_DIR = Path("reports/dashboard")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def load_data():
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return None
    return pd.read_csv(INPUT_FILE)


def plot_rating_distribution(df):
    logger.info("Generating Rating Distribution Plot...")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x="rating", hue="bank_name", palette="viridis")
    plt.title("Rating Distribution by Bank")
    plt.xlabel("Rating (1-5)")
    plt.ylabel("Count")
    plt.legend(title="Bank")
    plt.savefig(REPORT_DIR / "rating_distribution.png")
    plt.close()


def plot_sentiment_trend(df):
    logger.info("Generating Sentiment Trend Plot...")
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["month_year"] = df["review_date"].dt.to_period("M")

    trend_df = (
        df.groupby(["month_year", "bank_name"])["sentiment_score"].mean().reset_index()
    )
    trend_df["month_year"] = trend_df["month_year"].astype(str)

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=trend_df, x="month_year", y="sentiment_score", hue="bank_name", marker="o"
    )
    plt.title("Average Sentiment Score Trend")
    plt.xticks(rotation=45)
    plt.ylabel("Avg Sentiment Score")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "sentiment_trend.png")
    plt.close()


def generate_wordclouds(df):
    logger.info("Generating Word Clouds...")
    for bank in df["bank_name"].unique():
        for label in ["Positive", "Negative"]:
            subset = df[(df["bank_name"] == bank) & (df["sentiment_label"] == label)]
            if subset.empty:
                continue

            text = " ".join(subset["cleaned_text"].astype(str))
            wc = WordCloud(width=800, height=400, background_color="white").generate(
                text
            )

            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.title(f"{bank} - {label} Reviews")
            plt.savefig(REPORT_DIR / f"wordcloud_{bank}_{label}.png")
            plt.close()


def main():
    df = load_data()
    if df is not None:
        plot_rating_distribution(df)
        plot_sentiment_trend(df)
        generate_wordclouds(df)
        logger.info(f"Visualizations saved to {REPORT_DIR}")


if __name__ == "__main__":
    main()

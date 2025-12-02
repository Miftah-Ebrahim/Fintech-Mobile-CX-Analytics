import pandas as pd
from pathlib import Path

from utils import setup_logging

# --- CONFIGURATION ---
logger = setup_logging(__name__)

INPUT_FILE = Path("data/processed/sentiment_results.csv")
OUTPUT_FILE = Path("reports/insights_summary.txt")


def generate_insights():
    if not INPUT_FILE.exists():
        logger.error("Data file not found.")
        return

    df = pd.read_csv(INPUT_FILE)

    with open(OUTPUT_FILE, "w") as f:
        f.write("FINTECH MOBILE CX ANALYTICS - AUTOMATED INSIGHTS\n")
        f.write("================================================\n\n")

        for bank in df["bank_name"].unique():
            bank_df = df[df["bank_name"] == bank]
            avg_score = bank_df["sentiment_score"].mean()
            top_rating_count = len(bank_df[bank_df["rating"] == 5])
            low_rating_count = len(bank_df[bank_df["rating"] == 1])

            f.write(f"BANK: {bank}\n")
            f.write(f"  - Average Sentiment: {avg_score:.2f}\n")
            f.write(f"  - 5-Star Reviews: {top_rating_count}\n")
            f.write(f"  - 1-Star Reviews: {low_rating_count}\n")
            f.write("\n")

    logger.info(f"Insights generated at {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_insights()

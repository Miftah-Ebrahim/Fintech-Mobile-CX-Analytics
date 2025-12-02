import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
from typing import List, Tuple

from utils import setup_logging

# --- CONFIGURATION ---
logger = setup_logging(__name__)

INPUT_FILE = Path("data/processed/sentiment_results.csv")
OUTPUT_DIR = Path("reports/insights")  # Intermediate insights storage


def load_data(file_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise


def get_top_n_grams(
    corpus: List[str], n: int = 1, top_k: int = 10
) -> List[Tuple[str, int]]:
    """
    Extracts top N-grams from a list of text strings.
    """
    if not corpus:
        return []

    vec = CountVectorizer(ngram_range=(n, n), stop_words="english").fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:top_k]


def analyze_bank_themes(df: pd.DataFrame, bank_name: str):
    """
    Analyzes keywords and themes for a specific bank.
    """
    bank_df = df[df["bank_name"] == bank_name]
    corpus = bank_df["processed_text"].dropna().tolist()

    if not corpus:
        logger.warning(f"No data found for {bank_name}")
        return

    print(f"\n=== Analysis for {bank_name} ===")

    # Unigrams (Keywords)
    top_keywords = get_top_n_grams(corpus, n=1, top_k=10)
    print("Top 10 Keywords:")
    for word, freq in top_keywords:
        print(f"  - {word}: {freq}")

    # Bigrams (Themes/Context)
    top_bigrams = get_top_n_grams(corpus, n=2, top_k=5)
    print("\nTop 5 Themes (Bigrams):")
    for phrase, freq in top_bigrams:
        print(f"  - {phrase}: {freq}")

    # Negative Themes (Pain Points)
    neg_corpus = (
        bank_df[bank_df["sentiment_label"] == "Negative"]["processed_text"]
        .dropna()
        .tolist()
    )
    if neg_corpus:
        top_neg_bigrams = get_top_n_grams(neg_corpus, n=2, top_k=3)
        print("\nTop 3 Pain Points (Negative Bigrams):")
        for phrase, freq in top_neg_bigrams:
            print(f"  - {phrase}: {freq}")


def main():
    if not INPUT_FILE.exists():
        logger.error(
            f"Input file not found: {INPUT_FILE}. Run sentiment_analysis.py first."
        )
        return

    df = load_data(INPUT_FILE)

    banks = df["bank_name"].unique()

    for bank in banks:
        analyze_bank_themes(df, bank)


if __name__ == "__main__":
    main()

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pathlib import Path

from utils import setup_logging

# --- CONFIGURATION ---
logger = setup_logging(__name__)

INPUT_FILE = Path("data/clean/reviews_clean.csv")
OUTPUT_FILE = Path("data/processed/sentiment_results.csv")

# Ensure NLTK resources are available
try:
    nltk.data.find("vader_lexicon")
    nltk.data.find("stopwords")
    nltk.data.find("punkt")
    nltk.data.find("wordnet")
except LookupError:
    logger.info("Downloading NLTK resources...")
    nltk.download("vader_lexicon")
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("punkt_tab")


def load_data(file_path: Path) -> pd.DataFrame:
    """Loads the cleaned dataset."""
    try:
        logger.info(f"Loading data from {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise


def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies VADER sentiment analysis.
    Adds 'sentiment_score' and 'sentiment_label'.
    """
    logger.info("Initializing VADER Sentiment Analyzer...")
    sia = SentimentIntensityAnalyzer()

    def get_sentiment(text):
        if not isinstance(text, str):
            return 0.0, "Neutral"

        score = sia.polarity_scores(text)["compound"]

        if score >= 0.05:
            label = "Positive"
        elif score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return score, label

    logger.info("Calculating sentiment scores...")
    # Apply to the dataframe
    df[["sentiment_score", "sentiment_label"]] = df["cleaned_text"].apply(
        lambda x: pd.Series(get_sentiment(x))
    )

    return df


def preprocess_for_keywords(
    text: str, stop_words: set, lemmatizer: WordNetLemmatizer
) -> str:
    """
    Tokenizes, removes stop words, and lemmatizes text for keyword extraction.
    """
    if not isinstance(text, str):
        return ""

    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove stopwords and non-alphabetic tokens, then lemmatize
    cleaned_tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalpha() and token not in stop_words
    ]

    return " ".join(cleaned_tokens)


def prepare_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'processed_text' column for keyword analysis.
    """
    logger.info(
        "Preprocessing text for keyword extraction (Tokenization, Stopwords, Lemmatization)..."
    )
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    df["processed_text"] = df["cleaned_text"].apply(
        lambda x: preprocess_for_keywords(x, stop_words, lemmatizer)
    )
    return df


def save_results(df: pd.DataFrame, output_path: Path) -> None:
    """Saves the results to CSV."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Sentiment analysis results saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")


def main():
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    df = load_data(INPUT_FILE)

    # 1. Sentiment Analysis
    df = analyze_sentiment(df)

    # 2. Prepare for Keyword/Thematic Analysis
    df = prepare_keywords(df)

    # Save
    save_results(df, OUTPUT_FILE)

    # Validation
    print("\n--- Sentiment Distribution ---")
    print(df["sentiment_label"].value_counts())
    print("\n--- Sample Results ---")
    print(df[["cleaned_text", "sentiment_label", "sentiment_score"]].head())


if __name__ == "__main__":
    main()

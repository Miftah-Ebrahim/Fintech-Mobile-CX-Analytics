import logging
import pandas as pd
import re
from pathlib import Path
from typing import Optional, Tuple

# --- CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

INPUT_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
LATEST_FILE_PATTERN = "reviews_raw_*.csv"


def load_latest_data(input_dir: Path) -> Optional[pd.DataFrame]:
    """
    Locates and loads the most recent CSV file from the raw data directory.
    """
    try:
        # glob returns a generator, we turn it into a list and sort to find the newest
        files = sorted(input_dir.glob(LATEST_FILE_PATTERN), reverse=True)

        if not files:
            logger.error("No raw data files found in data/raw/")
            return None

        latest_file = files[0]
        logger.info(f"Loading latest dataset: {latest_file}")
        return pd.read_csv(latest_file)

    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        return None


def clean_text(text: str) -> str:
    """
    Standardizes text data:
    1. Converts to string (handles NaNs).
    2. Removes excessive whitespace.
    3. Strips leading/trailing spaces.
    """
    if not isinstance(text, str):
        return ""

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the cleaning steps in a functional pipeline.
    """
    initial_count = len(df)
    logger.info(f"Starting preprocessing on {initial_count} records...")

    # 1. Deduplication (Critical for Scraped Data)
    # We drop duplicates based on User, Date, and Content to avoid skewing analysis
    df = df.drop_duplicates(subset=["user_name", "review_date", "review_text"])
    duplicates_removed = initial_count - len(df)
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate records.")

    # 2. Date Conversion
    # Coerce errors to NaT (Not a Time) so the script doesn't crash on bad formats
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

    # 3. Text Normalization
    df["cleaned_text"] = df["review_text"].apply(clean_text)

    # 4. Feature Engineering: Review Length
    # Business Insight: Longer reviews often contain more specific complaints/praise
    df["word_count"] = df["cleaned_text"].apply(lambda x: len(x.split()))

    # 5. Handling Missing Values
    # We drop rows where the review text is empty or date is invalid
    df = df.dropna(subset=["cleaned_text", "review_date"])

    logger.info(f"Preprocessing complete. Final count: {len(df)} records.")
    return df


def save_processed_data(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Saves the clean dataframe to the processed directory.
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "reviews_cleaned.csv"

        # Save index=False to keep the file clean
        df.to_csv(output_path, index=False)
        logger.info(f"Cleaned data saved to: {output_path}")

    except IOError as e:
        logger.error(f"Failed to save processed data: {str(e)}")


def main():
    df = load_latest_data(INPUT_DIR)

    if df is not None:
        clean_df = process_pipeline(df)
        save_processed_data(clean_df, OUTPUT_DIR)

        # Validation: Print a sample
        print("\n--- Data Quality Check (Head) ---")
        print(clean_df[["review_date", "bank_name", "cleaned_text"]].head())
        print("\n--- Bank Distribution ---")
        print(clean_df["bank_name"].value_counts())


if __name__ == "__main__":
    main()

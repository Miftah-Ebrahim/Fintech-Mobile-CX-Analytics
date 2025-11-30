import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from google_play_scraper import Sort, reviews

# --- CONFIGURATION ---

# Configure Logging: Standard format for production logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# App IDs (Package Names) - Updated Nov 2025
APP_PACKAGES = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp",
}

# Configuration Constants
TARGET_COUNT = 500
OUTPUT_DIR = Path("data/raw")
DEFAULT_COUNTRY = "et"
DEFAULT_LANG = "en"


def fetch_reviews(
    bank_name: str, app_id: str, count: int = TARGET_COUNT
) -> List[Dict[str, Any]]:
    """
    Fetches review data from the Google Play Store API.

    Args:
        bank_name (str): The display name of the bank.
        app_id (str): The package name (e.g., com.example.app).
        count (int): Number of reviews to retrieve.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing processed review data.
    """
    logger.info(
        f"Starting extraction for {bank_name} ({app_id}) - Target: {count} reviews"
    )

    try:
        result, _ = reviews(
            app_id,
            lang=DEFAULT_LANG,
            country=DEFAULT_COUNTRY,
            sort=Sort.NEWEST,
            count=count,
        )

        if not result:
            logger.warning(
                f"No reviews returned for {bank_name}. Verify App ID validity."
            )
            return []

        cleaned_data = []
        for r in result:
            # Extract only relevant fields for downstream analysis
            entry = {
                "source": "Google Play",
                "bank_name": bank_name,
                "app_id": app_id,
                "review_date": r["at"],
                "user_name": r["userName"],
                "rating": r["score"],
                "review_text": r["content"],
                "thumbs_up_count": r["thumbsUpCount"],
                "app_version": r["reviewCreatedVersion"],
            }
            cleaned_data.append(entry)

        logger.info(
            f"Successfully extracted {len(cleaned_data)} records for {bank_name}"
        )
        return cleaned_data

    except Exception as e:
        logger.error(f"Failed to fetch data for {bank_name}: {str(e)}", exc_info=True)
        return []


def save_dataset(data: List[Dict[str, Any]], output_dir: Path) -> Optional[Path]:
    """
    Persists the aggregated data to a CSV file.

    Args:
        data (List[Dict]): The list of review records.
        output_dir (Path): The directory path for output.

    Returns:
        Optional[Path]: The path to the saved file, or None if save failed.
    """
    if not data:
        logger.warning("No data to save. Skipping file generation.")
        return None

    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        df = (
            pd.read_csv("data/raw/raw_reviews.csv")
            if os.path.exists("data/raw/raw_reviews.csv")
            else pd.DataFrame(data)
        )

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"reviews_raw_{timestamp}.csv"
        file_path = output_dir / filename

        df.to_csv(file_path, index=False, encoding="utf-8")

        logger.info(f"Dataset successfully saved to: {file_path}")
        logger.info(f"Total Records: {len(df)}")
        return file_path

    except IOError as e:
        logger.error(f"IO Error during file save: {str(e)}")
        return None


def main():
    """
    Main execution pipeline.
    """
    logger.info("Initializing Scraper Pipeline...")

    all_reviews = []

    for bank, app_id in APP_PACKAGES.items():
        bank_data = fetch_reviews(bank, app_id)
        if bank_data:
            all_reviews.extend(bank_data)

    save_dataset(all_reviews, OUTPUT_DIR)

    logger.info("Pipeline execution completed.")


if __name__ == "__main__":
    import os  # Needed for the check in save_dataset, keeping imports local if preferred or move to top

    main()

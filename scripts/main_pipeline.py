import subprocess
import sys
from pathlib import Path

from utils import setup_logging

# --- CONFIGURATION ---
logger = setup_logging(__name__)

SCRIPTS_DIR = Path("scripts")


def run_script(script_name):
    """Runs a python script located in the scripts directory."""
    script_path = SCRIPTS_DIR / script_name
    logger.info(f"--- Running {script_name} ---")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Output:\n{result.stdout}")
        logger.info(f"--- {script_name} Completed Successfully ---\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {script_name}:")
        logger.error(e.stderr)
        return False


def main():
    logger.info("Starting Fintech Mobile CX Analytics Pipeline...")

    # 1. Data Collection (Optional if data exists, but good to include)
    # Skipping scraper.py for now to avoid re-scraping in this demo run,
    # but in a real pipeline, it would be first.
    # if not run_script("scraper.py"): return

    # 2. Preprocessing
    if not run_script("preprocess.py"):
        return

    # 3. Sentiment Analysis
    if not run_script("sentiment_analysis.py"):
        return

    # 4. Keyword/Thematic Analysis
    if not run_script("keyword_thematic.py"):
        return

    # 5. Database Upload
    # Note: Requires .env or env vars to be set
    if not run_script("db_upload.py"):
        return

    # 6. Visualizations & Insights
    if not run_script("visualizations.py"):
        return
    if not run_script("insights.py"):
        return

    logger.info("Pipeline Execution Completed Successfully.")


if __name__ == "__main__":
    main()

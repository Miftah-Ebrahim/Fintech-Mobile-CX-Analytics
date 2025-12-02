import logging
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def test_connection():
    """Tests the PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "bank_reviews"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT", "5432"),
        )
        logger.info(" Connection Successful!")

        # Verify version
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        logger.info(f"Database Version: {db_version[0]}")

        cur.close()
        conn.close()
        return True

    except Exception as e:
        logger.error(f"Connection Failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()

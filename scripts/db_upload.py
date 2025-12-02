import pandas as pd
import psycopg2
from psycopg2 import sql
from pathlib import Path
import os
from dotenv import load_dotenv
from utils import setup_logging

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
logger = setup_logging(__name__)

INPUT_FILE = Path("data/processed/sentiment_results.csv")

# Database Credentials - Should be set via Environment Variables for security
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        return conn
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return None


def setup_database(conn):
    """Runs the schema.sql to create tables."""
    try:
        cur = conn.cursor()
        schema_path = Path("database/schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()

        cur.execute(schema_sql)
        conn.commit()
        logger.info("Database schema initialized.")
        cur.close()
    except Exception as e:
        logger.error(f"Failed to setup database: {e}")
        conn.rollback()


def upload_data(conn, df):
    """Uploads banks and reviews to the database."""
    cur = conn.cursor()

    try:
        # 1. Insert Banks
        banks = df["bank_name"].unique()
        bank_map = {}  # name -> id

        for bank in banks:
            # Upsert bank (simple ignore if exists for this project logic)
            cur.execute(
                "INSERT INTO banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING RETURNING bank_id;",
                (bank,),
            )
            result = cur.fetchone()

            if result:
                bank_map[bank] = result[0]
            else:
                # Fetch existing if not inserted
                cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s;", (bank,))
                bank_map[bank] = cur.fetchone()[0]

        logger.info(f"Banks processed: {bank_map}")

        # 2. Insert Reviews
        logger.info(f"Uploading {len(df)} reviews...")

        # Prepare list of tuples for batch insertion
        # Columns: bank_id, review_text, rating, review_date, sentiment_label, sentiment_score

        # Note: We need to map bank_name to bank_id

        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    bank_map[row["bank_name"]],
                    row["cleaned_text"],  # Using cleaned text
                    row["rating"],
                    row["review_date"],
                    row["sentiment_label"],
                    row["sentiment_score"],
                ),
            )

        conn.commit()
        logger.info("Data upload complete.")

    except Exception as e:
        logger.error(f"Failed to upload data: {e}")
        conn.rollback()
    finally:
        cur.close()


def main():
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    logger.info("Connecting to database...")
    conn = get_db_connection()

    if not conn:
        logger.error("Could not connect to database. Please check credentials.")
        return

    df = pd.read_csv(INPUT_FILE)

    setup_database(conn)
    upload_data(conn, df)

    conn.close()


if __name__ == "__main__":
    main()

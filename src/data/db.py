import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

Base = declarative_base()

SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = psycopg2.connect(
            f"postgresql://postgres:{SUPABASE_ANON_KEY}@{SUPABASE_PROJECT_ID}.supabase.co:5432/postgres"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None


def create_tables(conn):
    """Creates the database tables."""
    try:
        with conn.cursor() as cur:
            with open("src/data/schema.sql", "r") as f:
                cur.execute(f.read())
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
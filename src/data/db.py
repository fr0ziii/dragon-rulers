import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
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

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        create_tables(conn)
        conn.close()
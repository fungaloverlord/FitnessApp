import sqlite3
import pandas as pd
import os

# Convert to absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "assets/macrotracker.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        return conn
    except sqlite3.OperationalError as e:
        print(f"Error opening database: {e}")
        raise

def fetch_data(table: str):
    try:
        with get_db_connection() as conn:
            return pd.read_sql_query(f"SELECT * FROM {table}", conn)
    except Exception as e:
        print(f"Error fetching data from {table}: {e}")
        raise

def update_database(data, table_name: str):
    try:
        conn = get_db_connection()
        df = pd.DataFrame(data)
        if not df.empty:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
    except Exception as e:
        print(f"Error updating {table_name}: {e}")
        raise
    finally:
        conn.close()

def get_foods():
    try:
        with get_db_connection() as conn:
            df = pd.read_sql_query("SELECT food FROM foods", conn)
            return df["food"].unique()
    except Exception as e:
        print(f"Error fetching foods: {e}")
        raise


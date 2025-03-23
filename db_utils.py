import sqlite3
import pandas as pd
import os
from datetime import datetime

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
        cursor = conn.cursor()

        # Convert input data to DataFrame
        df_new = pd.DataFrame(data)

        # Fetch existing data from the database
        existing_data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

        # Identify rows to delete (based on actual data differences, not just IDs)
        merged_data = existing_data.merge(df_new, on="id", how="left", indicator=True)
        deleted_rows = merged_data[merged_data['_merge'] == 'left_only']

        # Perform deletions if necessary
        for _, row in deleted_rows.iterrows():
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row['id'],))

        # Perform updates or inserts
        for _, row in df_new.iterrows():
            # Check if the record already exists
            cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE id = ?", (row["id"],))
            exists = cursor.fetchone()[0]

            if exists:
                # Update existing record
                columns = ", ".join(f"{k} = ?" for k in row.index if k != "id")
                values = [row[k] for k in row.index if k != "id"]
                values.append(row["id"])
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET {columns}
                    WHERE id = ?
                """, values)
            else:
                # Insert new record
                columns = ", ".join(row.index)
                placeholders = ", ".join(["?" for _ in row.index])
                values = list(row)
                cursor.execute(f"""
                    INSERT INTO {table_name} ({columns})
                    VALUES ({placeholders})
                """, values)

        conn.commit()
    except Exception as e:
        print(f"Error updating {table_name}: {e}")
        raise
    finally:
        conn.close()


def add_new_food(food, weight, fat, carbs, protein):
    conn = get_db_connection()
    cursor = conn.cursor()
    food_data = fetch_data('foods')
    if 'id' in food_data.columns:
        new_id = str(max([int(x) for x in fetch_data('foods')['id']]) + 1)
    else:
        new_id = '1'

    cursor.execute("""
        INSERT INTO foods (id, food, weight, fat, carbs, protein)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_id, food, weight, fat, carbs, protein))

    conn.commit()
    conn.close()

def add_new_entry(meal,food, weight):
    conn = get_db_connection()
    cursor = conn.cursor()
    food_data = fetch_data('entries')
    if 'id' in food_data.columns:
        new_id = str(max([int(x) for x in fetch_data('entries')['id']]) + 1)
    else:
        new_id = '1'

    cursor.execute("""
        INSERT INTO entries (id, food, weight, entry_date, meal)
        VALUES (?, ?, ?, ?, ?)
    """, (new_id, food, weight, datetime.now().strftime("%m-%d-%Y"),meal))

    conn.commit()
    conn.close()

def get_foods():
    try:
        with get_db_connection() as conn:
            df = pd.read_sql_query("SELECT food FROM foods", conn)
            return df["food"].unique()
    except Exception as e:
        print(f"Error fetching foods: {e}")
        raise

def remove_all_triggers():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all trigger names
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'trigger';")
    triggers = cursor.fetchall()

    if triggers:
        # Loop through each trigger and drop it
        for trigger in triggers:
            trigger_name = trigger[0]
            try:
                cursor.execute(f"DROP TRIGGER {trigger_name}")
                print(f"Trigger '{trigger_name}' removed successfully.")
            except sqlite3.Error as e:
                print(f"Failed to remove trigger '{trigger_name}': {e}")
        # Commit changes
        connection.commit()
    else:
        print("No triggers found in the database.")

    # Close the connection
    connection.close()

def list_triggers(table_name):
    # Query triggers for the specified table
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM sqlite_master WHERE type = 'trigger' AND tbl_name = ?;"
    cursor.execute(query, (table_name,))
    triggers = cursor.fetchall()

    # Display the triggers
    if triggers:
        print(f"Triggers for table '{table_name}':")
        for trigger in triggers:
            print(trigger[0])
    else:
        print(f"No triggers found for table '{table_name}'.")

    # Close the connection
    conn.close()

def add_triggers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TRIGGER total_calories_insert
        AFTER INSERT ON foods
        FOR EACH ROW
        BEGIN
            UPDATE foods
            SET calories = (NEW.fat * 9) + (NEW.carbs * 4) + (NEW.protein * 4)
            WHERE id = NEW.id;
        END;
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TRIGGER total_calories_update
        AFTER UPDATE ON foods
        FOR EACH ROW
        BEGIN
            UPDATE foods
            SET calories = (NEW.fat * 9) + (NEW.carbs * 4) + (NEW.protein * 4)
            WHERE id = NEW.id;
        END;
    ''')
    conn.commit()

def sql(query):
    print(fetch_data("entries"))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    print(fetch_data("entries"))

# remove_all_triggers()
# add_triggers()
# list_triggers("foods")

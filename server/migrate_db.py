import sqlite3
import os

DB_FILE = 'instance/ecotrace.db'

def migrate_db():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    columns_to_add = [
        ("eco_points", "INTEGER DEFAULT 0"),
        ("trees_planted", "INTEGER DEFAULT 0"),
        ("co2_saved_kg", "FLOAT DEFAULT 0.0"),
        ("events_attended", "INTEGER DEFAULT 0")
    ]
    
    print("Checking for missing columns...")
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(user)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            print(f"Adding column: {col_name}")
            try:
                cursor.execute(f"ALTER TABLE user ADD COLUMN {col_name} {col_type}")
                print(f"Successfully added {col_name}")
            except sqlite3.OperationalError as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate_db()

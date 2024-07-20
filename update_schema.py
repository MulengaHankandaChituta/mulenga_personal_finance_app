import sqlite3

def update_database_schema():
    conn = sqlite3.connect('finance_management.db')
    cursor = conn.cursor()
    
    # Create a new table with the additional 'date' column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')

    # Copy data from the old table to the new table
    cursor.execute('''
        INSERT INTO new_expenses (id, amount, category)
        SELECT id, amount, category FROM expenses
    ''')

    # Drop the old table
    cursor.execute('DROP TABLE expenses')

    # Rename the new table to the original table name
    cursor.execute('ALTER TABLE new_expenses RENAME TO expenses')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_database_schema()
    print("Database schema updated successfully.")
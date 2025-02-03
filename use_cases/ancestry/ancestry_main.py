# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:49:59 2025

@author: otrevizo

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_inspect.py         # Print tables
│── ancestry_tests.py           # Unit tests for database functions
│── ancestry_export_xlsx.py     # Write db to Excel file

"""
import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_NAME = "ancestry.db"
INPUT_FILE = "ancestry_input.xlsx"

# Establish database connection
def connect_db():
    return sqlite3.connect(DB_NAME)

# Read input Excel file
def read_input_file():
    try:
        df_people = pd.read_excel(INPUT_FILE, sheet_name="People")
        df_relationships = pd.read_excel(INPUT_FILE, sheet_name="Relationships")
        return df_people, df_relationships
    except Exception as e:
        print(f"Error reading {INPUT_FILE}: {e}")
        return None, None

# Fetch existing data from the database
def fetch_existing_data():
    conn = connect_db()
    df_db_people = pd.read_sql("SELECT * FROM People", conn)
    df_db_relationships = pd.read_sql("SELECT * FROM Relationships", conn)
    conn.close()
    return df_db_people, df_db_relationships

# Compare and find differences
def compare_and_update(df_people, df_relationships, df_db_people, df_db_relationships):
    conn = connect_db()
    cursor = conn.cursor()
    changes_log = []

    # Process People sheet
    for index, row in df_people.iterrows():
        existing_person = df_db_people[df_db_people['person_id'] == row['person_id']]
        if not existing_person.empty:
            # Check for changes in existing person
            if not existing_person.equals(pd.DataFrame([row])): 
                # Update existing person
                update_query = "UPDATE People SET "
                update_values = []
                for col in df_people.columns:
                    if existing_person[col].values[0] != row[col]:
                        update_query += f"{col}=?, "  # Use f-string here to include column name
                        update_values.append(row[col])
                update_query = update_query[:-2] + f" WHERE person_id = {row['person_id']}" 
                cursor.execute(update_query, update_values) 
                changes_log.append(f"Updated Person: {row['person_id']}")
        else:
            # Add new person
            cursor.execute("INSERT INTO People (person_id, name, birthdate) VALUES (?, ?, ?)", 
                           (row['person_id'], row['name'], row['birthdate']))
            changes_log.append(f"Added Person: {row['person_id']}")

    # ... (Process Relationships sheet) ...

    conn.commit()
    conn.close()
    return changes_log

# Rename input file after processing
def archive_input_file():
    timestamp = datetime.now().strftime("%Y.%m.%d")
    new_name = f"ancestry_digested_{timestamp}.xlsx"
    os.rename(INPUT_FILE, new_name)
    print(f"Renamed {INPUT_FILE} to {new_name}")

# Main execution function
def main():
    df_people, df_relationships = read_input_file()
    if df_people is None or df_relationships is None:
        return
    
    df_db_people, df_db_relationships = fetch_existing_data()
    
    changes_log = compare_and_update(df_people, df_relationships, df_db_people, df_db_relationships)
    
    if changes_log:
        print("Changes made:")
        for log in changes_log:
            print(log)
    else:
        print("No changes detected.")
    
    archive_input_file()

if __name__ == "__main__":
    main()


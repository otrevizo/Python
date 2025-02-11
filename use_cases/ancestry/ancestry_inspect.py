# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 08:50:19 2025

@author: otrevizo

This script connects to ancestry.db and prints out all table names.

ancestry_project/
│── ancestry_db.py              # Handles database interactions (the class)
│── ancestry_get_input_xlsx.py  # Get ancestry_input.xlsx and update the db
│── ancestry_inspect.py         # Display table
│── ancestry_tests.py           # Adds records to the db, hardcoded, by hand
│── ancestry_export_xlsx.py     # Write db to Excel file
│── ancestry_family_tree.py     # Build the family tree (previous gens)

"""

import sqlite3

DB_NAME = "ancestry.db"

def list_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    
    conn.close()
    
def show_table_contents(table_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    print(f"\nContents of {table_name}:")
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == "__main__":
    list_tables()

    tables = ["People"]
    for table in tables:
        show_table_contents(table)

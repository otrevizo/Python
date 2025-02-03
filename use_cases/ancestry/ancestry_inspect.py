# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 08:50:19 2025

@author: otrevizo

This script connects to ancestry.db and prints out all table names.

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_inspect.py         # Print tables
│── ancestry_tests.py           # Unit tests for database functions
│── ancestry_export_xlsx.py     # Write db to Excel file

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

    tables = ["People", "Relationships"]
    for table in tables:
        show_table_contents(table)

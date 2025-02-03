# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:18:04 2025

@author: otrevizo

Export the ancestry.db into an Excel file.
The Excel file will have two sheets.
One sheet for People and one sheet for Relationships tables

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_inspect.py         # Print tables
│── ancestry_tests.py           # Unit tests for database functions
│── ancestry_export_xlsx.py     # Write db to Excel file


"""
import sqlite3
import pandas as pd

DB_NAME = "ancestry.db"
EXCEL_FILE = "ancestry_export.xlsx"

def export_to_excel():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    
    # Read data from tables
    people_df = pd.read_sql_query("SELECT * FROM People", conn)
    relationships_df = pd.read_sql_query("SELECT * FROM Relationships", conn)
    
    # Close the connection
    conn.close()
    
    # Write data to an Excel file
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        people_df.to_excel(writer, sheet_name="People", index=False)
        relationships_df.to_excel(writer, sheet_name="Relationships", index=False)
    
    print(f"Data exported successfully to {EXCEL_FILE}")

if __name__ == "__main__":
    export_to_excel()


# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:49:59 2025

@author: otrevizo

ancestry_main.py

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_inspect.py         # Print tables
│── ancestry_tests.py           # Unit tests for database functions
│── ancestry_export_xlsx.py     # Write db to Excel file

"""
import logging
from ancestry_db import AncestryDatabase

DB_NAME = "ancestry.db"
INPUT_FILE = "ancestry_input.xlsx"


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Establish database connection
db = AncestryDatabase()
db.connect()
db.create_tables()

# Main execution function
def main():
    try:
        df_people = db.read_input_file(INPUT_FILE)
        
        if df_people is not None:
            print("df_people columns:", df_people.columns)
            
            df_db_people = db.fetch_existing_data()
            
            changes_log = db.compare_and_update(df_people, df_db_people)
            
            if changes_log:
                print("Changes made:")
                for log in changes_log:
                    print(log)
            else:
                print("No changes detected.")
        
        db.archive_input_file(INPUT_FILE)
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:49:59 2025

@author: otrevizo

ancestry_get_input_xlsx.py

ancestry_project/
│── ancestry_db.py              # Handles database interactions (the class)
│── ancestry_get_input_xlsx.py  # Get ancestry_input.xlsx and update the db
│── ancestry_inspect.py         # Display table
│── ancestry_tests.py           # Adds records to the db, hardcoded, by hand
│── ancestry_export_xlsx.py     # Write db to Excel file
│── ancestry_family_tree.py     # Build the family tree (previous gens)

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
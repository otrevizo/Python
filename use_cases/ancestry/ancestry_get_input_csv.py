# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:04 2025

@author: otrevizo

ancestry_get_input_csv.py

ancestry_project/
│── ancestry_db.py              # Handles database interactions (the class)
│── ancestry_get_input_csv.py   # Get ancestry_input.csv and update the db
│── ancestry_inspect.py         # Display table
│── ancestry_tests.py           # Adds records to the db, hardcoded, by hand
│── ancestry_export_xlsx.py     # Write db to Excel file
│── ancestry_family_tree.py     # Build the family tree (previous gens)

"""

import logging
from ancestry_db import AncestryDatabase

# Configuration
DB_NAME = "ancestry.db"
INPUT_FILE = "ancestry_input.csv"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    """Main function to read CSV input, update the database, and archive the input file."""
    db = AncestryDatabase(db_name=DB_NAME)
    db.connect()
    db.create_tables()

    try:
        # Read the input CSV file
        df_people = db.read_csv_file(INPUT_FILE)
        
        if not df_people.empty:
            logging.info(f"CSV file '{INPUT_FILE}' loaded successfully.")
            
            # Fetch existing data from the database
            df_db_people = db.fetch_existing_data()
            
            # Compare and update the database with new records
            changes_log = db.compare_and_update(df_people, df_db_people)
            
            if changes_log:
                print("Changes made:")
                for log in changes_log:
                    print(log)
            else:
                print("No changes detected.")
            
            # Archive the input file after successful processing
            db.archive_file(INPUT_FILE)
        
        else:
            logging.warning("No data found in the input CSV file.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    finally:
        db.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()

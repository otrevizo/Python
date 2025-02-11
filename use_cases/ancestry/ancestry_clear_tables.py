# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:13:45 2025

@author: otrevizo

ancestry_project/
│── ancestry_db.py              # Handles database interactions (the class)
│── ancestry_get_input_xlsx.py  # Get ancestry_input.xlsx and update the db
│── ancestry_inspect.py         # Display table
│── ancestry_tests.py           # Adds records to the db, hardcoded, by hand
│── ancestry_export_xlsx.py     # Write db to Excel file
│── ancestry_family_tree.py     # Build the family tree (previous gens)

"""

import sqlite3
import logging

def clear_tables(db_name="ancestry.db"):
    """
    Clears all entries from the 'People' and 'Relationships' tables in the specified database.

    Args:
        db_name: The name of the database file. Defaults to "ancestry.db".
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Clear the 'People' table
        cursor.execute("DELETE FROM People")

        conn.commit()
        conn.close()
        logging.info("Tables cleared successfully.")

    except sqlite3.Error as e:
        logging.error(f"Error clearing tables: {e}")

if __name__ == "__main__":
    clear_tables()
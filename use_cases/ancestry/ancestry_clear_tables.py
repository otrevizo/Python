# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:13:45 2025

@author: otrevizo
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
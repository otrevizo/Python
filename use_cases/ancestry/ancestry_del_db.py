# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 15:34:21 2025

@author: trevizo
"""
import sqlite3
import os
import time

def delete_db(retries=3, delay=1):
  """
  Attempts to delete the ancestry.db file with retries.

  Args:
      retries: Number of retry attempts (default: 3).
      delay: Delay between retries in seconds (default: 1).
  """
  for attempt in range(retries):
    try:
      # Attempt to close any existing connections
      conn = sqlite3.connect("ancestry.db")
      conn.close()

      # Try to delete the file
      os.remove("ancestry.db")
      print("ancestry.db file deleted successfully.")
      return

    except sqlite3.Error as e:
      print(f"Error closing database connection: {e}")
    except FileNotFoundError:
      print("ancestry.db file not found.")
      return 
    except OSError as e:
      print(f"Error deleting ancestry.db file: {e}")

    if attempt < retries - 1:
      print(f"Retrying in {delay} seconds...")
      time.sleep(delay)

  print("Failed to delete ancestry.db file after multiple attempts.")

if __name__ == "__main__":
  delete_db()
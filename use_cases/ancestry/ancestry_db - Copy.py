# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:04 2025

@author: otrevizo
"""

# -*- coding: utf-8 -*-
"""
ancestry_db.py
Handles database interactions for the ancestry project.
"""
# -*- coding: utf-8 -*-
"""
ancestry_db.py
Handles database interactions for the ancestry project.
"""
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging
from typing import Optional, List, Tuple
from dateutil.parser import parse

class AncestryDatabase:
    """
    A class to interact with an SQLite3 database for ancestry data.
    """
    def __init__(self, db_name: str = "ancestry.db"):
        """Initializes the AncestryDatabase instance."""
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self):
        """Establish a connection to the database with Write-Ahead Logging (WAL) mode."""
        try:
            self.conn = sqlite3.connect(self.db_name, timeout=10)
            self.cursor = self.conn.cursor()  # Create the cursor here
            self.conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode for reduced locking
            logging.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")       

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logging.info("Database connection closed.")

    def ensure_connection(self):
        """Ensure that the database connection is established."""
        if not self.conn:
            self.connect()

    def create_tables(self) -> None:
        """Creates necessary tables if they do not exist."""
        self.ensure_connection()
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS People (
                    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    last_name TEXT NOT NULL,
                    maiden_name TEXT,
                    birth_date TEXT,
                    place_of_birth TEXT,
                    nationality TEXT,
                    father_id INTEGER,
                    mother_id INTEGER,
                    occupation TEXT,
                    residence TEXT,
                    death_date TEXT,
                    death_place TEXT,
                    cause_of_death TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(mother_id) REFERENCES People(person_id) ON DELETE SET NULL,
                    FOREIGN KEY(father_id) REFERENCES People(person_id) ON DELETE SET NULL
                )
            ''')
            self.conn.commit()
            logging.info("Tables created successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")

    def add_person(self, first_name: str, middle_name: str, last_name: str, 
                    birth_date: Optional[str] = None, place_of_birth: Optional[str] = None, 
                    nationality: Optional[str] = None, father_id: Optional[int] = None, 
                    mother_id: Optional[int] = None, occupation: Optional[str] = None, 
                    residence: Optional[str] = None, death_date: Optional[str] = None, 
                    death_place: Optional[str] = None, cause_of_death: Optional[str] = None, 
                    notes: Optional[str] = None) -> Optional[int]:
        """Adds a person to the People table and returns their ID."""
        try:
            self.cursor.execute('''
                INSERT INTO People (first_name, middle_name, last_name, birth_date, place_of_birth, 
                                      nationality, father_id, mother_id, occupation, residence, 
                                      death_date, death_place, cause_of_death, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, middle_name, last_name, birth_date, place_of_birth, nationality, 
                   father_id, mother_id, occupation, residence, death_date, death_place, 
                   cause_of_death, notes))
            self.conn.commit()
            logging.info(f"Person '{first_name} {middle_name} {last_name}' added successfully.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding person: {e}")
            return None    
    
        def fetch_existing_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
            """Fetch existing data from People table."""
            self.ensure_connection()
            df_people = pd.read_sql_query("SELECT * FROM People", self.conn)
            return df_people
    
        @staticmethod
        def parse_date(value: Optional[str]) -> Optional[str]:
            """
            Parses a value into a 'YYYY-MM-DD' date string if it's a valid date.
            Returns None for invalid or empty values.
            """
            if not value:
                return None
            try:
                date = parse(value, fuzzy=True)
                return date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                logging.warning(f"Could not parse date: {value}")
                return None
    
        @staticmethod
        def export_to_excel(db_name: str = "ancestry.db", excel_file: str = "ancestry_export.xlsx"):
            """Export the People table to an Excel file."""
            conn = sqlite3.connect(db_name)
            people_df = pd.read_sql_query("SELECT * FROM People", conn)
            conn.close()
            
            with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                people_df.to_excel(writer, sheet_name="People", index=False)
            logging.info(f"Data exported successfully to {excel_file}")
    
        @staticmethod
        def read_input_file(input_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
            """Reads input Excel file and returns People dataframe."""
            try:
                df_people = pd.read_excel(input_file, sheet_name="People")
                return df_people
            except Exception as e:
                logging.error(f"Error reading {input_file}: {e}")
                return pd.DataFrame(), pd.DataFrame()
    
        @staticmethod
        def archive_input_file(input_file: str) -> None:
            """Renames the input file with a timestamp after processing."""
            timestamp = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
            new_name = f"ancestry_digested_{timestamp}.xlsx"
            os.rename(input_file, new_name)
            logging.info(f"Renamed {input_file} to {new_name}")

    def fetch_existing_data(self):
        """Fetch existing data from People table."""
        self.connect()
        df_people = pd.read_sql_query("SELECT * FROM People", self.conn)
        self.close()
        return df_people
    
    def compare_and_update(self, 
                           df_people, 
                           df_db_people
                           ):
        """Compare and update the database based on differences in the input data."""
        self.connect()
        cursor = self.conn.cursor()
        changes_log = []
    
        # Process People sheet
        for _, row in df_people.iterrows():
            existing_person = df_db_people[df_db_people["person_id"] == row["person_id"]]
            if not existing_person.empty:
                # Check for changes in existing person
                if not existing_person.equals(pd.DataFrame([row])):
                    update_query = "UPDATE People SET "
                    update_values = []
                    for col in df_people.columns:
                        if existing_person[col].values[0] != row[col]:
                            update_query += f"{col}=?, "
                            update_values.append(row[col])
                    update_query = update_query[:-2] + f" WHERE person_id = {row['person_id']}"
                    cursor.execute(update_query, update_values)
                    changes_log.append(f"Updated Person: {row['person_id']}")
            else:
                # Add new person
                columns = ", ".join(row.keys())
                placeholders = ", ".join(["?"] * len(row))
                insert_query = f"INSERT INTO People ({columns}) VALUES ({placeholders})"
                cursor.execute(insert_query, tuple([x.item() if isinstance(x, np.ndarray) else x for x in row.values]))
                changes_log.append(f"Added Person: {row['person_id']}")
        
        self.conn.commit()
        self.close()
        return changes_log

    def get_person_by_id(self, person_id: int) -> Optional[Tuple]:
        """Retrieves a person by their ID."""
        self.cursor.execute('SELECT * FROM People WHERE person_id = ?', (person_id,))
        return self.cursor.fetchone()

    def get_ancestry(self, person_id: int) -> List[Tuple[int, str, str]]:
        """
        Retrieves the ancestry for a given person.
    
        Args:
            person_id (int): The ID of the person to retrieve ancestry for.
    
        Returns:
            List[Tuple[int, str, str]]: A list of tuples containing the person ID, name, and relationship.
        """
        ancestry = []
        to_process = [(person_id, 0)]  # Initialize list with person ID and generation
        while to_process:
            current_id, generation = to_process.pop(0)
            person = self.get_person_by_id(current_id)  # Pass current_id directly
            if person:
                name = f"{person[1]} {person[3]}"
                ancestry.append((current_id, name, f"Generation -{generation}"))
                # Get parents
                father_id, mother_id = person[8], person[9]
                if father_id:
                    to_process.append((father_id, generation + 1))
                if mother_id:
                    to_process.append((mother_id, generation + 1))
        return ancestry
    
    def get_family_tree(self, person_id: int, depth: int = 0, max_depth: int = 5, role: str = "Self", added_person_ids: Optional[set] = None) -> List[Tuple[int, str, str]]:
        if added_person_ids is None:
            added_person_ids = set()
        if person_id in added_person_ids or depth > max_depth:
            return []  # Prevent infinite recursion
        added_person_ids.add(person_id)
    
        family_tree = [(person_id, self.get_person_name(person_id), role)]
    
        # Fetch parents
        parents = self.get_parents(person_id)
        for parent_id, parent_name, parent_role in parents:
            if parent_id != person_id and parent_id not in added_person_ids:
                family_tree.extend(self.get_family_tree(parent_id, depth + 1, max_depth, parent_role, added_person_ids))
    
        # Fetch children
        children = self.get_children(person_id)
        for child_id, child_name, child_role in children:
            if child_id != person_id and child_id not in added_person_ids:
                family_tree.extend(self.get_family_tree(child_id, depth + 1, max_depth, child_role, added_person_ids))
    
        return family_tree

    def get_parents(self, person_id: int) -> List[Tuple[int, str, str]]:
        self.cursor.execute('''
            SELECT mother_id, father_id 
            FROM People 
            WHERE person_id = ?
        ''', (person_id,))
        parents = self.cursor.fetchone()
        result = []
        if parents:
            if parents[0]:
                result.append((parents[0], self.get_person_name(parents[0]), "Parent"))
            if parents[1]:
                result.append((parents[1], self.get_person_name(parents[1]), "Parent"))
        return result
    
    
    def get_children(self, person_id: int) -> List[Tuple[int, str, str]]:
        self.cursor.execute('''
            SELECT person_id 
            FROM People 
            WHERE mother_id = ? OR father_id = ?
        ''', (person_id, person_id))
        children = self.cursor.fetchall()
        return [(child[0], self.get_person_name(child[0]), "Child") for child in children]
    
    def get_person_name(self, person_id: int) -> str:
        """Helper method to get a person's full name by their ID."""
        self.cursor.execute('SELECT first_name, last_name FROM People WHERE person_id = ?', (person_id,))
        person = self.cursor.fetchone()
        return f"{person[0]} {person[1]}" if person else "Unknown"

    @staticmethod
    def export_to_excel(db_name: str = "ancestry.db", excel_file: str = "ancestry_export.xlsx"):
        """Export the People table to an Excel file."""
        conn = sqlite3.connect(db_name)
        people_df = pd.read_sql_query("SELECT * FROM People", conn)
        conn.close()

        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            people_df.to_excel(writer, sheet_name="People", index=False)
        print(f"Data exported successfully to {excel_file}")

    @staticmethod
    def parse_date(value: Optional[str]) -> Optional[str]:
        """
        Parses a value into a 'YYYY-MM-DD' date string if it's a valid date.
        Returns None for invalid or empty values.
        """
        if not value:
            return None
        try:
            date = parse(value, fuzzy=True)
            return date.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            logging.warning(f"Could not parse date: {value}")
            return None

    @staticmethod
    def read_input_file(input_file):
        INPUT_FILE = input_file
        try:
            df_people = pd.read_excel(INPUT_FILE, sheet_name="People")
            return df_people
        except Exception as e:
            print(f"Error reading {INPUT_FILE}: {e}")
            return None, None

    @staticmethod
    def archive_input_file(input_file):
        # Rename input file after processing
        INPUT_FILE = input_file
        timestamp = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        new_name = f"ancestry_digested_{timestamp}.xlsx"
        os.rename(INPUT_FILE, new_name)
        print(f"Renamed {INPUT_FILE} to {new_name}")


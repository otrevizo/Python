# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:04 2025

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
        """
        Creates necessary tables if they do not exist.
    
        This method creates the `People` table with structured fields for birth, death, and residence locations,
        including latitude and longitude for geospatial data.
        """
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
                    birth_city TEXT,
                    birth_state TEXT,
                    birth_country_code TEXT,  -- ISO 3166-1 Alpha-3 (e.g., USA, ITA)
                    birth_latitude REAL,
                    birth_longitude REAL,
                    death_date TEXT,
                    death_city TEXT,
                    death_state TEXT,
                    death_country_code TEXT,
                    death_latitude REAL,
                    death_longitude REAL,
                    nationality TEXT,
                    father_id INTEGER,
                    mother_id INTEGER,
                    occupation TEXT,
                    residence_street TEXT,
                    residence_city TEXT,
                    residence_state TEXT,
                    residence_country_code TEXT,
                    residence_latitude REAL,
                    residence_longitude REAL,
                    cause_of_death TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(mother_id) REFERENCES People(person_id) ON DELETE SET NULL,
                    FOREIGN KEY(father_id) REFERENCES People(person_id) ON DELETE SET NULL
                )
            ''')
            self.conn.commit()
            logging.info("Tables created successfully with structured location fields.")
        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")

    def add_person(self, first_name: str, middle_name: str, last_name: str, 
                   birth_date: Optional[str] = None, birth_city: Optional[str] = None, 
                   birth_state: Optional[str] = None, birth_country_code: Optional[str] = None, 
                   birth_latitude: Optional[float] = None, birth_longitude: Optional[float] = None, 
                   death_date: Optional[str] = None, death_city: Optional[str] = None, 
                   death_state: Optional[str] = None, death_country_code: Optional[str] = None,
                   death_latitude: Optional[float] = None, death_longitude: Optional[float] = None, 
                   nationality: Optional[str] = None, father_id: Optional[int] = None, 
                   mother_id: Optional[int] = None, occupation: Optional[str] = None, 
                   residence_street: Optional[str] = None, residence_city: Optional[str] = None, 
                   residence_state: Optional[str] = None, residence_country_code: Optional[str] = None, 
                   residence_latitude: Optional[float] = None, residence_longitude: Optional[float] = None,
                   cause_of_death: Optional[str] = None, notes: Optional[str] = None) -> Optional[int]:
        """
        Adds a new person to the `People` table with detailed location information.
    
        Args:
            first_name, middle_name, last_name: Personal details.
            birth_date, birth_city, birth_state, birth_country_code, birth_latitude, birth_longitude: Birth details.
            death_date, death_city, death_state, death_country_code, death_latitude, death_longitude: Death details.
            nationality: Nationality of the person.
            father_id, mother_id: Foreign keys for parents.
            occupation, residence details (street, city, state, country, latitude, longitude), cause_of_death, notes: Additional info.
    
        Returns:
            Optional[int]: The ID of the newly added person, or None if an error occurred.
        """
        try:
            self.cursor.execute('''
                INSERT INTO People (first_name, middle_name, last_name, birth_date, birth_city, birth_state, 
                                   birth_country_code, birth_latitude, birth_longitude, death_date, death_city, 
                                   death_state, death_country_code, death_latitude, death_longitude, nationality, 
                                   father_id, mother_id, occupation, residence_street, residence_city, 
                                   residence_state, residence_country_code, residence_latitude, residence_longitude, 
                                   cause_of_death, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, middle_name, last_name, birth_date, birth_city, birth_state, birth_country_code, 
                  birth_latitude, birth_longitude, death_date, death_city, death_state, death_country_code, 
                  death_latitude, death_longitude, nationality, father_id, mother_id, occupation, 
                  residence_street, residence_city, residence_state, residence_country_code, 
                  residence_latitude, residence_longitude, cause_of_death, notes))
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
    
    def compare_and_update(self, df_people, df_db_people):
        """
        Compares and updates the database based on differences in the input data.
        
        Args:
            df_people (DataFrame): Data from the input Excel file.
            df_db_people (DataFrame): Current database data for comparison.
    
        Returns:
            List[str]: A log of changes made to the database.
        """
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
                cursor.execute(insert_query, tuple(row.values))
                changes_log.append(f"Added Person: {row['person_id']}")
    
        self.conn.commit()
        self.close()
        return changes_log

    def get_person_by_id(self, person_id: int) -> Optional[Tuple]:
        """
        Retrieves a person by their ID, including all location details.
        
        Args:
            person_id (int): The ID of the person to retrieve.
        
        Returns:
            Optional[Tuple]: A tuple containing all person details or None if not found.
        """
        try:
            self.cursor.execute('''
                SELECT person_id, first_name, middle_name, last_name, maiden_name,
                       birth_date, birth_city, birth_state, birth_country_code, birth_latitude, birth_longitude,
                       death_date, death_city, death_state, death_country_code, death_latitude, death_longitude,
                       nationality, father_id, mother_id, occupation, 
                       residence_street, residence_city, residence_state, residence_country_code, 
                       residence_latitude, residence_longitude, cause_of_death, notes
                FROM People 
                WHERE person_id = ?
            ''', (person_id,))
            
            person = self.cursor.fetchone()
            return person if person else None
        except sqlite3.Error as e:
            logging.error(f"Error retrieving person with ID {person_id}: {e}")
            return None

    def get_ancestry(self, person_id: int) -> List[Tuple[int, str, str]]:
        """
        Retrieves the ancestry for a given person, sorted by generation.
        
        Args:
            person_id (int): The ID of the person to retrieve ancestry for.
        
        Returns:
            List[Tuple[int, str, str]]: A sorted list of tuples containing the person ID, name, and relationship.
        """
        def get_generation_label(generation: int) -> str:
            """Returns the appropriate label for the given generation."""
            if generation == 0:
                return "Yourself"
            elif generation == -1:
                return "Parent"
            elif generation == -2:
                return "Grandparent"
            elif generation == -3:
                return "Great-Grandparent"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs(generation + 2) % 10, "th")
                return f"{abs(generation + 2)}{suffix} Great-Grandparent"
    
        ancestry = []
        to_process = [(person_id, 0)]  # (person_id, generation)
    
        while to_process:
            current_id, generation = to_process.pop(0)
            person = self.get_person_by_id(current_id)
            if person:
                name = f"{person[1]} {person[3]}"  # Full name (first_name + last_name)
                relation = get_generation_label(generation)
                ancestry.append((current_id, name, relation, generation))
    
                # Add parents with generation decremented
                father_id, mother_id = person[18], person[19]
                if father_id:
                    to_process.append((father_id, generation - 1))
                if mother_id:
                    to_process.append((mother_id, generation - 1))
    
        # Sort ancestry by the generation (the last element in each tuple)
        ancestry.sort(key=lambda x: -x[3])
    
        # Remove the generation number before returning (to match the original format)
        return [(person_id, name, relation) for person_id, name, relation, _ in ancestry]

    
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

#    @staticmethod
    def read_csv_file(self, input_file: str) -> pd.DataFrame:
        """
        Reads the input CSV file and returns a pandas DataFrame.
        
        Args:
            input_file (str): Path to the input CSV file.
        
        Returns:
            pd.DataFrame: DataFrame with the contents of the CSV file.
        """
        try:
            df = pd.read_csv(input_file)
            logging.info(f"CSV file '{input_file}' read successfully.")
            return df
        except Exception as e:
            logging.error(f"Error reading CSV file '{input_file}': {e}")
            return pd.DataFrame()
    
#    @staticmethod
    def archive_file(self, input_file: str) -> None:
        """
        Renames the input file with a timestamp after processing.
        
        Args:
            input_file (str): Path to the input file.
        """
        try:
            base_name, ext = os.path.splitext(input_file)
            timestamp = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
            new_name = f"{base_name}_digested_{timestamp}{ext}"
            os.rename(input_file, new_name)
            logging.info(f"Renamed '{input_file}' to '{new_name}'.")
        except Exception as e:
            logging.error(f"Error archiving file '{input_file}': {e}")

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:04 2025

@author: trevizo
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
        """Connects to the SQLite database with Write-Ahead Logging mode to reduce locking issues."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.execute("PRAGMA journal_mode=WAL;")  # Enables WAL mode
            self.cursor = self.conn.cursor()
            logging.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
        

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
                    mother_id INTEGER,
                    father_id INTEGER,
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Relationships (
                    relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person1_id INTEGER,
                    person2_id INTEGER,
                    relationship_type TEXT,
                    UNIQUE(person1_id, person2_id, relationship_type),
                    FOREIGN KEY(person1_id) REFERENCES People(person_id) ON DELETE CASCADE,
                    FOREIGN KEY(person2_id) REFERENCES People(person_id) ON DELETE CASCADE
                )
            ''')
            self.conn.commit()
            logging.info("Tables created successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")

    def add_person(self, first_name: str, middle_name: str, last_name: str, 
                    birth_date: Optional[str] = None, place_of_birth: Optional[str] = None, 
                    nationality: Optional[str] = None, mother_id: Optional[int] = None, 
                    father_id: Optional[int] = None, occupation: Optional[str] = None, 
                    residence: Optional[str] = None, death_date: Optional[str] = None, 
                    death_place: Optional[str] = None, cause_of_death: Optional[str] = None, 
                    notes: Optional[str] = None) -> Optional[int]:
        """Adds a person to the People table and returns their ID."""
        try:
            self.cursor.execute('''
                INSERT INTO People (first_name, middle_name, last_name, birth_date, place_of_birth, 
                                      nationality, mother_id, father_id, occupation, residence, 
                                      death_date, death_place, cause_of_death, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, middle_name, last_name, birth_date, place_of_birth, nationality, 
                   mother_id, father_id, occupation, residence, death_date, death_place, 
                   cause_of_death, notes))
            self.conn.commit()
            logging.info(f"Person '{first_name} {middle_name} {last_name}' added successfully.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Error adding person: {e}")
            return None    
    def add_relationship(self, person1_id: int, person2_id: int, relationship_type: str) -> None:
        """Adds a relationship between two people."""
        try:
            self.cursor.execute('''
                INSERT INTO Relationships (person1_id, person2_id, relationship_type) 
                VALUES (?, ?, ?)
            ''', (person1_id, person2_id, relationship_type))
            self.conn.commit()
            logging.info(f"Relationship added successfully.")
        except sqlite3.IntegrityError:
            logging.warning("Duplicate relationship detected.")
        except sqlite3.Error as e:
            logging.error(f"Error adding relationship: {e}")

    def fetch_existing_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Fetch existing data from People and Relationships tables."""
        self.ensure_connection()
        df_people = pd.read_sql_query("SELECT * FROM People", self.conn)
        df_relationships = pd.read_sql_query("SELECT * FROM Relationships", self.conn)
        return df_people, df_relationships

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
        """Export the People and Relationships tables to an Excel file."""
        conn = sqlite3.connect(db_name)
        people_df = pd.read_sql_query("SELECT * FROM People", conn)
        relationships_df = pd.read_sql_query("SELECT * FROM Relationships", conn)
        conn.close()
        
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            people_df.to_excel(writer, sheet_name="People", index=False)
            relationships_df.to_excel(writer, sheet_name="Relationships", index=False)
        logging.info(f"Data exported successfully to {excel_file}")

    @staticmethod
    def read_input_file(input_file: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Reads input Excel file and returns People and Relationships dataframes."""
        try:
            df_people = pd.read_excel(input_file, sheet_name="People")
            df_relationships = pd.read_excel(input_file, sheet_name="Relationships")
            return df_people, df_relationships
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

    def add_relationship(self, person1_id: int, person2_id: int, relationship_type: str) -> None:
        """Adds a relationship between two people."""
        try:
            self.cursor.execute('''
                INSERT INTO Relationships (person1_id, person2_id, relationship_type) 
                VALUES (?, ?, ?)
            ''', (person1_id, person2_id, relationship_type))
            self.conn.commit()
            logging.info(f"Relationship '{relationship_type}' added between {person1_id} and {person2_id}.")
        except sqlite3.IntegrityError:
            logging.warning(f"Duplicate relationship: {person1_id} - {relationship_type} - {person2_id}.")
        except sqlite3.Error as e:
            logging.error(f"Error adding relationship: {e}")

    def fetch_existing_data(self):
        """Fetch existing data from People and Relationships tables."""
        self.connect()
        df_people = pd.read_sql_query("SELECT * FROM People", self.conn)
        df_relationships = pd.read_sql_query("SELECT * FROM Relationships", self.conn)
        self.close()
        return df_people, df_relationships
    
    def compare_and_update(self, df_people, df_relationships, df_db_people, df_db_relationships):
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
                cursor.execute(
                    "INSERT INTO People (person_id, name, birthdate) VALUES (?, ?, ?)",
                    (row["person_id"], row["name"], row["birthdate"]),
                )
                changes_log.append(f"Added Person: {row['person_id']}")

        # Process Relationships sheet
        for _, row in df_relationships.iterrows():
            existing_relationship = df_db_relationships[(df_db_relationships["person1_id"] == row["person1_id"]) & 
                                                     (df_db_relationships["person2_id"] == row["person2_id"]) &
                                                     (df_db_relationships["relationship_type"] == row["relationship_type"])]
            if not existing_relationship.empty:
                # Relationship exists, check for changes (currently not implemented)
                # ... (Add logic to check and update relationship attributes if needed) ...
                pass 
            else:
                # Add new relationship
                cursor.execute(
                    "INSERT INTO Relationships (person1_id, person2_id, relationship_type) VALUES (?, ?, ?)",
                    (row["person1_id"], row["person2_id"], row["relationship_type"])
                )
                changes_log.append(f"Added Relationship: {row['person1_id']} - {row['relationship_type']} - {row['person2_id']}")

        self.conn.commit()
        self.close()
        return changes_log

    def get_person_by_id(self, person_id: int) -> Optional[Tuple]:
        """Retrieves a person by their ID."""
        self.cursor.execute('SELECT * FROM People WHERE person_id = ?', (person_id,))
        return self.cursor.fetchone()

    def get_family_tree(self, person_id: int) -> List[Tuple[int, str, str, str]]:
        """Retrieves all relationships for a given person."""
        self.cursor.execute('''
            SELECT p2.person_id, p2.first_name, p2.last_name, r.relationship_type 
            FROM Relationships r
            JOIN People p2 ON r.person2_id = p2.person_id
            WHERE r.person1_id = ?
        ''', (person_id,))
        return self.cursor.fetchall()

    @staticmethod
    def export_to_excel(db_name: str = "ancestry.db", excel_file: str = "ancestry_export.xlsx"):
        """Export the People and Relationships tables to an Excel file."""
        conn = sqlite3.connect(db_name)
        people_df = pd.read_sql_query("SELECT * FROM People", conn)
        relationships_df = pd.read_sql_query("SELECT * FROM Relationships", conn)
        conn.close()

        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            people_df.to_excel(writer, sheet_name="People", index=False)
            relationships_df.to_excel(writer, sheet_name="Relationships", index=False)
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
            df_relationships = pd.read_excel(INPUT_FILE, sheet_name="Relationships")
            return df_people, df_relationships
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


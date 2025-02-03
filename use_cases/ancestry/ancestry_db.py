# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 08:39:38 2025

@author: trevizo

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_models.py          # Defines data structures (Person, Relationship)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_tests.py           # Unit tests for database functions

"""

import sqlite3
import logging
from typing import Optional, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class AncestryDatabase:
    """
    A class to interact with an SQLite3 database for ancestry data.
    """

    def __init__(self, db_name: str = "ancestry.db"):
        """
        Initializes the AncestryDatabase instance.
        """
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """
        Establishes a connection to the database.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")

    def close(self) -> None:
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()
            logging.info("Database connection closed.")

    def create_tables(self) -> None:
        """
        Creates necessary tables if they do not exist.
        """
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS People (
                    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    middle_initial TEXT,
                    last_name TEXT NOT NULL,
                    mainden_name TEXT,
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

            self.cursor.execute('''
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
            logging.info("Tables created successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")

    def add_person(self, first_name: str, middle_initial: Optional[str], last_name: str, birth_date: Optional[str],
                   place_of_birth: Optional[str], nationality: Optional[str], mother_id: Optional[int],
                   father_id: Optional[int], occupation: Optional[str], residence: Optional[str],
                   death_date: Optional[str], death_place: Optional[str], cause_of_death: Optional[str],
                   notes: Optional[str]) -> Optional[int]:
        """
        Adds a person to the People table.
        """
        try:
            self.cursor.execute('''
                INSERT INTO People (first_name, middle_initial, last_name, birth_date, place_of_birth, nationality, 
                                   mother_id, father_id, occupation, residence, death_date, death_place, 
                                   cause_of_death, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, middle_initial, last_name, birth_date, place_of_birth, nationality, mother_id,
                  father_id, occupation, residence, death_date, death_place, cause_of_death, notes))
            self.conn.commit()
            person_id = self.cursor.lastrowid
            logging.info(f"Person '{first_name} {last_name}' added with ID {person_id}.")
            return person_id
        except sqlite3.Error as e:
            logging.error(f"Error adding person: {e}")
            return None

    def add_relationship(self, person1_id: int, person2_id: int, relationship_type: str) -> None:
        """
        Adds a relationship between two people.
        """
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

    def get_person_by_id(self, person_id: int) -> Optional[Tuple]:
        """
        Retrieves a person by their ID.
        """
        self.cursor.execute('SELECT * FROM People WHERE person_id = ?', (person_id,))
        return self.cursor.fetchone()

    def get_family_tree(self, person_id: int) -> List[Tuple[int, str, str, str]]:
        """
        Retrieves all relationships for a given person.
        """
        self.cursor.execute('''
            SELECT p2.person_id, p2.first_name, p2.last_name, r.relationship_type 
            FROM Relationships r
            JOIN People p2 ON r.person2_id = p2.person_id
            WHERE r.person1_id = ?
        ''', (person_id,))
        return self.cursor.fetchall()

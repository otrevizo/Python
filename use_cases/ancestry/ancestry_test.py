# -*- coding: utf-8 -*-
"""
Created on Mon Feb  10 09:35:06 2025

@author: otrevizo

Unit test script to populate the database with sample ancestry data.

ancestry_project/
│── ancestry_db.py              # Handles database interactions
│── ancestry_main.py            # Entry point for running operations
│── ancestry_inspect.py         # Print tables
│── ancestry_tests.py           # Unit tests for database functions
│── ancestry_export_xlsx.py     # Write db to Excel file
"""

import logging
from ancestry_db import AncestryDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize and set up database
db = AncestryDatabase()
db.connect()
db.create_tables()

# --- Main Couple ---
antonio_veneziano = db.add_person(
    first_name="Antonio",
    middle_name=None,
    last_name="Veneziano",
    birth_date="1935-05-22",
    birth_city="Philadelphia",
    birth_state="PA",
    birth_country_code="USA",
    birth_latitude=39.9526,
    birth_longitude=-75.1652,
    nationality="Italian-American",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street="123 Main St",
    residence_city="Philadelphia",
    residence_state="PA",
    residence_country_code="USA",
    residence_latitude=39.9526,
    residence_longitude=-75.1652,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

maria_mancini = db.add_person(
    first_name="Maria",
    middle_name=None,
    last_name="Mancini",
    birth_date="1937-11-09",
    birth_city="New York",
    birth_state="NY",
    birth_country_code="USA",
    birth_latitude=40.7128,
    birth_longitude=-74.0060,
    nationality="Italian-American",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street="456 Park Ave",
    residence_city="New York",
    residence_state="NY",
    residence_country_code="USA",
    residence_latitude=40.7128,
    residence_longitude=-74.0060,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

# --- Parents of Antonio and Maria ---
paolo_veneziano = db.add_person(
    first_name="Paolo",
    middle_name=None,
    last_name="Veneziano",
    birth_date="1905-08-20",
    birth_city="Rome",
    birth_state=None,
    birth_country_code="ITA",
    birth_latitude=41.9028,
    birth_longitude=12.4964,
    nationality="Italian",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street=None,
    residence_city="Rome",
    residence_state=None,
    residence_country_code="ITA",
    residence_latitude=41.9028,
    residence_longitude=12.4964,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

rosa_conti = db.add_person(
    first_name="Rosa",
    middle_name=None,
    last_name="Conti",
    birth_date="1908-04-10",
    birth_city="Naples",
    birth_state=None,
    birth_country_code="ITA",
    birth_latitude=40.8518,
    birth_longitude=14.2681,
    nationality="Italian",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street=None,
    residence_city="Naples",
    residence_state=None,
    residence_country_code="ITA",
    residence_latitude=40.8518,
    residence_longitude=14.2681,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

# --- Grandparents ---
giovanni_veneziano = db.add_person(
    first_name="Giovanni",
    middle_name=None,
    last_name="Veneziano",
    birth_date="1880-06-15",
    birth_city="Florence",
    birth_state=None,
    birth_country_code="ITA",
    birth_latitude=43.7696,
    birth_longitude=11.2558,
    nationality="Italian",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street=None,
    residence_city="Florence",
    residence_state=None,
    residence_country_code="ITA",
    residence_latitude=43.7696,
    residence_longitude=11.2558,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

anna_russo = db.add_person(
    first_name="Anna",
    middle_name=None,
    last_name="Russo",
    birth_date="1882-09-21",
    birth_city="Milan",
    birth_state=None,
    birth_country_code="ITA",
    birth_latitude=45.4642,
    birth_longitude=9.1900,
    nationality="Italian",
    father_id=None,
    mother_id=None,
    occupation=None,
    residence_street=None,
    residence_city="Milan",
    residence_state=None,
    residence_country_code="ITA",
    residence_latitude=45.4642,
    residence_longitude=9.1900,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

# --- Children ---
lucia_veneziano = db.add_person(
    first_name="Lucia",
    middle_name=None,
    last_name="Veneziano",
    birth_date="1960-07-15",
    birth_city="Philadelphia",
    birth_state="PA",
    birth_country_code="USA",
    birth_latitude=39.9526,
    birth_longitude=-75.1652,
    nationality="Italian-American",
    father_id=antonio_veneziano,
    mother_id=maria_mancini,
    occupation=None,
    residence_street=None,
    residence_city="Philadelphia",
    residence_state="PA",
    residence_country_code="USA",
    residence_latitude=39.9526,
    residence_longitude=-75.1652,
    death_date=None,
    death_city=None,
    death_state=None,
    death_country_code=None,
    death_latitude=None,
    death_longitude=None,
    cause_of_death=None,
    notes=None
)

# Confirm database initialization
logging.info("Test database populated successfully.")
db.close()

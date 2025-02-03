# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:17:06 2025

@author: trevizo
"""

import logging
from ancestry_db import AncestryDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

db = AncestryDatabase()
db.connect()
db.create_tables()

# --- Main Couple ---
antonio_veneziano = db.add_person(
    "Antonio", 
    None,  
    "Veneziano", 
    "1935-05-22",  
    "Philadelphia",  
    "Italian-American",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
maria_mancini = db.add_person(
    "Maria", 
    None,  
    "Mancini", 
    "1937-11-09",  
    "New York City",  
    "Italian-American",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
db.add_relationship(antonio_veneziano, maria_mancini, "spouse")

# --- Parents of Antonio and Maria ---
paolo_veneziano = db.add_person(
    "Paolo", 
    None,  
    "Veneziano", 
    "1905-08-20",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
rosa_conti = db.add_person(
    "Rosa", 
    None,  
    "Conti", 
    "1908-04-10",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
angelo_mancini = db.add_person(
    "Angelo", 
    None,  
    "Mancini", 
    "1906-12-05",  
    "USA",  
    "Italian-American",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
teresa_ricci = db.add_person(
    "Teresa", 
    None,  
    "Ricci", 
    "1909-09-14",  
    "USA",  
    "Italian-American",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)

# Add relationships between parents
db.add_relationship(paolo_veneziano, rosa_conti, "spouse")
db.add_relationship(angelo_mancini, teresa_ricci, "spouse")
db.add_relationship(paolo_veneziano, antonio_veneziano, "parent")
db.add_relationship(rosa_conti, antonio_veneziano, "parent")
db.add_relationship(angelo_mancini, maria_mancini, "parent")
db.add_relationship(teresa_ricci, maria_mancini, "parent")

# --- Grandparents ---
giovanni_veneziano = db.add_person(
    "Giovanni", 
    None,  
    "Veneziano", 
    "1880-06-15",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes
)
anna_russo = db.add_person(
    "Anna", 
    None,  
    "Russo", 
    "1882-09-21",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
giuseppe_mancini = db.add_person(
    "Giuseppe", 
    None,  
    "Mancini", 
    "1878-11-03",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
luisa_ferrara = db.add_person(
    "Luisa", 
    None,  
    "Ferrara", 
    "1881-07-12",  
    "USA",  
    "American",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
marco_ricci = db.add_person(
    "Marco", 
    None,  
    "Ricci", 
    "1879-05-30",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
caterina_bianchi = db.add_person(
    "Caterina", 
    None,  
    "Bianchi", 
    "1883-02-17",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
francesco_conti = db.add_person(
    "Francesco", 
    None,  
    "Conti", 
    "1885-01-20",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
elisabetta_rosati = db.add_person(
    "Elisabetta", 
    None,  
    "Rosati", 
    "1887-06-10",  
    "Italy",  
    "Italian",  
    None,  # mother_id
    None,  # father_id
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)

# Add relationships between grandparents
db.add_relationship(giovanni_veneziano, anna_russo, "spouse")
db.add_relationship(giuseppe_mancini, luisa_ferrara, "spouse")
db.add_relationship(marco_ricci, caterina_bianchi, "spouse")
db.add_relationship(francesco_conti, elisabetta_rosati, "spouse")
db.add_relationship(giovanni_veneziano, paolo_veneziano, "parent")
db.add_relationship(anna_russo, paolo_veneziano, "parent")
db.add_relationship(francesco_conti, rosa_conti, "parent")
db.add_relationship(elisabetta_rosati, rosa_conti, "parent")
db.add_relationship(giuseppe_mancini, angelo_mancini, "parent")
db.add_relationship(luisa_ferrara, angelo_mancini, "parent")
db.add_relationship(marco_ricci, teresa_ricci, "parent")
db.add_relationship(caterina_bianchi, teresa_ricci, "parent")

# --- Children ---
lucia_veneziano = db.add_person(
    "Lucia", 
    None,  
    "Veneziano", 
    "1960-07-15",  
    "Philadelphia",  
    "Italian-American",  
    antonio_veneziano,  
    maria_mancini,  
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
gianna_veneziano = db.add_person(
    "Gianna", 
    None,  
    "Veneziano", 
    "1963-04-25",  
    "Philadelphia",  
    "Italian-American",  
    antonio_veneziano,  
    maria_mancini,  
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)
marco_veneziano = db.add_person(
    "Marco", 
    None,  
    "Veneziano", 
    "1966-09-10",  
    "Philadelphia",  
    "Italian-American",  
    antonio_veneziano,  
    maria_mancini,  
    None,  # occupation
    None,  # residence
    None,  # death_date
    None,  # death_place
    None,  # cause_of_death
    None   # notes  
)

# Add relationships between children and parents
db.add_relationship(antonio_veneziano, lucia_veneziano, "parent")
db.add_relationship(maria_mancini, lucia_veneziano, "parent")
db.add_relationship(antonio_veneziano, gianna_veneziano, "parent")
db.add_relationship(maria_mancini, gianna_veneziano, "parent")
db.add_relationship(antonio_veneziano, marco_veneziano, "parent")
db.add_relationship(maria_mancini, marco_veneziano, "parent")



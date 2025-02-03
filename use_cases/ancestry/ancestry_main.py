# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 08:43:10 2025

@author: trevizo

ancestry_project/
│── ancestry_db.py              # Handles database interactions (this class)
│── ancestry_models.py          # Defines data structures (Person, Relationship)
│── ancestry_main.py            # Entry point for running operations
│── ancestry_tests.py           # Unit tests for database functions

"""

from ancestry_db import AncestryDatabase

if __name__ == "__main__":
    db = AncestryDatabase()
    db.connect()
    db.create_tables()

    # Adding sample people
    john_id = db.add_person("John", "Doe", "1980-01-15")
    jane_id = db.add_person("Jane", "Doe", "1982-05-20")
    alice_id = db.add_person("Alice", "Doe", "2005-06-10")

    # Adding relationships
    db.add_relationship(john_id, jane_id, "spouse")
    db.add_relationship(john_id, alice_id, "parent")
    db.add_relationship(jane_id, alice_id, "parent")

    # Fetching person
    person = db.get_person_by_id(alice_id)
    print(f"Retrieved Person: {person}")

    # Fetching family tree
    tree = db.get_family_tree(john_id)
    print("John's Family Tree:")
    for member in tree:
        print(member)

    db.close()

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:56:21 2025

@author: otrevizo

ancestry_family_tree.py

Prompts the user for a person_id and prints the family tree using get_family_tree() from ancestry_db.py
"""

from ancestry_db import AncestryDatabase

def main():
    # Initialize database
    db = AncestryDatabase()
    db.connect()

    try:
        person_id = input("Enter the person_id to retrieve the family tree: ").strip()
        
        if not person_id.isdigit():
            print("Invalid input. Please enter a valid integer for person_id.")
            return
        
        person_id = int(person_id)
        family_tree = db.get_family_tree(person_id)
        
        if family_tree:
            print("\nFamily Tree:")
            for member in family_tree:
                print(f"ID: {member[0]}, Name: {member[1]}, Relation: {member[2]}")
        else:
            print("No family tree found for the given person_id.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
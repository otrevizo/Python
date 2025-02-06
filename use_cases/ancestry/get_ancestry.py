# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:47:27 2025

@author: otrevizo

get_ancestry.py

Retrieves parent, grandparents, great grandparents... etc... past generations

"""

# get_ancestry.py

from ancestry_db import AncestryDatabase

def main():
    # Initialize database
    db = AncestryDatabase()
    db.connect()

    try:
        person_id = input("Enter the person_id to retrieve their ancestry: ").strip()
        
        if not person_id.isdigit():
            print("Invalid input. Please enter a valid integer for person_id.")
            return
        
        person_id = int(person_id)
        ancestry = db.get_ancestry(person_id)
        
        if ancestry:
            print("\nAncestry:")
            for person in ancestry:
                print(f"ID: {person[0]}, Name: {person[1]}, Relation: {person[2]}")
        else:
            print("No ancestry found for the given person_id.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
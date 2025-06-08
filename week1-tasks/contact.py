#!/usr/bin/env python3
"""
Contact Management System (CLI) using Python.

Features:
- Add contacts
- Search contacts by name
- Update contact information
- Data persistence using JSON file
- Input validation and error handling

Run the script and follow the menu prompts.
"""

import json
import os
import re
import sys

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Load contacts from the JSON file. Return a dict."""
    if not os.path.exists(CONTACTS_FILE):
        return {}
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                print("Warning: Invalid contacts file format. Starting fresh.")
                return {}
            return data
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read contacts file or file is corrupted. Starting fresh.")
        return {}

def save_contacts(contacts):
    """Save contacts dictionary to the JSON file."""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
    except IOError:
        print("Error: Unable to save contacts to file.")

def is_valid_email(email):
    """Simple regex to validate an email address."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def get_non_empty_input(prompt):
    """Prompt user until they enter a non-empty input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.")

def add_contact(contacts):
    print("\n--- Add Contact ---")
    name = get_non_empty_input("Enter contact name: ")
    if name in contacts:
        print(f"Contact '{name}' already exists.")
        return
    phone = input("Enter phone number (optional): ").strip()
    email = input("Enter email (optional): ").strip()
    if email and not is_valid_email(email):
        print("Invalid email format. Email will be skipped.")
        email = ""
    contacts[name] = {
        "phone": phone,
        "email": email
    }
    save_contacts(contacts)
    print(f"Contact '{name}' added successfully.")

def search_contacts(contacts):
    print("\n--- Search Contacts ---")
    query = get_non_empty_input("Enter name or part of name to search: ").lower()
    results = {name: info for name, info in contacts.items() if query in name.lower()}
    if not results:
        print("No contacts found matching that name.")
        return
    print(f"\nFound {len(results)} contact(s):")
    for name, info in sorted(results.items()):
        phone = info.get("phone") or "N/A"
        email = info.get("email") or "N/A"
        print(f"- {name}\n  Phone: {phone}\n  Email: {email}")

def update_contact(contacts):
    print("\n--- Update Contact ---")
    name = get_non_empty_input("Enter the exact contact name to update: ")
    if name not in contacts:
        print(f"No contact found with the name '{name}'.")
        return
    current = contacts[name]
    print(f"Current phone: {current.get('phone') or '(none)'}")
    new_phone = input("Enter new phone number (leave blank to keep current): ").strip()
    if new_phone:
        current['phone'] = new_phone
    print(f"Current email: {current.get('email') or '(none)'}")
    new_email = input("Enter new email (leave blank to keep current): ").strip()
    if new_email:
        if is_valid_email(new_email):
            current['email'] = new_email
        else:
            print("Invalid email format. Email not updated.")
    contacts[name] = current
    save_contacts(contacts)
    print(f"Contact '{name}' updated successfully.")

def main_menu():
    contacts = load_contacts()
    menu = """
Contact Management System
=========================
1. Add Contact
2. Search Contacts
3. Update Contact
4. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contacts(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please select a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()


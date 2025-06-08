#!/usr/bin/env python3
import json
import os
import re

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return {}
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read contacts file or file is corrupted. Starting with empty contacts.")
        return {}

def save_contacts(contacts):
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2)
    except IOError:
        print("Error: Unable to save contacts to file.")

def is_valid_email(email):
    # Simple regex for email validation
    pattern = r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
    return re.match(pattern, email) is not None

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.")

def add_contact(contacts):
    print("\n--- Add Contact ---")
    name = get_non_empty_input("Enter name: ")
    if name in contacts:
        print(f"Contact '{name}' already exists.")
        return
    phone = input("Enter phone number (optional): ").strip()
    email = input("Enter email (optional): ").strip()
    if email and not is_valid_email(email):
        print("Invalid email format. Skipping email.")
        email = ""
    contacts[name] = {
        "phone": phone,
        "email": email
    }
    save_contacts(contacts)
    print(f"Contact '{name}' added successfully.")

def search_contacts(contacts):
    print("\n--- Search Contacts ---")
    query = get_non_empty_input("Enter name to search: ").lower()
    results = {name: info for name, info in contacts.items() if query in name.lower()}
    if not results:
        print("No contacts found matching that name.")
        return
    print(f"\nFound {len(results)} contact(s):")
    for name, info in results.items():
        phone = info.get("phone", "")
        email = info.get("email", "")
        print(f"- {name}\n  Phone: {phone or 'N/A'}\n  Email: {email or 'N/A'}")

def update_contact(contacts):
    print("\n--- Update Contact ---")
    name = get_non_empty_input("Enter the exact contact name to update: ")
    if name not in contacts:
        print(f"No contact found with the name '{name}'.")
        return
    contact = contacts[name]
    print(f"Current phone: {contact.get('phone', '')}")
    new_phone = input("Enter new phone number (leave blank to keep current): ").strip()
    if new_phone:
        contact['phone'] = new_phone
    print(f"Current email: {contact.get('email', '')}")
    new_email = input("Enter new email (leave blank to keep current): ").strip()
    if new_email:
        if is_valid_email(new_email):
            contact['email'] = new_email
        else:
            print("Invalid email format. Email not updated.")
    contacts[name] = contact
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
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contacts(contacts)
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please select 1-4.")

if __name__ == "__main__":
    main_menu()


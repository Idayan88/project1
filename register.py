import json
import os

JSON_FILE = 'users.json'

def initialize_json_file():
    """Ensure users.json exists; if not, create it with an empty list."""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as file:
            json.dump([], file)

def read_users():
    """Read and return all users from users.json."""
    with open(JSON_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_users(users):
    """Write the list of users back to users.json."""
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def add_user(username, password):
    """Add a new user to users.json."""
    users = read_users()
    if any(user.get('username') == username for user in users):
        raise ValueError("User with this username already exists.")
    
    new_user = {"username": username, "password": password}
    users.append(new_user)
    write_users(users)
    return new_user
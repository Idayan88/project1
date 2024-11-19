import json
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key_here'  # Use a secure random key in production

# Path to the JSON file where user data will be stored
users_file_path = 'users.json'

# Load existing users data from the JSON file (if it exists)
def load_users():
    try:
        with open(users_file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Write user data to the JSON file
def save_users(users):
    try:
        with open(users_file_path, 'w') as file:
            json.dump(users, file, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")

# Route to serve the registration page (HTML form)
@app.route('/')
def index():
    # Check if the user is logged in by checking the session
    if 'username' in session:
        return f"Welcome, {session['username']}! <br><a href='/logout'>Logout</a>"
    return render_template('index.html')  # If not logged in, show the login/register form

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Validate the input
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Load existing users
    users = load_users()

    # Check if the username already exists
    if username in users:
        return jsonify({'error': 'Username already taken'}), 400

    # Add the new user to the users dictionary
    users[username] = password

    # Save the updated users dictionary to the JSON file
    save_users(users)

    return jsonify({'message': 'User registered successfully!'})

# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Validate the input
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Load existing users
    users = load_users()

    # Check if the username exists and if the password matches
    if username not in users:
        return jsonify({'error': 'Username not found'}), 404

    if users[username] != password:
        return jsonify({'error': 'Incorrect password'}), 403

    # Set the session variable for the logged-in user
    session['username'] = username

    return jsonify({'message': 'Login successful!'})

# Route to handle user logout
@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    return redirect(url_for('index'))  # Redirect to the homepage

if __name__ == '__main__':
    app.run(debug=True)

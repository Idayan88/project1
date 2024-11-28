from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return []


# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        users = load_users()
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            session["user"] = username
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        users = load_users()
        if any(u['username'] == username for u in users):
            return jsonify({"message": "Username already exists!"}), 409

        users.append({"username": username, "password": password})
        save_users(users)
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']}! <a href='/logout'>Logout</a>"
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

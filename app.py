from flask import Flask, render_template , jsonify, request
from register import initialize_json_file, add_user

app = Flask(__name__)
# Initialize the JSON file when the server starts
initialize_json_file()

@app.route('/register', methods=['POST'])
def register_user():
    """Endpoint to register a new user."""
    try:
        # קבלת הנתונים מהבקשה בפורמט JSON
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Invalid data format"}), 400
        
        username = data['username']
        password = data['password']
        
        # הוספת המשתמש החדש
        new_user = add_user(username, password)
        return jsonify({"message": "User registered successfully", "user": new_user}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def register():
    return render_template('register.html')

@app.route('/<filename>')
def file(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
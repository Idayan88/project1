from flask import Blueprint, request, jsonify
import json
import os

main = Blueprint('main', __name__)


# Endpoint להוספת דומיין בודד
@main.route('/add_domain', methods=['POST'])
def add_domain():
    data = request.get_json()
    domain = data.get('domain')
    username = 'example_user'  # שים כאן את שם המשתמש הנוכחי

    if not domain:
        return jsonify({"status": "Error", "message": "No domain provided"}), 400

    # יצירת נתיב קובץ הדומיינים
    file_path = f"{username}_domains.json"

    # אם הקובץ קיים, טוענים את הדומיינים הקיימים
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            domains_data = json.load(f)
    else:
        domains_data = []

    # הוספת הדומיין החדש
    new_domain = {
        "domain": domain,
        "status": "Pending",
        "ssl_expiration": "N/A",
        "ssl_issuer": "N/A"
    }
    domains_data.append(new_domain)

    # שמירה לקובץ
    with open(file_path, 'w') as f:
        json.dump(domains_data, f, indent=4)

    return jsonify({"status": "Success", "message": "Domain added successfully"}), 200


# Endpoint להעלאת קובץ דומיינים (Bulk Upload)
@main.route('/bulk_upload', methods=['POST'])
def bulk_upload():
    # בדיקה אם קובץ נשלח בבקשה
    if 'file' not in request.files:
        return jsonify({"status": "Error", "message": "No file part"}), 400
    
    file = request.files['file']
    
    # בדיקה אם שם הקובץ לא ריק
    if file.filename == '':
        return jsonify({"status": "Error", "message": "No selected file"}), 400
    
    # בדיקה אם הקובץ הוא קובץ .txt
    if not file.filename.endswith('.txt'):
        return jsonify({"status": "Error", "message": "Invalid file format. Please upload a .txt file."}), 400

    # קריאת התוכן של הקובץ
    domains = file.read().decode('utf-8').splitlines()
    
    # קביעת שם הקובץ עבור הדומיינים
    username = 'example_user'  # כאן עליך לשים את שם המשתמש הנוכחי
    file_path = f"{username}_domains.json"

    try:
        # קריאה של הדומיינים הקיימים בקובץ (אם קיים)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                domains_data = json.load(f)
        else:
            domains_data = []
        
        # הוספת כל דומיין שנמצא בקובץ
        for domain in domains:
            if not domain:
                continue
            # יצירת רשומה חדשה לכל דומיין
            new_domain = {
                "domain": domain,
                "status": "Pending",
                "ssl_expiration": "N/A",
                "ssl_issuer": "N/A"
            }
            domains_data.append(new_domain)
        
        # שמירה של הדומיינים החדשים בקובץ
        with open(file_path, 'w') as f:
            json.dump(domains_data, f, indent=4)

        return jsonify({"status": "Success", "message": "Bulk upload successful"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": f"An error occurred: {str(e)}"}), 500

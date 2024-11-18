from flask import Flask
from .routes import main  # ייבוא של ה-Blueprint

def create_app():
    app = Flask(__name__)  # יצירת אפליקציה חדשה
    app.register_blueprint(main)  # רישום ה-Blueprint של הנתיבים
    return app

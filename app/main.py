from app import create_app

app = create_app()

if __name__ == '__main__':
    print(app.url_map)  # הדפסת כל הנתיבים המוגדרים באפליקציה
    app.run(debug=True)  # הפעלת השרת על פורט 5000

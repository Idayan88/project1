document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // מניעת שליחה רגילה של הטופס

    // איסוף נתוני הטופס
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // הכנת הנתונים כ-JSON
    const data = { username, password };

    try {
        // שליחת הנתונים לשרת Flask
        const response = await fetch('http://127.0.0.1:8080/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // טיפול בתשובה מהשרת
        const messge = document.getElementById('messge');
        const result = await response.json();
        if (response.ok) {
            messge.textContent = result.message;
            messge.style.color = 'green';; // הודעת הצלחה
        } else {
            messge.textContent = result.error;
            messge.style.color = 'red'; // הודעת שגיאה
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to the server.');
    }
});
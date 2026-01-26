from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="mysql",      # use "localhost" if not using Docker
        user="root",
        password="root",
        database="school"
    )

# Create database & table
def init_db():
    conn = mysql.connector.connect(
        host="mysql",      # use "localhost" if not using Docker
        user="root",
        password="root"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS school")
    cursor.execute("USE school")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            age INT NOT NULL,
            course VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    course = request.form['course']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, age, course) VALUES (%s, %s, %s, %s)",
        (name, email, age, course)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('welcome.html', name=name)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

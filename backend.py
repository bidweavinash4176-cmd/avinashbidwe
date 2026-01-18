from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="host.docker.internal", # Special address to access host's local MySQL
        user="root",
        password="@Abcd$4176",
        database="school"
    )

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
    cursor.execute("INSERT INTO students (name, email, age, course) VALUES (%s, %s, %s , %s)", (name, email, age, course))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

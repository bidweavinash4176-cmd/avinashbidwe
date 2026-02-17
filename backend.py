from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecret"

# ----------------------------
# KEYCLOAK CONFIG
# ----------------------------
oauth = OAuth(app)

keycloak = oauth.register(
    name='keycloak',
    client_id='flask-app',
    client_secret='EHLcKiBWTaXUjZeGbfwyzHUK0ritiEDo',
    server_metadata_url='http://keycloak:8080/realms/flask-realm/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email'
    }
)

# ----------------------------
# AUTH ROUTES
# ----------------------------

@app.route("/")
def home():
    if 'user' not in session:
        return redirect("/login")

    return render_template("index.html", user=session['user'])


@app.route("/login")
def login():
    return keycloak.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )




@app.route("/callback")
def callback():
    token = keycloak.authorize_access_token()

    print("\n========== TOKEN OBJECT ==========")
    print(token)

    print("\n========== ACCESS TOKEN ==========")
    print(token["access_token"])

    print("\n========== ID TOKEN ==========")
    print(token["id_token"])

    session['user'] = token["userinfo"]

    return redirect("/")









@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ----------------------------
# DATABASE
# ----------------------------

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="school"
    )


def init_db():
    conn = mysql.connector.connect(
        host="mysql",
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
            email VARCHAR(100) NOT NULL ,
            age INT NOT NULL,
            course VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------
# PROTECTED SUBMIT ROUTE
# ----------------------------

@app.route('/submit', methods=['POST'])
def submit():

    if 'user' not in session:
        return redirect("/login")

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

# ----------------------------

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shanmuga18#",
    database="email_reader"
)
cursor = db.cursor()

# Create a table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        password VARCHAR(255),
        contact VARCHAR(15),
        name VARCHAR(255)
    )
""")
db.commit()

# Define a route for the form
@app.route('/form', methods=['GET', 'POST'])
def user_form():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        name = request.form['name']

        # Insert the form data into the database
        cursor.execute("INSERT INTO users (email, password, contact, name) VALUES (%s, %s, %s, %s)", (email, password, contact, name))
        db.commit()

        return redirect(url_for('hello'))

    return render_template('form.html')

# Define a route for the hello page
@app.route('/hello')
def hello():
    # Fetch data from the database and pass it to the template
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('details.html', users=users)

# Corrected indentation for these lines
@app.route('/')
def home():
    return 'Hello, this is the home page!'

if __name__ == '__main__':
    app.run(debug=True)

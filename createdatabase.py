from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PHW#84#jeor'
app.config['MYSQL_DB'] = 'main'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # To return query results as dictionaries

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Store username and hashed password in the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Retrieve the hashed password from the database for the given username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Check if the hashed password matches the input password
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                # If passwords match, set the user as logged in
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        
        # If login fails, show an error message
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'xyz1234'
    app.run(debug=True)

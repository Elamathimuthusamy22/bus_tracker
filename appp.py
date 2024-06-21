# import logging
# logging.basicConfig(level=logging.DEBUG)
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PHW#84#jeor'
app.config['MYSQL_DB'] = 'patients'

# MySQL configurations


mysql = MySQL(app)
@app.route('/doctoss')
def doctoss():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctoss")
    doctoss = cur.fetchall()
    cur.close()
    # print(doctoss)
    return render_template('doctoss.html',doctoss=doctoss)
    #app.logger.debug(doctoss)


if __name__ == "__main__":
    app.run(debug=True)
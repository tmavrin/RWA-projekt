from flask import Flask, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

with open('password.txt') as f:
    passwd = f.readline().strip()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = 'User'

mysql = MySQL(app)


@app.route('/Login', methods=['GET'])
def describeLogin():
    cur = mysql.connection.cursor()
    cur.execute('DESCRIBE LoginInfo')
    mysql.connection.commit()
    return jsonify(data=cur.fetchall())

@app.route('/Reviews', methods=['GET'])
def describeReview():
    cur = mysql.connection.cursor()
    cur.execute('DESCRIBE Reviews')
    mysql.connection.commit()
    return jsonify(data=cur.fetchall())



if __name__ == '__main__':
    app.run()

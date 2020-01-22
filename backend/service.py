from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

with open('password.txt') as f:
    mysql_passwd = f.readline().strip()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = mysql_passwd
app.config['MYSQL_DB'] = 'User'
app.debug = True

mysql = MySQL(app)

def send_query(query):
    print('Query: ' + query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    data = cur.fetchall()
    print('Returning the following data: ' + str(data))
    return jsonify(data)


################################
##      LoginInfo METHODS     ##
################################

@app.route('/users', methods=['GET'])
def get_users():
    if 'username' in request.args:
        username = request.args['username']
        query = (f'SELECT * FROM LoginInfo WHERE username=\'{username}\'')
    else:
        query = 'SELECT * FROM LoginInfo'
    return send_query(query)

@app.route('/users', methods=['POST'])
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    query = (f'INSERT INTO LoginInfo(Username, Password)  '
            f'VALUES(\'{username}\', \'{password}\')')
    return send_query(query)

@app.route('/users', methods=['PUT'])
def update_user_set_new_password():
    username = request.form.get('username')
    new_password = request.form.get('password')
    query = (f'UPDATE LoginInfo SET Password=\'{new_password}\' '
            f'WHERE username=\'{username}\'')
    return send_query(query)

@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    query = (f'DELETE FROM LoginInfo WHERE username=\'{username}\'')
    return send_query(query)


################################

@app.route('/show-user-reviews', methods=['POST'])
def show_user_reviews():
    '''
    '''
    username = request.form.get('username')
    query = (f'SELECT * FROM Reviews WHERE username=\'{username}\'')
    return send_query(query)

@app.route('/create-review', methods=['POST'])
def create_review():
    '''
    '''
    tourid = request.form.get('tourid')
    username = request.form.get('username')
    review_text = request.form.get('review_text')
    query = (f'INSERT INTO Reviews(TourID, Username, ReviewText)  '
            f'VALUES({tourid}, \'{username}\', \'{review_text}\')')
    return send_query(query)

@app.route('/check-login', methods=['POST'])
def check_login():
    '''
    Returns json in the form:
    { 'count': integer } 
    for each matching user, pass pair
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    query = (f'SELECT count(*) FROM LoginInfo WHERE '
            f'username=\'{username}\' '
            f'and password=\'{password}\'')
    print(query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    data = cur.fetchone()
    print('Returning the following data: ' + str(data[0]))
    return jsonify(count=data[0])

@app.route('/', methods=['GET'])
def greet():
    return 'Sladoled!'

@app.route('/show-reviews', methods=['GET'])
def describe_review():
    query = 'SELECT * FROM  Reviews'
    return send_query(query)



if __name__ == '__main__':
    app.run()

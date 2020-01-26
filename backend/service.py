from flask import Flask, jsonify, request, abort
from flask_mysqldb import MySQL
from flask_cors import CORS
import json


app = Flask(__name__)
cors = CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'duser'
app.config['MYSQL_PASSWORD'] = 'duserpass'
app.config['MYSQL_DB'] = 'agencija'
app.debug = True

mysql = MySQL(app)

def send_query(query):
    #print('Query: ' + query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    data = cur.fetchall()
    #print('Returning the following data: ' + str(data))

    if cur.rowcount == 0:
        return "no result"
    if data:
        row_headers=[x[0] for x in cur.description]
        json_data=[]
        for result in data:
                json_data.append(dict(zip(row_headers,result)))
        return jsonify(json_data)
    else:
        return "success"
    

def check_request_body(json_data, *args):
    try:
        for i in args:
            json_data[i]
        return True
    except:
        return False

def check_params(params, *args):
    try:
        for i in args:
            if params.get(i) is None:
                raise Exception()
        return True
    except:
        return False


################################
##        OFFER METHODS       ##
################################


@app.route('/offers', methods=['GET'])
def get_offers():
    query = "SELECT id,title,description,price,isTop,image,pdf FROM offer"
    if (check_params(request.args, 'pageNo', 'itemNo')):
        pageNo = request.args.get('pageNo')
        itemNo = request.args.get('itemNo')
        query += " LIMIT {},{}".format(int(pageNo)*int(itemNo), itemNo)
    return send_query(query)

@app.route('/offers', methods=['POST'])
def create_offer():
    data = request.get_json()
    if(check_request_body(data, 'title', 'description', 'price')):
        title = data['title']
        desc = data['description']
        price = data['price']
        query = "INSERT INTO offer (title,description,price) VALUES ('{}','{}','{}')".format(title,desc,price)
        return send_query(query)
    else:
        abort(400, "missing properties from body")

@app.route('/offers', methods=['PUT'])
def update_offerr():
    data = request.get_json()
    # mozda postoji bolji nacin za ovo?
    if(check_request_body(data, 'title', 'description', 'price','isTop', 'id')):
        title = data['title']
        desc = data['description']
        #image = data['image']
        #pdf = data['pdf']
        isTop = data['isTop']
        id_ = data['id']
        price = data['price']
        query = "UPDATE offer SET title='{}', description='{}',price={}, isTop={} WHERE id ='{}'".format(title, desc, price, isTop, id_)
        return send_query(query)
    else:
        abort(400, "missing properties from body")

@app.route('/offers', methods=['DELETE'])
def delete_offer():
    if(check_params(request.args, 'id')):
        id_ = request.args.get('id')
        query = "DELETE FROM offer WHERE id='{}'".format(id_)
        return send_query(query)
    else:
        abort(400, "Missing id param")

@app.route('/top-offers', methods=['GET'])
def get_top_offers(): 
    query = "SELECT id,title,description,price,isTop,image,pdf FROM offer WHERE isTop=true"
    return send_query(query)

@app.route('/top-offers', methods=['POST'])
def set_top_offers():
    if(check_params(request.args, 'id')):
        id_ = request.args.get('id')
        query = "UPDATE offer SET isTop=true WHERE id='{}'".format(id_)
        return send_query(query)
    else:
        abort(400, "Missing id param")


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

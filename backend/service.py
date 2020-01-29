from flask import Flask, jsonify, request, abort, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import json, os
from flask_jwt import JWT, jwt_required, current_identity
from datetime import datetime
from werkzeug.security import safe_str_cmp
from flask_bcrypt import Bcrypt



def create_app(test_config=None):
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    last_restart= datetime.now()

    app.config['MYSQL_HOST'] = '172.17.0.4'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'rwaprojekt'
    app.config['MYSQL_DB'] = 'agencija'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SECRET_KEY'] = 'Jn1p4fc28XYv'

    ALLOWED_EXTENSIONS_PDF = set(['pdf'])
    ALLOWED_EXTENSIONS_IMG = set(['png'])

    class User(object):
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password

        def __str__(self):
            return "User(id='%s')" % self.id

    def allowed_pdf(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF

    def allowed_img(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG
        
    app.debug = True

    cors = CORS(app)
    mysql = MySQL(app)
    bcrypt = Bcrypt(app)

    def send_query(query):
        try:
            cur = mysql.connection.cursor()
            cur.execute(query)

            mysql.connection.commit()
            data = cur.fetchall()
            if cur.rowcount == 0:
                return "no result"
            if data:
                row_headers=[x[0] for x in cur.description]
                json_data=[]
                for result in data:
                        json_data.append(dict(zip(row_headers, result)))
                return jsonify(json_data)
            else:
                return "success"
        except:
            abort(409,"DB integrity error, probably duplicate")
        

    def send_query_(query):
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        data = cur.fetchall()
        if cur.rowcount == 0:
            return "no result"
        if data:
            row_headers=[x[0] for x in cur.description]
            json_data=[]
            for result in data:
                    json_data.append(dict(zip(row_headers, result)))
            return json_data
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

    def authenticate(username, password):
        user = send_query_("SELECT id,username,password FROM user where username='{}'".format(username))[0]

        if user and bcrypt.check_password_hash(user['password'], password):
            return User(user['id'].decode('ascii'),user['username'],user['password'])

    def identity(payload):
        user_id = payload['identity']
        return user_id
      
    jwt = JWT(app, authenticate, identity)

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return "JWT Token: VALID"

    @app.route('/register', methods=['POST'])
    def register_user():
        if(check_request_body(request.get_json(), 'username', 'password')):
            username = request.get_json()['username']
            password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
            query = "INSERT INTO user (username,password) VALUES('{}','{}')".format(username, password)
            return send_query(query)
        else:
            abort(400, "missing properties from body, REQUIRED: username, password")


    @app.route('/offers', methods=['GET'])
    def get_offers():
        query = "SELECT id,title,description,price,isTop,image,pdf FROM offer"
        if (check_params(request.args, 'pageNo', 'itemNo')):
            pageNo = request.args.get('pageNo')
            itemNo = request.args.get('itemNo')
            query += " LIMIT {},{}".format(int(pageNo)*int(itemNo), itemNo)
        return send_query(query)

    @app.route('/offers', methods=['POST'])
    #@jwt_required()
    def create_offer():
        data = request.get_json()
        if(check_request_body(data, 'title', 'description', 'price')):
            title = data['title']
            desc = data['description']
            price = data['price']
            query = "INSERT INTO offer (title,description,price) VALUES ('{}','{}','{}')".format(title,desc,price)
            return send_query(query)
        else:
            abort(400, "missing properties from body, REQUIRED: title, description, price")

    @app.route('/offers', methods=['PUT'])
    #@jwt_required()
    def update_offerr():
        data = request.get_json()
        # mozda postoji bolji nacin za ovo?
        if(check_request_body(data, 'title', 'description', 'price', 'id')):
            title = data['title']
            desc = data['description']
            #image = data['image']
            #pdf = data['pdf']
            #isTop = data['isTop']
            id_ = data['id']
            price = data['price']
            query = "UPDATE offer SET title='{}', description='{}',price={} WHERE id ='{}'".format(title, desc, price, id_)
            return send_query(query)
        else:
            abort(400, "missing properties from body, REQUIRED: title, description, price, id")

    @app.route('/offers', methods=['DELETE'])
    #@jwt_required()
    def delete_offer():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            query = "DELETE FROM offer WHERE id='{}'".format(id_)
            return send_query(query)
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/top-offers', methods=['GET'])
    def get_top_offers(): 
        query = "SELECT id,title,description,price,isTop,image,pdf FROM offer WHERE isTop=true"
        return send_query(query)

    @app.route('/top-offers', methods=['POST'])
    #@jwt_required()
    def set_top_offers():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            query = "UPDATE offer SET isTop=true WHERE id='{}'".format(id_)
            return send_query(query)
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/top-offers', methods=['DELETE'])
    #@jwt_required()
    def remove_top_offers():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            query = "UPDATE offer SET isTop=false WHERE id='{}'".format(id_)
            return send_query(query)
        else:
            abort(400, "Missing id param, REQUIRED: id")


    ################################
    ##     File Upload METHODS    ##
    ################################

    @app.route('/pdf', methods=['POST'])
    #@jwt_required()
    def upload_pdf():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            if (request.files.get('pdf') == None):
                abort(400, "No file under file key: `pdf`")
            file = request.files.get('pdf')
            if file and allowed_pdf(file.filename):
                filename = "{}.pdf".format(id_)
                filelink = "pdf?id={}".format(id_)
                query = "UPDATE offer SET pdf='{}' WHERE id='{}'".format(filelink,id_)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/pdfs", filename))
                return 'File successfully uploaded, {}'.format(send_query(query))
            else:
                abort(400, 'Allowed file types are pdf')
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/pdf', methods=['GET'])
    def download_pdf():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            print(id_)
            uploads = os.path.join('', app.config['UPLOAD_FOLDER'] + "/pdfs")
            img_file_name = "{}.pdf".format(id_)
            return send_from_directory(directory=uploads, filename=img_file_name)
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/image', methods=['POST'])
    #@jwt_required()
    def upload_image():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            if (request.files.get('image') == None):
                abort(400, "No file under file key: `image`")
            file = request.files.get('image')
            if file and allowed_img(file.filename):
                filename = "{}.png".format(id_)
                filelink = "image?id={}".format(id_)
                query = "UPDATE offer SET image='{}' WHERE id='{}'".format(filelink,id_)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/images", filename))
                return 'File successfully uploaded, {}'.format(send_query(query))
            else:
                abort(400, 'Allowed file types are pdf')
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/image', methods=['GET'])
    def get_image():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            print(id_)
            uploads = os.path.join('', app.config['UPLOAD_FOLDER']+"/images")
            pdf_file_name = "{}.png".format(id_)
            return send_from_directory(directory=uploads, filename=pdf_file_name)
        else:
            abort(400, "Missing id param, REQUIRED: id")




    ################################
    ##      LoginInfo METHODS     ##
    ################################

    @app.route('/users', methods=['GET'])
    def get_users():
        abort(410, "Endpoint moved to /auth, use: {'username': 'user', 'password' : 'pass'}. For authorization purposes, it returns JWT token for further authorization. /protected endpoint tests JWT token")
        
        #if 'username' in request.args:
        #    username = request.args['username']
        #    query = "SELECT * FROM LoginInfo WHERE username='{}'".format(username)
        #else:
        #    query = 'SELECT * FROM LoginInfo'
        #return send_query(query)

    @app.route('/users', methods=['POST'])
    def create_user():
        abort(410, "Endpoint moved to /register, use: {'username': 'user', 'password': 'pass'}")
        #username = request.form.get('username')
        #password = request.form.get('password')
        #query = "INSERT INTO LoginInfo(Username, Password) VALUES('{}','{}' )".format(username,password)
        #return send_query(query)

    @app.route('/users', methods=['PUT'])
    def update_user_set_new_password():
        abort(410, "Endpoint moved to /register, use: {'username': user, 'password': pass}")
        #username = request.form.get('username')
        #new_password = request.form.get('password')
        #query = "UPDATE LoginInfo SET Password='{}' WHERE username='{}')".format(new_password,username)
        #return send_query(query)

    @app.route('/users/<string:username>', methods=['DELETE'])
    def delete_user(username):
        abort(410, "Endpoint moved to /register, use: {'username': user, 'password': pass}")
        #query = "DELETE FROM LoginInfo WHERE username='{}')".format(username)
        #return send_query(query)


    ################################

    @app.route('/show-user-reviews', methods=['POST'])
    def show_user_reviews():
        abort(410, "Endpoint removed, endpoint doesn't exist anymore")

        #username = request.form.get('username')
        #query = "SELECT * FROM Reviews WHERE username='{}')".format(username)
        #return send_query(query)

    @app.route('/create-review', methods=['POST'])
    def create_review():
        abort(410, "Endpoint removed, endpoint doesn't exist anymore")
        
        #tourid = request.form.get('tourid')
        #username = request.form.get('username')
        #review_text = request.form.get('review_text')
        #query = "INSERT INTO Reviews(TourID, Username, ReviewText) VALUES({}, '{}', '{}')".format(tourid,username,review_text)
        #return send_query(query)

    @app.route('/check-login', methods=['POST'])
    def check_login():
        abort(410, "Endpoint removed, endpoint doesn't exist anymore")
        
        #username = request.form.get('username')
        #password = request.form.get('password')
        #query = "SELECT count(*) FROM LoginInfo WHERE username='{}' and password='{}'')".format(username,password)
        #print(query)
        #cur = mysql.connection.cursor()
        #cur.execute(query)
        #mysql.connection.commit()
        #data = cur.fetchone()
        #print('Returning the following data: ' + str(data[0]))
        #return jsonify(count=data[0])

    @app.route('/show-reviews', methods=['GET'])
    def describe_review():
        abort(410, "Endpoint removed, endpoint doesn't exist anymore")
        
        #query = 'SELECT * FROM  Reviews'
        #return send_query(query)

    @app.route('/', methods=['GET'])
    def greet():
        response = "<h2>Last restart: " + str(last_restart) + "</h2><br> <h2>Working Endpoints</h2>"\
            + "<h3>/offers [GET,POST,PUT,DELETE]</h3><br>"\
            + "<h3>/top-offer [GET,POST,DELETE]</h3><br>"\
            + "<h3>/image [POST,GET]</h3> <p>Requires <b>id</b> for get and post and file with property name <b>image</b> on upload.</p> <br>"\
            + "<h3>/pdf [POST,GET]</h3> <p>Requires <b>id</b> for get and post and file with property name <b>pdf</b> on upload.</p> <br>"\
            + "<h2>JWT AUTHORIZATION</h2><br>"\
            + "<h3>/auth [POST]</h2><br>"\
            + "<h3>@jwt_required METHODS (registered user/admin only)</h2> <p>Every protected request needs to have Authorization: JWT -jwt_token- header.</p><br>"\
            + "<p>Token can be retrieved from 'hostaddress/auth' with body params 'username' and 'password'. </p><br>"\
            + "<p>All passswords are stored as <b>hash</b> in database. </p><br>"
        return response


    if __name__ == '__main__':
        app.run()

    return app

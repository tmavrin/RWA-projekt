from flask import Flask, jsonify, request, abort, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import json, os
from flask_jwt import JWT, jwt_required, current_identity
from datetime import datetime
from werkzeug.security import safe_str_cmp
from flask_bcrypt import Bcrypt
from flask.logging import create_logger



def create_app(test_config=None):
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    last_restart= datetime.now()
    
    #app.config['MYSQL_HOST'] = '172.17.0.2'
    #app.config['MYSQL_USER'] = 'root'
    #app.config['MYSQL_PASSWORD'] = 'rwaprojekt'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'duser'
    app.config['MYSQL_PASSWORD'] = 'duserpass'

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
    LOG = create_logger(app)


    ################################
    ##       GLOBAL METHODS       ##
    ################################

    @app.before_request
    def logRequest():
        LOG.debug(request.headers)

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



    ################################
    ##         USER METHODS       ##
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
    #@jwt_required()
    def protected():
        return jsonify("JWT Token: VALID")

    @app.route('/register', methods=['POST'])
    def register_user():
        if(check_request_body(request.get_json(), 'username', 'password')):
            username = request.get_json()['username']
            password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
            query = "INSERT INTO user (username,password) VALUES('{}','{}')".format(username, password)
            return send_query(query)
        else:
            abort(400, "missing properties from body, REQUIRED: username, password")



    ################################
    ##        OFFER METHODS       ##
    ################################

    @app.route('/offers', methods=['GET'])
    def get_offers():
        query = "SELECT id,title,description,price,isTop,image,pdf FROM offer"
        if (check_params(request.args, 'q')):
            search = request.args.get('q')
            query += " WHERE title LIKE '%{}%' OR description LIKE '%{}%'".format(search, search)
        if (check_params(request.args, 'price')):
            price = request.args.get('price')
            if price == 1:
                query += " ORDER BY price DESC"
            elif price == 0:
                query += " ORDER BY price ASC"
        if (check_params(request.args, 'polazak')):
            polazak = request.args.get('polazak')
            if polazak == 1:
                query += " ORDER BY polazak DESC"
            elif polazak == 0:
                query += " ORDER BY polazak ASC"
        if (check_params(request.args, 'povratak')):
            polazak = request.args.get('povratak')
            if polazak == 1:
                query += " ORDER BY povratak DESC"
            elif polazak == 0:
                query += " ORDER BY povratak ASC"
        if (check_params(request.args, 'pageNo', 'itemNo')):
            pageNo = request.args.get('pageNo')
            itemNo = request.args.get('itemNo')
            query += " LIMIT {},{}".format(int(pageNo) * int(itemNo), itemNo)
        return send_query(query)
    
    @app.route('/offers-count', methods=['GET'])
    def get_number_of_offers():
        query = "SELECT COUNT(*) as count FROM offer"
        data = send_query_(query)
        return jsonify(data[0])

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
            isTop = data['isTop']
            id_ = data['id']
            price = data['price']
            query = "UPDATE offer SET title='{}', description='{}', price='{}', isTop='{}' WHERE id ='{}'".format(title, desc, price, isTop, id_)
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
    ##     FILE UPLOAD METHODS    ##
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
                exists = send_query_("SELECT * FROM offer WHERE id='{}'").format(id_)
                if (exists == "no result"):
                    abort(400,"Invalid id")

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

                exists = send_query_("SELECT * FROM offer WHERE id='{}'").format(id_)
                if (exists == "no result"):
                    abort(400,"Invalid id")

                query = "UPDATE offer SET image='{}' WHERE id='{}'".format(filelink,id_)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/images", filename))
                return 'File successfully uploaded, {}'.format(send_query(query))
            else:
                abort(400, 'Allowed file types are png')
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



    if __name__ == '__main__':
        app.run()

    return app

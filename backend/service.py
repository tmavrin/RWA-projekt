from flask import Flask, jsonify, request, abort, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import json, os


def create_app(test_config=None):
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['MYSQL_HOST'] = '172.17.0.4'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'rwaprojekt'
    app.config['MYSQL_DB'] = 'agencija'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS_PDF = set(['pdf'])
    ALLOWED_EXTENSIONS_IMG = set(['png'])

    def allowed_pdf(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF

    def allowed_img(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG
        
    app.debug = True

    cors = CORS(app)
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
            abort(400, "missing properties from body, REQUIRED: title, description, price")

    @app.route('/offers', methods=['PUT'])
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
    def set_top_offers():
        if(check_params(request.args, 'id')):
            id_ = request.args.get('id')
            query = "UPDATE offer SET isTop=true WHERE id='{}'".format(id_)
            return send_query(query)
        else:
            abort(400, "Missing id param, REQUIRED: id")

    @app.route('/top-offers', methods=['DELETE'])
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
                file.save(os.path.join(app.config['UPLOAD_FOLDER'+ "pdfs"], filename))
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
            pdf_file_name = "{}.pdf".format(id_)
            return send_from_directory(directory=uploads, filename=pdf_file_name)
        else:
            abort(400, "Missing id param, REQUIRED: id")




    ################################
    ##      LoginInfo METHODS     ##
    ################################

    @app.route('/users', methods=['GET'])
    def get_users():
        if 'username' in request.args:
            username = request.args['username']
            query = "SELECT * FROM LoginInfo WHERE username='{}'".format(username)
        else:
            query = 'SELECT * FROM LoginInfo'
        return send_query(query)

    @app.route('/users', methods=['POST'])
    def create_user():
        username = request.form.get('username')
        password = request.form.get('password')
        query = "INSERT INTO LoginInfo(Username, Password) VALUES('{}','{}' )".format(username,password)
        return send_query(query)

    @app.route('/users', methods=['PUT'])
    def update_user_set_new_password():
        username = request.form.get('username')
        new_password = request.form.get('password')
        query = "UPDATE LoginInfo SET Password='{}' WHERE username='{}')".format(new_password,username)
        return send_query(query)

    @app.route('/users/<string:username>', methods=['DELETE'])
    def delete_user(username):
        query = "DELETE FROM LoginInfo WHERE username='{}')".format(username)
        return send_query(query)


    ################################

    @app.route('/show-user-reviews', methods=['POST'])
    def show_user_reviews():
        '''
        '''
        username = request.form.get('username')
        query = "SELECT * FROM Reviews WHERE username='{}')".format(username)
        return send_query(query)

    @app.route('/create-review', methods=['POST'])
    def create_review():
        '''
        '''
        tourid = request.form.get('tourid')
        username = request.form.get('username')
        review_text = request.form.get('review_text')
        query = "INSERT INTO Reviews(TourID, Username, ReviewText) VALUES({}, '{}', '{}')".format(tourid,username,review_text)
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
        query = "SELECT count(*) FROM LoginInfo WHERE username='{}' and password='{}'')".format(username,password)
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

    return app

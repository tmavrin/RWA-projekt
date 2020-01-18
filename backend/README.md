# Backend tech design

### Show User Reviews
route: (`/show-user-reviews`, methods=['POST'])  
parameters: username  
purpose: Returns all reviews associated with the username  

### Show All Reviews
route: (`/show-reviews`, methods=['GET'])  
parameters:  
purpose: Returns all reviews  

### Create Review  
route : (`/create-review`, methods=['POST'])  
parameters: tourid, username, review_text
purpose: Creates a new review entry  

### Create User
route: (`/create-user`, methods=['POST'])  
parameters: username, password  
purpose: Creates a new user  

### Login
route: (`/check-login`, methods=['POST'])  
parameters: username, password  
purpose: Returns number of matching username-password pairs  

### Login Info  
route: (`/show-login-info`, methods=['GET'])  
parameters:   
purpose: Returns all users  

</br></br></br></br>


# Backend setup

## MySQL setup:

```bash
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo mysql_secure_installation
```

## Load database into MySQL:


```bash
$ sudo mysql
```
```
mysql> source user.sql
```

## Flask setup:

```bash
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-flask
$ pip3 install flask flask-mysqldb 
# might need to install dependencies for flask-mysqldb
```

## Create `password.txt` file in the same directory as `service.py`

Create a `password.txt` file which will contain only the MySQL password.
The `service.py` flask script reads the password to access the User database.

## Run Flask server:

```bash
$ python3 service.py
```

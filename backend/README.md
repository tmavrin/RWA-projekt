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

Create a password.txt file which will contain only the MySQL password.
The `service.py` flask script reads the password to access the User database.

## Run Flask server:

```bash
$ python3 service.py
```

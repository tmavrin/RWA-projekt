# Backend tech design

## `TO DO`
If possible, enable receiving and, *more importantly*, returning data in JSON format.  
Backend server should be able to perform all CRUD operations on all tables.  
Note that route URLs for all methods except `DELETE` should contain only the name of DB relation they access.  
For examples, check out the `DONE` section.  
\* Adding pdfs to DB would be nice, but `NOT A PRIORITY`.

#### Get all offers
route: `/offers`, method=`['GET']`  
parameters:  
purpose: Returns all offers

#### Create offer
route: `/offers`, method=`['POST']`  
parameters: title, description, price, date, picture, (pdf*)  
purpose: Creates a new offer

#### Edit offer
route: `/offers`, method=`['PUT']`  
parameters: tourId, title, description, price, date, picture, (pdf*)  
purpose: Edits the offer with specified tourId

#### Delete offer
route: `/offers/tourId`, method=`['DELETE']`  
parameters:  
purpose: Deletes offer with specified tourId

#### Get top offers
route: `/top-offers`, method=`['GET']`  
parameters:  
purpose: Returns all top offers

#### Mark offer as top offer
route: `/top-offers`, method=`['POST']`  
parameters: tourId  
purpose: Adds offer with specified tourId to the top offers list

#### Remove offer from top offers list
route: `/top-offers/tourId`, method=`['DELETE']`  
parameters:   
purpose: Removes offer with specified tourId from the top offers list

## `DONE`
\* Should review the similarity between 'Get user by username' and 'Login'
or how authentication is usually handled in similar cases.
DB should not contain user passwords in raw form. 

#### Get all users
route: `/users`, method=`['GET']`  
parameters:   
purpose: Returns all users  

#### Get user by username*
route: `/users`, method=`['GET']`  
parameters: username  
purpose: Returns user with specified username

#### Create user
route: `/users`, method=`['POST']`  
parameters: username, password  
purpose: Creates a new user

#### Edit user password
route: `/users`, method=`['PUT']`  
parameters: username, password  
purpose: Edits the user (password) with specified username

#### Delete user
route: `/users/username`, method=`['DELETE']`  
parameters:  
purpose: Deletes user with specified username

#### Login*
route: `/check-login`, method=`['POST']`  
parameters: username, password  
purpose: Returns number of matching username-password pairs  


## `NOT A PRIORITY`
#### Get gallery
route: `/gallery`, method=`['GET']`  
parameters:  
purpose: Returns all photos (url)  

#### Get offer by tourId
route: `/offers`, method=`['GET']`  
parameters: tourId  
purpose: Returns offer with specified tourId

#### Show user reviews
route: (`/show-user-reviews`, method=`['POST']`)  
parameters: username  
purpose: Returns all reviews associated with the username  

#### Show all reviews
route: (`/show-reviews`, method=`['GET']`)  
parameters:  
purpose: Returns all reviews  

#### Create review  
route : (`/create-review`, method=`['POST']`)  
parameters: tourid, username, review_text
purpose: Creates a new review entry  



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
$ pip3 install flask flask-mysqldb flask-cors
# might need to install dependencies for flask-mysqldb
```

## Create `password.txt` file in the same directory as `service.py`

Create a `password.txt` file which will contain only the MySQL password.
The `service.py` flask script reads the password to access the User database.

## Run Flask server:

```bash
$ python3 service.py
```

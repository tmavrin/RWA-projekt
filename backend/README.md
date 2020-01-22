# Backend tech design

### Create User
route: (`/create-user`, methods=['POST'])  
parameters: username, password  
purpose: Creates a new user  
</br></br>
### Login
route: (`/check-login`, methods=['POST'])  
parameters: username, password  
purpose: Returns number of matching username-password pairs  
</br></br>
### Create Offer
Route (`/offer/create`, method=`POST`)  
Body: 
```JSON
{
 "title" : string,    
  "description": string,    
  "price": number,
  "date" : timestamp/date/string,
  "picture": url/file,
  "pdf": url/file
} 
```
Response: `HTTP STATUS`  
</br></br>
### Get ALL Offers
route (`/offer/getAll`, method=`GET`)  
Response: 
```JSON
[
  {
    "id" : string,
    "title" : string,    
    "description": string,    
    "price": number,
    "date" : timestamp/date/string,
    "picture": url/file,
    "pdf": url/file
  },
  {
    ...
  },
  ...
]
```
</br></br>
### Get TOP Offers
Route (`/offer/getTop`, method=`GET`)  
Response: 
```JSON
[
  {
    "id": string,
    "title" : string,    
    "description": string,    
    "price": number,
    "date" : timestamp/date/string,
    "picture": url/file,
    "pdf": url/file
  },
  {
    ...
  },
  ...
]
```
</br></br>
### Set TOP Offer
Route (`/offer/setTop`, method=`PUT`)  
Body:
```
{
  "id": string
}
```
Response: `HTTP STATUS`  
</br></br>
### Remove TOP Offer
Route (`/offer/removeTop`, method=`PUT`)  
Body:
```
{
  "id": string
}
```
Response: `HTTP STATUS` 
</br></br>
### Get Gallery
Route (`/gallery/get`, method=`GET`)  
Response :
```
  [
    "url" : string,
    "url" : string,
    "url" : string,
    "url" : string,
    ...
  ]
```

</br></br></br></br></br></br></br></br>
## `NOT PRIORITY` Trenutno nije prioritet   
### Login Info  
route: (`/show-login-info`, methods=['GET'])  
parameters:   
purpose: Returns all users  

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

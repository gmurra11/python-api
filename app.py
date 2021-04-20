from flask import Flask, jsonify, request, Response, json
from settings import *
from BookModel import *
from UserModel import User
from functools import wraps

import jwt, datetime

app.config['SECRET_KEY'] = 'whatever'

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=300)  #ie: token will last 100 secs, from now to 100secs
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

#Creating a decorator
#takes a function - you need to import wraps above
def token_required(f):
    @wraps(f) #preserves original function name otherwise Flask will throw an error
    def wrapper(*args, **kwargs):  #kw keywords
        token = request.args.get('token')
        #decode will try, it can only exceed, otherwise everything else is a exception
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs) # return function to wrapper level
        except:
            return jsonify({'error': 'Need a valid token'}), 401
    return wrapper # return to token_required level

#By default its a GET request Authenticate: books?token=eyJ0eXAiOiJKV1QiLCJh
#GET books?token=xxxxxx
@app.route('/books')
@token_required #passes in ?token variable to the wrapper
def get_books():
    return jsonify({'books': Book.get_all_books()})

def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#POST
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        #Reponse is a constructor, returning http status code; you need to import it at the top
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in the request",
            "helpString": "Data should be passed similiar to {'name': 'bookname', 'price': 7.99, 'isbn': 42325423424}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), 400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>')
def get_isbn(isbn):
    return_value = Book.get_book(isbn)
    return return_value

#PUT method
#Note PUT requries client send full object, ie: price and name.  Partial update, eg: updating name is a http PATCH
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response

#PATCH -- Update single element within our dictionary
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

#HTTP DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with ISBN not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response;



app.run(port=5000)

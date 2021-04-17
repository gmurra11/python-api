from flask import Flask, jsonify, request, Response, json
from settings import *

books = [
    {
        'name': 'Whatever book',
        'price': 6.99,
        'isbn': 5645645454
    },
    {
        'name': 'Another book',
        'price': 8.99,
        'isbn': 254564654564
    }
]

#By default its a GET request
@app.route('/books')
def get_books():
    return jsonify({'books': books})

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
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        #Reponse is a constructor, returning http status code; you need to import it at the top
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

#Update or PUT method
#Note PUT requries client send full object, ie: price and name.  Partial update, eg: updating name is a http PATCH
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

#Update single element within our dictionary - we need a PATCH
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book["name"] = request_data["name"]
    if("price" in request_data):
        updated_book["price"] = request_data["price"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

#HTTP DELETE
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0;
    for book in books:
        if(book["isbn"] == isbn):
            books.pop(i)  #Using the index of the list to delete array element
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with ISBN not found."
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response;



app.run(port=5000)

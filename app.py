from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)
#print(__name__)

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

app.run(port=5000)

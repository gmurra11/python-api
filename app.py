from flask import Flask, jsonify

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

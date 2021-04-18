from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

#db.Model inherits from db.<method> Model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer)

    #self takes in a book object
    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

    def add_book(_name, _price, _isbn):
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]
        # Book comes from db.model, alot funactionality comes from this...
        #The output would be <Book 1>, <Book 2> - we need a friendly format

    def get_book(_isbn):
        the_book = Book.query.filter_by(isbn=_isbn).first()
        return Book.json(the_book)

    def delete_book(_isbn):
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    def update_book_price(_isbn, _price):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        db.session.commit()

    def update_book_name(_isbn, _name):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        db.session.commit()

    def replace_book(_isbn, _name, _price):
        book_to_replace = Book.query.filter_by(isbn=_isbn).first()
        book_to_replace.name = _name
        book_to_replace.price = _price
        db.session.commit()

    #Called only when you run the terminal, ie: python3 only at the prompt
    def __repr__(self): #repr means represents; returns a printable representation of the object
        book_object = {
            'name:': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)

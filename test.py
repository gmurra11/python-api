#Validate what the client sends - we want a valid book
def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

valid_object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 3334534534
}

missing_name = {
    'price': 6.99,
    'isbn': 3334534534
}

missing_price = {
    'name': 'F',
    'isbn': 3334534534
}

missing_isbn = {
    'name': 'F',
    'price': 6.99
}

empty_dictionary = {}

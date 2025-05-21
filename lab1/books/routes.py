from flask import jsonify, request
from marshmallow import ValidationError
from . import books_bp
from .storage import books
from .models import Book
from .schemas import BookSchema

book_schema = BookSchema()

@books_bp.route('/books', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books])

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b.id == book_id), None)
    return jsonify(book.to_dict()) if book else (jsonify({"error": "Not found"}), 404)

@books_bp.route('/books', methods=['POST'])
def add_book():
    json_data = request.get_json()

    try:
        data = book_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    existing_ids = [book.id for book in books]
    new_id = 1
    while new_id in existing_ids:
        new_id += 1

    new_book = Book(id=new_id, title=data['title'], author=data['author'])
    books.append(new_book)
    return jsonify(new_book.to_dict()), 201

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b.id != book_id]
    return jsonify({"message": "Deleted"}), 204

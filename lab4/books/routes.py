from flask import jsonify, request
from marshmallow import ValidationError
from . import books_bp
from .models import Book
from .schemas import BookSchema
from database import db

book_schema = BookSchema()

@books_bp.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=2, type=int)
    cursor = request.args.get('cursor', type=int)
    limit = min(limit, 100)

    query = Book.query.order_by(Book.id)

    if cursor:
        query = query.filter(Book.id > cursor)

    books = query.limit(limit + 1).all()

    has_next = len(books) > limit
    books_to_return = books[:limit]

    next_cursor = books[limit].id if has_next else None

    response = {
        "books": [book.to_dict() for book in books_to_return],
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor,
            "has_next": has_next
        }
    }

    return jsonify(response)

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@books_bp.route('/books', methods=['POST'])
def add_book():
    json_data = request.get_json()
    
    if not json_data:
        return jsonify({"error": "No data provided"}), 400

    try:
        data = book_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    new_book = Book(title=data['title'], author=data['author'])
    
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create book"}), 500

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete book"}), 500
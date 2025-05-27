from flask import jsonify, request
from marshmallow import ValidationError
from . import books_bp
from .models import Book
from .schemas import BookSchema
from database import db

book_schema = BookSchema()

@books_bp.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    limit = min(limit, 100)

    books = Book.query.order_by(Book.id).offset(offset).limit(limit).all()
    total_count = Book.query.count()
    
    response = {
        "books": [book.to_dict() for book in books],
        "pagination": {
            "offset": offset,
            "limit": limit,
            "total": total_count,
            "has_next": offset + limit < total_count,
            "has_prev": offset > 0
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
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from flasgger import swag_from
from flask import request
from .models import Book
from .schemas import BookSchema
from database import db

book_schema = BookSchema()
books_schema = BookSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
parser.add_argument('author', type=str, required=True, help='Author cannot be blank')

class BooksResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'List of books',
                'schema': BookSchema(many=True)
            }
        },
        'parameters': [
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'default': 2,
                'required': False
            },
            {
                'name': 'cursor',
                'in': 'query',
                'type': 'integer',
                'required': False
            }
        ]
    })
    def get(self):
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

        return {
            "books": books_schema.dump(books_to_return),
            "pagination": {
                "limit": limit,
                "next_cursor": next_cursor,
                "has_next": has_next
            }
        }, 200

    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'schema': BookSchema,
                'required': True,
                'description': 'Book data'
            }
        ],
        'responses': {
            201: {
                'description': 'Book created',
                'schema': BookSchema
            },
            400: {'description': 'Validation Error'}
        }
    })
    def post(self):
        args = parser.parse_args()

        try:
            data = book_schema.load(args)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        new_book = Book(title=data['title'], author=data['author'])

        try:
            db.session.add(new_book)
            db.session.commit()
            return book_schema.dump(new_book), 201
        except Exception:
            db.session.rollback()
            return {"error": "Failed to create book"}, 500

class BookResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Book details',
                'schema': BookSchema
            },
            404: {'description': 'Book not found'}
        }
    })
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        return book_schema.dump(book), 200

    @swag_from({
        'responses': {
            200: {'description': 'Book deleted'},
            404: {'description': 'Book not found'}
        }
    })
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404

        try:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully"}, 200
        except Exception:
            db.session.rollback()
            return {"error": "Failed to delete book"}, 500

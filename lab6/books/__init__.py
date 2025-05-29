from flask_restful import Api
from flask import Blueprint
from .routes import BooksResource, BookResource

books_bp = Blueprint('books', __name__)
api = Api(books_bp)

api.add_resource(BooksResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

from flask import Flask
from flasgger import Swagger
from database import db
from books import books_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Swagger(app)

    db.init_app(app)

    app.register_blueprint(books_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

        from books.models import Book
        if Book.query.count() == 0:
            initial_books = [
                Book(title="No Longer Human", author="Osamu Dazai"),
                Book(title="1984", author="George Orwell"),
                Book(title="The Lord of the Rings", author="J.R.R. Tolkien")
            ]

            for book in initial_books:
                db.session.add(book)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')

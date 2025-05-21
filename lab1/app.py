from flask import Flask
from books import books_bp

app = Flask(__name__)
app.register_blueprint(books_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)

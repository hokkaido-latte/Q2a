#Write me a init py file so that my bookController can recognize all_books from books.py
from flask import Flask
from controllers.bookController import bookController
from models.books import all_books
app = Flask(__name__)
app.register_blueprint(bookController)
app.all_books = all_books
@app.route('/')
def index():
    return "Welcome to the Book Store!"
if __name__ == '__main__':
    app.run(debug=True)


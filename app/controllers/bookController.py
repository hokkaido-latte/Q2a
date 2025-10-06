##create a simple book controller that routes to /books.html by default
from flask import Blueprint, render_template
from models.books import all_books

bookController = Blueprint('bookController', __name__)

@bookController.route('/')
@bookController.route('/books')
def books():
    books = all_books
    return render_template('books.html', panel = "Book Titles",books=all_books)




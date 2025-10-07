##create a simple book controller that routes to /books.html by default
from flask import Blueprint, render_template
from ..models.books import all_books

bookController = Blueprint('bookController', __name__)

@bookController.route('/')
@bookController.route('/books')
def books():
    books = all_books
    return render_template('books.html', panel = "Book Titles",books=all_books)

@bookController.route('/bookDetails/<string:book_title>')
def viewBookDetails(book_title):
    book = next((book for book in all_books if book['title'] == book_title), None)
    if book:
        return render_template('bookDetails.html', panel = "Book Titles", book=book)
    else:
        return "Book not found", 404

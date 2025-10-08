# from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for

# from models.forms import BookForm

# from models.users import User
from ..models.books import all_books, Book

books = Blueprint('bookController', __name__) 

@books.route('/')
@books.route('/books')
def books_list():
    allBooks = Book.getAllBooks()
    return render_template('books.html', panel="Book Titles", books=allBooks)


@books.route("/bookDetails/<string:book_title>")
def viewBookDetail(book_title):
    book = Book.getBook(title=book_title)
    if book:
        print(f"Book '{book_title}' exists in Mongo")
        return render_template('bookDetails.html', panel="Book Titles", book=book)
    else:
        # fallback_book = next((b for b in all_books if b['title'] == book_title), None)
        # if fallback_book:
        #     print(f"Book '{book_title}' found in dictionary variable")
        #     return render_template('bookDetails.html', panel="Book Titles", book=fallback_book)
        # else:
        #     print(f"Book '{book_title}' not found in both Mongo and fallback data")
        #     return "Book not found", 404
        return "Book not found", 404

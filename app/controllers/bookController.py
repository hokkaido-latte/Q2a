from flask import Blueprint, request, redirect, render_template, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import random

from ..models.forms import RegForm, BookForm
from ..models.users import User
from ..models.books import all_books, Book
from ..models.loans import Loan

books = Blueprint('bookController', __name__)

PASSWORD = "12345"
ADMIN_HASH = generate_password_hash(PASSWORD, method='pbkdf2:sha256')
PETER_HASH = generate_password_hash(PASSWORD, method='pbkdf2:sha256')
adminUser = User.getUser("admin@lib.sg")
peteroh = User.getUser("poh@lib.sg")
if not adminUser:
    adminUser = User.createUser(email="admin@lib.sg", password=ADMIN_HASH, name="Admin")
if not peteroh:
    nonadminUser = User.createUser(email="poh@lib.sg", password=PETER_HASH, name="Peter Oh")


#For testing
allUsers = User.getAllUsers()
for eachuser in allUsers:
    print(eachuser['name'])

allLoans = Loan.getAllLoans()
for eachLoan in allLoans:
    Loan.deleteLoan(eachLoan)

Book.restoreAllAvailability()

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
        return render_template('bookDetails.html', panel="Book Details", book=book)
    else:
        return "Book not found", 404

@books.route('/login', methods=['GET', 'POST'])
def login():
    form = RegForm()
    if request.method == 'POST':
        print(request.form.get('checkbox'))
        if form.validate():
            check_user = User.getUser(email=form.email.data)
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    # FIX 3: Changed 'bookController.books' to 'bookController.books_list'
                    return redirect(url_for('bookController.books_list'))
                else:
                    form.password.errors.append("User Password Not Correct")
            else:
                form.email.errors.append("No Such User")
    return render_template('login.html', form=form, panel="Login")

@books.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.getUser(email=form.email.data)
            if not existing_user:
                hashpass = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                User.createUser(email=form.email.data, password=hashpass, name=form.name.data)
                return redirect(url_for('bookController.login'))
            else:
                form.email.errors.append("User already existed")
    return render_template('register.html', form=form, panel="Register")


@books.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('bookController.books_list'))

@books.route('/addbook', methods = ['GET','POST'])
@login_required
def addBook():
    form = BookForm()
    genres = ["Animals", "Business", "Comics", "Communication", "Dark Academia", "Emotion", "Fantasy", "Fiction", "Friendship", "Graphic Novels", "Grief", 
"Historical Fiction", "Indigenous", "Inspirational", "Magic", "Mental Health", 
"Nonfiction", "Personal Development",  "Philosophy", "Picture Books", "Poetry", "Productivity", "Psychology", "Romance", "School", "Self Help"] 

    form.genres.choices = [(genre, genre) for genre in genres]

    if form.validate_on_submit():
        try:
            authors_data = [
                entry.author_name.data.strip()
                for entry in form.authors
                if entry.author_name.data and entry.author_name.data.strip()
            ]
            
            description_data=form.description.data
            if isinstance(description_data, str):
                description_list = [d.strip() for d in form.description.data.split('\n') if d.strip()]

            Book.createBook(
                genres=form.genres.data, 
                title=form.title.data, 
                category=form.category.data,
                url=form.url.data,
                description=description_list,
                authors=authors_data,
                pages=int(form.pages.data),
                available=int(form.copies.data),
                copies=int(form.copies.data)
                )
            return redirect(url_for('bookController.books_list'))
        except Exception as e:
            print(f"Error creating book: {e}")
            flash("An error occurred while adding your book")
   
    return render_template('addbook.html', panel="Add A Book",genres=genres, form=form)

@books.route('/loan/<string:book_title>')
@login_required
def loanBook(book_title):
    #Get current user
    member = current_user
    if member.getName() != "Admin":
        #Create a random date 10-20 days before today's date for testing purpose
        borrowDate = datetime.now() - timedelta(days=random.randint(10,20))
        loanBook = Book.getBook(title=book_title)
        if not loanBook:
            flash(f"Book '{book_title}' does not exist", "warning")
            return redirect(url_for('bookController.books_list'))

        loan_result = Loan.createLoan(member=member, book=loanBook, borrowDate=borrowDate)

        if isinstance(loan_result, Loan):
            flash(f"You have successfully borrowed '{book_title}'")
        elif loan_result=="ALREADY_BORROWED":
            flash(f"Failed to loan '{book_title}'. You already have an unreturned loan for this book.", "danger")
        elif loan_result=="UNAVAILABLE":
            flash(f"Failed to loan '{book_title}'. This book is currently unavailable'", "danger")
        else:
            flash(f"Failed to loan '{book_title}' due to enexpected error")

        return redirect(url_for('bookController.books_list'))

    flash("Admin account cannot use loan feature", "warning")
    return redirect(url_for('bookController.books_list'))
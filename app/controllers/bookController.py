# # from flask_login import login_user, login_required, logout_user, current_user
# from flask import Blueprint, request, redirect, render_template, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user, current_user
# # from models.forms import BookForm

# # from models.users import User
# from ..models.forms import RegForm
# from ..models.users import User
# from ..models.books import all_books, Book

# books = Blueprint('bookController', __name__) 

# @books.route('/')
# @books.route('/books')
# def books_list():
#     allBooks = Book.getAllBooks()
#     return render_template('books.html', panel="Book Titles", books=allBooks)


# @books.route("/bookDetails/<string:book_title>")
# def viewBookDetail(book_title):
#     book = Book.getBook(title=book_title)
#     if book:
#         print(f"Book '{book_title}' exists in Mongo")
#         return render_template('bookDetails.html', panel="Book Titles", book=book)
#     else:
#         # fallback_book = next((b for b in all_books if b['title'] == book_title), None)
#         # if fallback_book:
#         #     print(f"Book '{book_title}' found in dictionary variable")
#         #     return render_template('bookDetails.html', panel="Book Titles", book=fallback_book)
#         # else:
#         #     print(f"Book '{book_title}' not found in both Mongo and fallback data")
#         #     return "Book not found", 404
#         return "Book not found", 404

# @books.route('/login', methods=['GET', 'POST'])
# def login():
#     form = RegForm()
#     if request.method == 'POST':
#         print(request.form.get('checkbox'))
#         if form.validate():
#             check_user = User.getUser(email=form.email.data)
#             if check_user:
#                 if check_password_hash(check_user['password'], form.password.data):
#                     login_user(check_user)
#                     return redirect(url_for('bookController.books'))      
#                 else:
#                     form.password.errors.append("User Password Not Correct")
#             else:
#                 form.email.errors.append("No Such User")
#     return render_template('login.html', form=form, panel="Login")

# @books.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegForm()
#     if request.method == 'POST':
#         if form.validate():
#             existing_user = User.getUser(email=form.email.data)
#             if not existing_user:
#                 hashpass = generate_password_hash(form.password.data, method='sha256')
#                 User.createUser(email=form.email.data,password=hashpass, name=form.name.data)
#                 return redirect(url_for('bookController.login'))
#             else:
#                 form.email.errors.append("User already existed")
#                 render_template('register.html', form=form, panel="Register")
#     return render_template('register.html', form=form, panel="Register")

from flask import Blueprint, request, redirect, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from ..models.forms import RegForm
from ..models.users import User
from ..models.books import all_books, Book

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

allUsers = User.getAllUsers()
for eachuser in allUsers:
    print(eachuser.getName())

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

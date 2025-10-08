# from flask import Flask
# from flask_mongoengine import MongoEngine, Document
# from flask_login import LoginManager

# #import pymongo

# db = MongoEngine()

# def create_app():
#     app = Flask(__name__)
#     app.config['MONGODB_SETTINGS'] = {
#         'db':'books',
#         'host':'localhost'
#     }

#     app.static_folder = 'static'
#     app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

#     db.init_app(app)
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'
#     login_manager.login_message = "Please login or register first to get an account."
#     #return app, db, login_manager
#     from .controllers.bookController import books
#     app.register_blueprint(books)
#     return app, login_manager

# # app, db, login_manager = create_app()
# app = create_app()
from flask import Flask
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'books',
        'host': 'localhost'
    }

    app.static_folder = 'static'
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    # FIX 1: The login_view must match the blueprint name and function name
    login_manager.login_view = 'bookController.login'
    login_manager.login_message = "Please login or register first to get an account."

    # FIX 2: Mandatory user_loader function for Flask-Login
    from .models.users import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.getUserById(user_id)

    from .controllers.bookController import books
    app.register_blueprint(books)

    return app, login_manager

app, login_manager = create_app()

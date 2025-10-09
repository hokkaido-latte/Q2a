from app import db
from flask_login import UserMixin


class User(UserMixin, db.Document):
    
    meta = {'collection': 'appUsers'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()
    avatar = db.StringField()
    
    @staticmethod
    def getUser(email):
        return User.objects(email=email).first()

    @staticmethod
    def getUserById(user_id):
        return User.objects(pk=user_id).first()
    
    @staticmethod 
    def createUser(email, name, password):
        user = User.getUser(email)
        if not user:
            user = User(email=email, name=name, password=password, avatar="").save()
        return user  

    # @staticmethod
    # def addAvatar(user):
    #     user.save()

    @staticmethod
    def getAllUsers():
        return User.objects()

    def getName(self):
        return self.name

    @staticmethod
    def deleteUser(email):
        user = User.getUser(email)
        if user:
            user.delete()
            return True
        return False
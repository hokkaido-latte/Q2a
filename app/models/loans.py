from flask_mongoengine import MongoEngine
from .. import db
from ..models.books import Book
from datetime import datetime, timedelta

class Loan(db.Document):
    # Define the collection name
    meta = {'collection': 'loans'}
    member = db.ReferenceField('User', required=True)
    book = db.ReferenceField('Book', required=True)
    borrowDate = db.DateTimeField(required=True)
    returnDate = db.DateTimeField()
    renewCount = db.IntField(default=0)


    #Create loan document
    # @staticmethod
    # def createLoan(member, book, borrowDate):
    #     if Loan.getActiveLoansByMember(member).count()==0:
    #         loan = Loan(member=member, book=book, borrowDate=borrowDate)
    #         if Book.loanBook(book):
    #             loan.save()
    #             return loan
    #         else:
    #            return None
    #     else:
    #         return None

    @staticmethod
    def createLoan(member, book, borrowDate):
        if Loan.getActiveLoansByMember(member, book):
            return "ALREADY_BORROWED"

        loan = Loan(member=member,book=book,borrowDate=borrowDate)

        if Book.loanBook(book):
            loan.save()
            return loan

        else:
            return "UNAVAILABLE"

    #Retrieve loan documents by member
    @staticmethod
    def getLoansByMember(member):
        return Loan.objects(member=member)

    #Retrieve specific loan by member and book
    @staticmethod
    def getLoanByMemberAndBook(member, book):
        return Loan.objects(member=member, book=book).first()
    
    #Update loan details
    @staticmethod
    def loanRenew(loan, borrowDate):
        loan.renewCount += 1
        loan.borrowDate = borrowDate
        loan.save()
        return loan

    #Update loan return details
    @staticmethod
    def loanReturn(loan, returnDate):
        loan.returnDate = returnDate
        loan.save()
        Book.returnBook(loan.book)
        return loan

    #delete loan document
    @staticmethod
    def deleteLoan(loan):
        loan.delete()
        return True

    #Retrieve active loans (not returned) by member
    @staticmethod
    def getActiveLoansByMember(member):
        return Loan.objects(member=member, returnDate=None)   

    #Create a method to see if a member has an active loan for a specific book
    @staticmethod
    def getActiveLoansByMember(member, book):
        return Loan.objects(member=member, book=book, returnDate=None).first()

    @staticmethod
    def getAllLoans():
        return Loan.objects()


    def getDueDate(self):
        #Return due date which is 14 days from borrow date
        return self.borrowDate + timedelta(days=14)
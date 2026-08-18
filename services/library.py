from models.book import Book
from models.member import Member
from models.transaction import Transaction
from datetime import datetime
from late_fee import LateFeeServices
from exceptions import (
    BookNotBorrowedError,
    BookNotFoundError,
    MemberNotFoundError
)

class Library:

    def __init__(self,late_fee_service = None):
        self.books = dict()
        self.members = dict()
        self.transaction  = dict()
        self.next_transaction_id = 1

        if late_fee_service is None:
            late_fee_service = LateFeeServices()
        self.late_fee_service = late_fee_service

    # book Management 
    # add book , delete book ,find book , search book 

    def add_book(self,book):
        if book.id in self.books:
            raise ValueError (
                f"Book with ID {book.id} already exists"
            )
        self.books[book.id]= book 

    def remove_book(self,book_id):
        if book_id not in self.books:
            raise ValueError(
                f" Book with ID {book_id} doesnt exists"
            )
        del self.books[book_id]

    def find_book(self,book_id):
        if book_id not in self.books:
            raise ValueError(
                f"Book with ID{book_id} doesnt exists "
            )
        return self.books[book_id]
    def search_books(self,query):
        query = query.lower()

        results = []

        for book in self.books.values():
            if(
                query in book.title.lower()
                or query in book.author.lower()
                or query in book.category.lower()
                or query in book.isbn.lower()
            ):
                results.append(book)

        return results

    # Member Management 
    # add member , remove member , find member 
    def add_member(self,member):
        if member.id in self.members:
            raise ValueError(
                f"Member with ID {member.id} already exists"
            )
        self.members[member.id] = member

    def remove_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(
                f"Member with ID {member_id} doesnt exists"
            )
        del self.members[member_id]

    def find_member(self, member_id):
        if member_id not in self.members:
            raise ValueError(
                f"Member with ID {member_id} doesnt exists "
            )
        return self.members[member_id]

    # borrow / return 

    def borrow_book(self,book_id,member_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        book.borrow()
        member.borrow(book_id)

        # create transaction
        transaction = Transaction(
            transaction_id= self.next_transaction_id,
            member_id= member_id,
            book_id= book_id,
            borrowed_at= datetime.now()
        )
        self.transaction[self.next_transaction_id] = transaction
        self.next_transaction_id +=1 
        return transaction

    def return_book(self,book_id,member_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if book_id not in member.borrowed_books():
            raise BookNotBorrowedError(
                f"Member with ID {member_id } didnt borrowed this book"
            )
        book.return_book()
        member.return_book(book_id)

        transaction = None
        for current_transaction in self.transaction:
            if(
                current_transaction.member_id == member_id
                and current_transaction.book_id == book_id
                and current_transaction.is_active
            ):
                transaction = current_transaction

            if transaction is None:
                raise ValueError(
                    "No active transaction found for this borrowing"
                )

            # record return time 
            transaction.return_book()

            return transaction
        
    def get_member_late_fee(
            self,
            member_id,
            as_of = None
    ):
        member = self.find_member(member_id)

        results =[]

        for transaction in self.transaction.values():
            if transaction.member_id != member_id:
                continue

            result = self.late_fee_service.calculate_fee(
                transaction,
                as_of=as_of,
            )

            if result.is_late:
                results.append(result)

        total_fee = sum(
            result.late_fee
            for result in results
        )

        return {
            "member_id" : member_id,
            "Results" : results,
            "total_fee" : total_fee 
        }

    def get_defaulters(self, as_of=None):

        defaulters = {}

        for transaction in self.transaction.values():

            result = self.late_fee_service.calculate_fee(
                transaction,
                as_of=as_of,
            )

            if not result.is_late:
                continue

            member_id = result.member_id

            if member_id not in defaulters:
                defaulters[member_id] = {
                    "member_id": member_id,
                    "details": [],
                    "total_fee": 0,
                }

            defaulters[member_id]["details"].append(result)

            defaulters[member_id]["total_fee"] += result.fee

        return list(defaulters.values())
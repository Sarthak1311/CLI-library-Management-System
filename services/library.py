from models.book import Book
from models.member import Member
from exceptions import (
    BookNotBorrowedError,
    BookNotFoundError,
    MemberNotFoundError
)

class Library:

    def __init__(self):
        self.books = dict()
        self.members = dict()
        self.transaction  = dict()

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

    def return_book(self,book_id,member_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if book_id not in member.borrowed_books():
            raise BookNotBorrowedError(
                f"Member with ID {member_id } didnt borrowed this book"
            )
        book.return_book()
        member.return_book(book_id)
        

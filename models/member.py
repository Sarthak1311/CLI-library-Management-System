from .person import Person

class Member(Person):
    def __init__(self,id,name,email,borrowed_books=None):
        super().__init__(id,name,email)
        self.borrowed_books = borrowed_books or set()


    def display_role(self):
        print(f"{self.name} is a member")
        return super().display_role()

    def borrow(self,book_name):
        self.borrowed_books.add(book_name)
        print(f"{self.name} borrowed the {book_name}")

    def retrun_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            print(f"{self.name} return the {book}")
        else: 
            print(f"{self.name} doesn't have {book} in his/her borrowed list")



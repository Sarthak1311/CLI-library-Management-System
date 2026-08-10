from exceptions import BookNotAvailableError,BookError,BookNotFoundError,InvalidISBNError

class Book:

    def __init__(
            self,
            book_id,
            title,
            author,
            category,
            isbn,
            total_copies
    ):
        self.book_id = book_id
        self.title= title
        self.author = author
        self.category = category
        self.isbn = isbn

        if total_copies<0:
            raise ValueError(" Total copies cannot be negative")

        self.total_copies = total_copies
        self.__available_copies = total_copies

    @property
    def available_copies(self):
        return self.__available_copies

    def borrow(self):
        if self.__available_copies == 0:
            raise BookNotAvailableError(
                f"'{self.title}' is not available" 
            )

        self.__available_copies-=1

    def return_book(self):
        if self.__available_copies == self.total_copies:
            raise ValueError(
                f"All copies of the '{self.title}' is available in the library"
            )

        self.__available_copies+=1

    def is_available(self):
        return self.__available_copies>0

    @staticmethod
    def validate_isbn(isbn):
        if not isinstance(isbn, str):
            return False

        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) not in (10, 13):
            return False

        return isbn.isdigit()

    @classmethod
    def from_dict(cls,data):
        isbn = data['isbn']

        if not cls.validate_isbn(isbn):
            raise InvalidISBNError(
                f"Invalid ISBN: {isbn}"
            )
        book = cls(
            book_id = data['id'],
            title= data['title'],
            author = data['author'],
            category = data['category'],
            isbn = data['isbn'],
            total_copies = data['total_copies']   
        )

        book.__available_copies = data['available_copies']

        return book

    def __str__(self):
        return f"{self.title} is written by {self.author}"


    def __repr__(self):
        return (
            f"Book("
            f"id={self.book_id!r}, "
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"isbn={self.isbn!r}, "
            f"category={self.category!r}, "
            f"total_copies={self.total_copies!r}, "
            f"available_copies={self.available_copies!r}"
            f")"
        )
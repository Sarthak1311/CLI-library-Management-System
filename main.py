from models.book import Book
from exceptions import BookError, InvalidISBNError,BookNotAvailableError

def section(title):
    print(f"\n----{title}")

def test_basic_creation():
    section("Basic Creation")

    book = Book(
        1,
        "The Alchmist",
        "Paulo",
        "Fiction/ Drama",
        '9780061122415',
        10
    )
    print(book.title)
    print(book.__repr__)
    print("no of available copies ", book.available_copies)
    print("is the book available ",book.is_available())

def borrow_and_return_test():
    section("borrow/return")
    book = Book(2,"the hoobit","JRR","Fantasy","9780547928227",1)

    book.borrow()
    print("is the book available : ",book.is_available())
    try:
        book.borrow()
    except BookNotAvailableError as e:
        print("Caught expected error " , e)

    book.return_book()
    print("is the book available now : ",book.is_available())
    print("Number of copies in the inventory:",book.available_copies)

    try:
        book.return_book()
    except ValueError as e:
        print("expected error ", e)
    

def test_negative_copies():
    section("Negative total_copies validation")
    try:
        Book(3, "Bad Book", "Someone", "Fiction", "1234567890", -5)
    except ValueError as e:
        print("Caught expected error:", e)


def test_isbn_validation():
    section("ISBN validation")
    print(Book.validate_isbn("9780132350884"))   # True (13 digits)
    print(Book.validate_isbn("0132350882"))       # True (10 digits)
    print(Book.validate_isbn("978-0-13-235088-4"))  # True (dashes stripped)
    print(Book.validate_isbn("abc123"))            # False
    print(Book.validate_isbn(12345))               # False (not a string)


def test_from_dict():
    section("from_dict (valid)")
    data = {
        "id": 4,
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopian",
        "isbn": "9780451524935",
        "total_copies": 5,
        "available_copies": 2
    }
    book = Book.from_dict(data)
    print(book)
    print("Available copies from dict:", book.available_copies)

    section("from_dict (invalid ISBN)")
    bad_data = dict(data, isbn="not-a-valid-isbn")
    try:
        Book.from_dict(bad_data)
    except InvalidISBNError as e:
        print("Caught expected error:", e)


if __name__ == "__main__":
    test_basic_creation()
    test_borrow_and_return()
    test_negative_copies()
    test_isbn_validation()
    test_from_dict()
class LibraryError(Exception):
    """Base Exception for library application """
    pass

class BookError(LibraryError):
    """Base exception for book related error"""
    pass

class BookNotFoundError(BookError):
    pass

class BookNotAvailableError(BookError):
    pass

class InvalidISBNError(BookError):
    pass

class MemberNotFoundError(LibraryError):
    pass
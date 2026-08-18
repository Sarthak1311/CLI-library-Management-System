from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    transaction_id:int
    member_id:int
    book_id:int
    borrowed_at:datetime
    returned_at:Optional[datetime] = None

    def return_book(self):
        if self.returned_at is not None:
            raise ValueError(
                "This book has already been returned"
            )
        self.returned_at= datetime.now()

    @property
    def is_active(self):
        return self.returned_at is None
    
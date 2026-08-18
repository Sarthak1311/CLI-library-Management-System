from dataclasses import dataclass
from datetime import datetime,timedelta
from math import ceil

from models.transaction import Transaction 

@dataclass
class LateFeeResult:
    book_id: int
    member_id : int
    is_late : bool
    day_late : int
    late_fee : int

class LateFeeServices:
    DAYSALLOWED =14 
    BASE_FINE = 500
    DAILY_FINE = 50

    def is_late(
            self,
            transaction: Transaction,
            as_of : datetime | None =None
    )-> bool :
        if as_of is None:
            as_of = datetime.now()

        end_time = transaction.returned_at or as_of

        allowed_until =transaction.borrowed_at + timedelta(days= self.DAYSALLOWED)
        return end_time > allowed_until

    def calculate_fee(
            self,
            transaction : Transaction,
            as_of : datetime |None = None
    )-> LateFeeResult:
        if as_of is None:
            as_of = datetime.now()

        end_time = transaction.returned_at or as_of

        allowed_untill = transaction.borrowed_at + timedelta(days= self.DAYSALLOWED)

        overdue_duration = end_time - allowed_untill 

        # if still days lkeft to return the book return no late fees 
        if overdue_duration.total_seconds()<=0:
            return LateFeeResult(
                book_id= transaction.book_id,
                member_id= transaction.member_id,
                is_late=False,
                day_late=0,
                late_fee=0
            )
        days_late = ceil(
            overdue_duration.total_seconds()/86400
        )

        fee = (
            self.BASE_FINE + (days_late * self.DAILY_FINE)
        )

        return LateFeeResult(
            book_id=transaction.book_id,
            member_id=transaction.member_id,
            is_late=True,
            day_late=days_late,
            late_fee= fee
        )
    
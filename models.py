from database import Base
from datetime import date
from sqlalchemy import DATE, TEXT, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

class BookReviewsFlat(Base):
    __tablename__ = 'book_reviews_flat'
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name : Mapped[str] = mapped_column(TEXT(), nullable=False)
    user_email : Mapped[str] = mapped_column(TEXT(), nullable=False)
    book_title : Mapped[str] = mapped_column(TEXT(), nullable=False)
    book_isbn : Mapped[str | None] = mapped_column(TEXT())
    author_name : Mapped[str] = mapped_column(TEXT(), nullable=False)
    author_country : Mapped[str | None] = mapped_column(TEXT())
    genre_name : Mapped[str | None] = mapped_column(TEXT())
    rating : Mapped[int] = mapped_column(nullable=False)
    review_text : Mapped[str | None] = mapped_column(TEXT())
    review_date : Mapped[date] = mapped_column(DATE, nullable=False)

    __table_args__ = (CheckConstraint("rating > 0 and rating < 6", name='checkra15'), 
                      CheckConstraint("user_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name='checkue15'),
                      CheckConstraint(
                            "book_isbn IS NULL OR char_length(book_isbn) IN (10, 13)",
                            name="checkbi15",
                        ),
                      CheckConstraint("review_date <= CURRENT_DATE", name="checkrd15")
                      )
from typing import List
from database import Base
from datetime import date
from sqlalchemy import DATE, TEXT, CheckConstraint, ForeignKey, UniqueConstraint, text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    __table_args__ = (CheckConstraint("rating > 0 and rating < 6", name='checkra_flat_15'), 
                      CheckConstraint("user_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name='checkue_flat_15'),
                      CheckConstraint(
                            "book_isbn IS NULL OR char_length(book_isbn) IN (10, 13)",
                            name="checkbi_flat_15",
                        ),
                      CheckConstraint("review_date <= CURRENT_DATE", name="checkrd_flat_15")
                      )
    

class User(Base):
    __tablename__='users'
    user_email : Mapped[str] = mapped_column(TEXT(), primary_key=True, autoincrement=False)
    user_name : Mapped[str] = mapped_column(TEXT(), nullable=False)

    reviews : Mapped[List['Review']] = relationship(back_populates='reviewer')

    __table_args__ = (CheckConstraint("user_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name='checkue_users_15'),
                      Index(
                        "ix_user_email_fill70",
                        "user_email",
                        postgresql_with={"fillfactor": 70},
                      ),
                      )

class Book(Base):
    __tablename__='books'
    id : Mapped[int] = mapped_column(primary_key=True)
    book_isbn : Mapped[str | None] = mapped_column(TEXT())
    book_title : Mapped[str] = mapped_column(TEXT(), nullable=False)
    author_name : Mapped[str] = mapped_column(TEXT(), nullable=False)
    genre_name : Mapped[str | None] = mapped_column(TEXT())

    reviews : Mapped[List['Review']] = relationship(back_populates='book')

    __table_args__ = (CheckConstraint(
                            "book_isbn IS NULL OR char_length(book_isbn) IN (10, 13)",
                            name="checkbi_books_15",
                        ),
                        UniqueConstraint(
                            "book_isbn",
                            name="uq_books_isbn_not_null",
                        ),
                        Index(
                            "ix_book_id_fill70",
                            "id",
                            postgresql_with={"fillfactor": 70},
                        ),)

class Review(Base):
    __tablename__='reviews'
    id : Mapped[int] = mapped_column(primary_key=True)
    reviewer_email : Mapped[str] = mapped_column(TEXT(), ForeignKey("users.user_email", ondelete='CASCADE'))
    book_id : Mapped[int | None] = mapped_column(ForeignKey("books.id", ondelete='CASCADE'), nullable=True)
    rating : Mapped[int] = mapped_column(nullable=False)
    review_text : Mapped[str | None] = mapped_column(TEXT())
    review_date : Mapped[date] = mapped_column(DATE, nullable=False)

    reviewer : Mapped['User'] = relationship(back_populates="reviews")
    book : Mapped['Book'] = relationship(back_populates="reviews")

    __table_args__ = (CheckConstraint("rating > 0 and rating < 6", name='checkra_reviews_15'), 
                      CheckConstraint("review_date <= CURRENT_DATE", name="checkrd_reviews_15"),
                      Index(
                          'ix_review_id_fill70',
                          'id',
                          postgresql_with={"fillfactor": 70},
                      ))
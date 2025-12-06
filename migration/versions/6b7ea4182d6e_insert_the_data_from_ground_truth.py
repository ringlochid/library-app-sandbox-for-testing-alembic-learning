"""Insert the data from ground truth

Revision ID: 6b7ea4182d6e
Revises: fd8e6c8dad22
Create Date: 2025-12-06 16:08:22.889266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b7ea4182d6e'
down_revision: Union[str, Sequence[str], None] = 'fd8e6c8dad22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("""INSERT INTO users(
                         user_email,
                         user_name
                         )
                         SELECT DISTINCT user_email, user_name
                         FROM book_reviews_flat
                         """))
    
    conn.execute(sa.text("""INSERT INTO books(
                         book_isbn,
                         book_title,
                         author_name,
                         genre_name
                         )
                         SELECT  DISTINCT
                         book_isbn,
                         book_title,
                         author_name,
                         genre_name
                         FROM book_reviews_flat
                         """))
    
    conn.execute(sa.text("""
                        INSERT INTO reviews(
                        reviewer_email,
                        book_id,
                        rating,
                        review_text,
                        review_date
                        )
                        SELECT
                        f.user_email,
                        b.id,
                        f.rating,
                        f.review_text,
                        f.review_date
                        FROM book_reviews_flat AS f
                        JOIN users AS u
                        ON f.user_email = u.user_email
                        LEFT JOIN books AS b
                        ON b.book_isbn IS NOT DISTINCT FROM f.book_isbn
                        AND b.book_title = f.book_title
                        AND b.author_name = f.author_name;
                        """))

def downgrade() -> None:
    """Downgrade schema."""
    pass

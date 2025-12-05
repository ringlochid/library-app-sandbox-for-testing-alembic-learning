"""insert test user data

Revision ID: 52ed8da2aab8
Revises: 970fb5810ea7
Create Date: 2025-12-05 21:58:11.944231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52ed8da2aab8'
down_revision: Union[str, Sequence[str], None] = '970fb5810ea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute(sa.text("""
        INSERT INTO book_reviews_flat (
            user_name,
            user_email,
            book_title,
            book_isbn,
            author_name,
            author_country,
            genre_name,
            rating,
            review_text,
            review_date
        )
        SELECT
            'seed_user_type1_' || i::text AS user_name,

            'seed_user_type1_' || i::text || '_' ||
            substr(md5(random()::text), 1, 6) || '@example.com' AS user_email,

            'Book ' || substr(md5((i::text || random()::text)), 1, 10) AS book_title,

            CASE
              WHEN random() < 0.1 THEN NULL
              ELSE
                CASE
                  WHEN random() < 0.5 THEN
                    lpad((floor(random() * 1e10))::bigint::text, 10, '0')
                  ELSE
                    lpad((floor(random() * 1e13))::bigint::text, 13, '0')
                END
            END AS book_isbn,

            'Author ' || substr(md5((i::text || 'author')::text), 1, 8) AS author_name,

            (ARRAY['US','UK','AU','CA','CN','JP','FR','DE']
              [1 + floor(random() * 8)])::text AS author_country,

            (ARRAY['Fantasy','Sci-Fi','Romance','Non-Fiction','Mystery','Horror']
              [1 + floor(random() * 6)])::text AS genre_name,

            (floor(random() * 5)::int + 1) AS rating,

            'Review #' || i::text || ' lorem ipsum...' AS review_text,

            (CURRENT_DATE - ((floor(random() * (365 * 5)))::int || ' days')::interval)::date
                AS review_date

        FROM generate_series(1, 3000000) AS s(i);
    """))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("""DELETE FROM book_reviews_flat WEHERE user_name like 'seed_user_type1_%'
                       AND user_email like 'seed_user_type1_%@example.com'
                       """))

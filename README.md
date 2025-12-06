# Alembic BCNF migration with preserved load

Practice project for migrating a denormalized, “bad” table into a BCNF-ish layout while keeping a few million rows of data intact. Postgres + SQLAlchemy + Alembic power the versioned steps.

## Migration flow (version control strategy)
- `970fb5810ea7_create_flatened_table`: create the source `book_reviews_flat` table with checks on email/ISBN/rating/date.
- `52ed8da2aab8_insert_test_user_data`: bulk-seed ~3M synthetic rows into `book_reviews_flat` via `generate_series`, randomizing emails/ISBNs/genres/ratings/dates.
- `fd8e6c8dad22_create_bcnf_tables`: create normalized tables `users`, `books`, and `reviews`, add FK cascades, and use fillfactor-tuned indexes on hot PK columns.
- `6b7ea4182d6e_insert_the_data_from_ground_truth`: populate the BCNF tables from the flat table. Uses distinct selects for `users`/`books` and joins with `IS NOT DISTINCT FROM` to attach reviews to the matching book even when ISBN is null. (Downgrade intentionally left empty for this data-move step.)

## How to run it
1. Ensure Postgres is available and adjust the connection string in both `database.py` and `alembic.ini` if needed (default DB: `library-app-load-testing-sandbox`).
2. Create the database (if missing): `createdb library-app-load-testing-sandbox`.
3. Apply the full migration chain and load data:
   ```bash
   alembic upgrade head
   ```
   Seeding ~3M rows will take time—watch the console output to track progress.

## Resulting schema
- `book_reviews_flat`: original wide table kept for comparison/testing.
- `users`: PK on `user_email`, email format check, fillfactor-tuned index.
- `books`: surrogate `id` PK, optional `book_isbn`, title/author/genre columns, fillfactor-tuned index.
- `reviews`: FK to `users` and `books` (cascade deletes), rating/date checks, fillfactor-tuned index on `id`.

## Notes
- This layout is meant for load-testing migration patterns, not for production-ready constraints (e.g., no uniqueness on ISBN/title/author beyond the surrogate key).
- All SQL in migrations is plain Postgres; adjust for other databases before running elsewhere.

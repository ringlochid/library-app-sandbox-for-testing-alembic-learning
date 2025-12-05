from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASEURL = "postgresql+psycopg://postgres:123456@localhost:5432/library-app-load-testing-sandbox"

engine = create_engine(DATABASEURL, echo=True, future=True, pool_size=5, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
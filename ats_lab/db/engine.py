from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from ..config.settings import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session = Session(engine)

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


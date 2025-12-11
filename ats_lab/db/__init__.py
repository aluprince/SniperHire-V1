"""
init_db.py
----------
Creates tables in the database.
Useful for development.
Alembic migrations will replace this in Phase 2.
"""

from .engine import engine
from .engine import Base

def init_db():
    # Create all tables discovered from Base subclasses
    Base.metadata.create_all(bind=engine)

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database url
# DATABASE_URL = 'sqlite:/// blob/blob.db' # blob.db => filename

# absolute path to blog/ directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# database file inside blog/
DB_PATH = os.path.join(BASE_DIR, "blog.db")

# database url
DATABASE_URL = f"sqlite:///{DB_PATH}"

# create engine
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

# create session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# declare mapping (create Base)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

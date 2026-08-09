from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

DATABASE_URL = "postgresql+psycopg://postgres:ghaith123@localhost:5432/gym"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine,autocommit = False , autoflush=False)

Base = declarative_base()

def get_db() : 
    with LocalSession() as session :
        yield session


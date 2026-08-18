from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from app.config import settings


engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine,autocommit = False , autoflush=False)

Base = declarative_base()

def get_db() : 
    with LocalSession() as session :
        yield session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from app.config import settings

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine,autocommit = False , autoflush=False)

Base = declarative_base()

def get_db() : 
    with LocalSession() as session :
        yield session


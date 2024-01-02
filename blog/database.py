from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #connect_args={"check_same_thread": False}: is needed only for SQLite. It's not needed for other databases.
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.
                                        # And then a new session will be created for the next request.

Base = declarative_base()



# IMP:
'''
https://fastapi.tiangolo.com/tutorial/sql-databases/#main-fastapi-app : scroll for this - Create a dependency



'''
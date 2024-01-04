from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


# for database mapping: SqlAlchemy
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(String)

    # fK col
    user_id = Column(Integer, ForeignKey("users.id") ) #users.id ==> users is the user table name and id is the PK of users table

    creator = relationship("User", back_populates="blogs") # 1st arg is the table name and 2nd is linking column to User table column that will link with this variable/atribute 
    # for using this attrbute inside ShowBlog schema there must be something in user_id But if null thne show error
    def __repr__(self) -> str:
      return f"Id = {self.id}, title = {self.title})"
    


# Model for creating user

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(String)

    blogs = relationship("Blog", back_populates="creator") 
# https://www.youtube.com/watch?v=7t2alSnE2-I&t=164s       go on relationship timeStamp for more about the back_populates
  # OR: https://hackersandslackers.com/sqlalchemy-data-models/
    def __repr__(self) -> str:
      return f"User-Id = {self.id}, User-name = {self.name})"



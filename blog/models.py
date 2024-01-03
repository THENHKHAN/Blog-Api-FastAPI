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

    def __repr__(self) -> str:
      return f"User-Id = {self.id}, User-name = {self.name})"



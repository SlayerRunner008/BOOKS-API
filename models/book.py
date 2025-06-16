from config.database import Base 
from sqlalchemy import Column, String, Integer


class Book(Base):
    __tablename__ = "Books"

    code = Column(Integer, primary_key=True, index = True, autoincrement=True)
    title = Column(String,nullable=False )
    author = Column(String, nullable=False)
    year = Column(Integer,nullable=False)
    category = Column(String, nullable=False)
    numOfPages = Column(Integer, nullable=False)

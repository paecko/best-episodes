from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
base = declarative_base()
class Show(base):
    __tablename__ = 'shows'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    imdb_id = Column(String)
    rating = Column(Numeric)

class Episode(base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    imdb_id = Column(String)
    rating = Column(Numeric)



from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://sqlalchemy.sqlite', echo = True)

base = declarative_base()

class transactions (base):
    __tablename__ = 'Transactions'

    transaction_id = Column(Integer, primary_key = True)
    
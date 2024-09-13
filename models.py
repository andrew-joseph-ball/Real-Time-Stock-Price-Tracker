from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = 'stock_prices'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)


engine = create_engine('sqlite:///stock.db')
Base.metadata.create_all(engine)

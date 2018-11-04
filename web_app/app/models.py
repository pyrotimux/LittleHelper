from database import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey, Float, Date



class HelperTable(Base):
    __tablename__ = 'helpertable'
    Id = Column(Integer(), primary_key=True)
    Title = Column(String(255), nullable=False)
    Plot = Column(String(64000), nullable=False)
    Year = Column(String(255), nullable=False)
    Type = Column(String(255), nullable=False)
    Rated = Column(String(255), nullable=False)
    Genre = Column(String(255), nullable=False)

    def __init__(self, arr):
        self.Title = arr[0]
        self.Plot = arr[1]
        self.Year = arr[2]
        self.Type = arr[3]
        self.Rated = arr[4]
        self.Genre = arr[5]

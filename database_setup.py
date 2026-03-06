from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./cleansl.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Tables

class Resident(Base):
    __tablename__ = "residents"
    house_id = Column(String, primary_key=True)
    road_id = Column(String, index=True)
    past_violations = Column(Integer, default=0)
    last_pickup_date = Column(DateTime)

class Driver(Base):
    __tablename__ = "drivers"
    driver_id = Column(String, primary_key=True)
    
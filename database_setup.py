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
    name = Column(String)
    assigned_road = Column(String)

class RouteLog(Base):
    __tablename__ = "route_logs"
    route_id = Column(Integer, primary_key=True)
    driver_id = Column(String)
    road_id = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    required_minutes = Column(Integer) 
    is_completed = Column(Integer, default=0)

class Complaint(Base):
    __tablename__ = "complaints"
    complaint_id = Column(Integer, primary_key=True)
    type = Column(String) # e.g., 'ILLEGAL_DUMPING'
    road_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

def build_database():
    Base.metadata.create_all(bind=engine)
    print("CleanSL Database created successfully with all tables!")

if __name__ == "__main__":
    build_database()
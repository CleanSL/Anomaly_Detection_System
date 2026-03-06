from sqlalchemy.orm import sessionmaker
from database_setup import engine, Resident, Driver, RouteLog, Complaint
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
db = Session()

def seed_database():
    db.query(Resident).delete()
    db.query(Driver).delete()
    db.query(RouteLog).delete()
    db.query(Complaint).delete()

r1 = Resident(house_id="H-101", road_id="Main_St", 
                  last_pickup_date=datetime.utcnow() - timedelta(days=1))
    
r2 = Resident(house_id="H-102", road_id="Main_St", past_violations=3, 
                  last_pickup_date=datetime.utcnow() - timedelta(days=10))

d1 = Driver(driver_id="D-001", name="Saman", assigned_road="Main_St")
d2 = Driver(driver_id="D-002", name="Kamal", assigned_road="Side_St")

log1 = RouteLog(driver_id="D-001", road_id="Main_St", 
                    start_time=datetime.utcnow() - timedelta(hours=2),
                    end_time=datetime.utcnow() - timedelta(hours=1, minutes=35),
                    required_minutes=20, is_completed=1)
    
log2 = RouteLog(driver_id="D-002", road_id="Side_St", 
                    start_time=datetime.utcnow() - timedelta(minutes=10),
                    end_time=datetime.utcnow() - timedelta(minutes=8),
                    required_minutes=15, is_completed=1)

c1 = Complaint(type="ILLEGAL_DUMPING", road_id="Main_St")

db.add_all([r1, r2, d1, d2, log1, log2, c1])
db.commit() 
print("Database Seeded! Test data is now saved in cleansl.db")

if __name__ == "__main__":
    seed_database()
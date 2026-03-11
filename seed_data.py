from database_setup import supabase
from datetime import datetime, timedelta, timezone

def seed_supabase():
    print("Uploading test data to Supabase...")

    user_id = "00000000-0000-0000-0000-000000000001"
    dummy_user = {
        "id": user_id,
        "role": "resident",
        "full_name": "Test Resident",
        "phone_number": "123456789"
    }
    supabase.table("users").upsert(dummy_user).execute()

    test_addresses = [
        {
            "id": "00000000-0000-0000-0000-000000000101", 
            "street_address": "Main_St", 
            "violation_count": 0,
            "last_collection_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        },
        {
            "id": "00000000-0000-0000-0000-000000000102", 
            "street_address": "Main_St", 
            "violation_count": 4,
            "last_collection_at": (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        },
        {
            "id": "00000000-0000-0000-0000-000000000103",
            "street_address": "Main_St",
            "violation_count": 4,
            "last_collection_at": (datetime.now(timezone.utc) - timedelta(days=15)).isoformat()
        }
    ]
    test_complaints = [
       {
        "resident_id": user_id,
        "address_id": None, 
        "location_name": "Main_St",
        "complaint_text": "Massive illegal heap near the intersection.",
        "status": "pending"
    }
    ]
    
    try:
        print("Uploading addresses...")
        supabase.table("addresses").upsert(test_addresses).execute()
        
        print("Uploading complaints...")
        supabase.table("complaints").upsert(test_complaints).execute()
        
        print(" Full test environment is ready!")
    except Exception as e:
        print(f" Database Error: {e}")

if __name__ == "__main__":
    seed_supabase()
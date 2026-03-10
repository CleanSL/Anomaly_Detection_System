from database_setup import supabase
from datetime import datetime, timedelta

def seed_supabase():
    print("Uploading test data to Supabase...")

    test_addresses = [
        {
            "id": "00000000-0000-0000-0000-000000000101", # UUID format for H-101
            "street_address": "Main_St", 
            "violation_count": 0,
            "last_collection_at": (datetime.utcnow() - timedelta(days=1)).isoformat()
        },
        {
            "id": "00000000-0000-0000-0000-000000000102", # UUID format for H-102
            "street_address": "Main_St", 
            "violation_count": 3, 
            "last_collection_at": (datetime.utcnow() - timedelta(days=10)).isoformat()
        }
    ]

    supabase.table("addresses").insert(test_addresses).execute()
    print("Test data uploaded successfully!")

if __name__ == "__main__":
    seed_supabase()
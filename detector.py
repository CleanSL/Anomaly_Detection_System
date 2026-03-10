from database_setup import supabase
from datetime import datetime, timezone

def check_for_anomalies():
    response = supabase.table("addresses").select("*").execute()
    addresses = response.data

    print(f"Scanning {len(addresses)} houses for anomalies...\n")

    for house in addresses:
        last_date = datetime.fromisoformat(house['last_collection_at'].replace('Z', '+00:00'))
        days_since = (datetime.now(timezone.utc) - last_date).days
        
        violations = house['violation_count']
        
        has_complaint = True
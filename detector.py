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

    if days_since >= 14 and has_complaint and violations > 3:
        print(f"🚨 RED (Critical): House {house['id']} at {house['street_address']}")

    elif (has_complaint and violations > 3) or (days_since >= 14 and has_complaint):
        print(f"⚠️ YELLOW (Warning): House {house['id']} needs investigation.")

    elif days_since <= 7:
        print(f"✅ GREEN (No Anomaly): House {house['id']} is up to date.")

    else:
        print(f"⚪ NEUTRAL: House {house['id']} is between 8-13 days with no complaints.")

if __name__ == "__main__":
    check_for_anomalies()
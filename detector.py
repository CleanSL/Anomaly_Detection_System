from fastapi import FastAPI, HTTPException
from database_setup import supabase
from datetime import datetime, timezone
import uvicorn

app = FastAPI(title="CleanSL Anomaly API"

def check_for_anomalies():
    response = supabase.table("addresses").select("*").execute()
    addresses = response.data

    if not addresses:
        print("Wait! Your database is empty. Run seed_data.py first.")
        return

    print(f"Scanning {len(addresses)} houses for anomalies...\n")

    results = []
    
    for house in addresses:
        house_id = house['id']
        street = house['street_address']

        if not house.get("last_collection_at"):
            print(f"Skipping house {house_id} - missing last_collection_at")
            continue

        last_date = datetime.fromisoformat(house['last_collection_at'].replace('Z', '+00:00'))
        days_since = (datetime.now(timezone.utc) - last_date).days
        
        violations = house['violation_count']

        comp_res = supabase.table("complaints") \
            .select("id") \
            .or_(f"address_id.eq.{house_id},location_name.eq.{street}") \
            .eq("status", "pending") \
            .execute()
        
        complaint_count = len(comp_res.data)
        has_complaint = complaint_count > 0

        score = (days_since * 2) + (violations * 5) + (complaint_count * 10)
        
    status = "NEUTRAL"
    if days_since >= 14 and has_complaint and violations > 3:
        status = "RED"

    elif (has_complaint and violations > 3) or (days_since >= 14 and has_complaint):
        status = "YELLOW"

    elif days_since <= 7:
        status = "GREEN"

    results.append({
            "id": house_id,
            "street": street,
            "status": status,
            "score": score,
            "days_since": days_since,
            "violations": violations,
            "complaint_count": complaint_count
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)

    print(f"\n--- CleanSL Anomaly Report ({len(addresses)} Houses) ---")
    
    for r in results:
        print(f"[{r['status']}] Score: {r['score']} | House: {r['id']} ({r['street']})")

if __name__ == "__main__":
    check_for_anomalies()
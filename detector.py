from fastapi import FastAPI, HTTPException
from database_setup import supabase
from datetime import datetime, timezone
import uvicorn
from models import Address
from pydantic import ValidationError

app = FastAPI(title="CleanSL Anomaly API")

@app.get("/anomalies")
def get_anomaly_report():
    response = supabase.table("addresses").select("*").execute()
    addresses = response.data

    if not addresses:
        return {"message": "Wait! Your database is empty. Run seed_data.py first."}

    results = []
    
    for raw_house in addresses:
        if not isinstance(raw_house, dict):
            continue

        try:
        
            house = Address.model_validate(raw_house)
            
            house_id = house.id
            street = house.street_address
            violations = house.violation_count

            if not house.last_collection_at:
                continue

            
            days_since = (datetime.now(timezone.utc) - house.last_collection_at).days

            
            comp_res = supabase.table("complaints") \
                .select("id") \
                .or_(f"address_id.eq.{house_id},location_name.eq.{street}") \
                .eq("status", "pending") \
                .execute()
            
            complaint_count = len(comp_res.data) if comp_res.data else 0
            has_complaint = complaint_count > 0


            score = (int(days_since) * 2) + (int(violations) * 5) + (int(complaint_count) * 10)
            
   
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

        except ValidationError:
            continue
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return {"anomalies": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
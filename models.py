from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class Address(BaseModel):
    id: str
    street_address: str
    violation_count: int = 0
    last_collection_at: Optional[datetime]

    @field_validator("violation_count", mode="before")
    @classmethod
    def fix_violation(cls, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
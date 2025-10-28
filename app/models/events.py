from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class EventType(str, Enum):
    NUTRITIONAL = "Nutricional"
    REPRODUCTIVE = "Reprodutivo"
    HEALTH = "Saúde"
    PERFORMANCE = "Performance"
    GENERAL = "Geral"

class Event(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    animal_id: str
    type: EventType = EventType.GENERAL
    description: str
    event_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        collection = "events"
        indexes = [
            {"keys": [("event_date", -1)]},
            {"keys": [("description", "text")]},
            {"keys": [("animal_id", 1), ("event_date", -1)]},
            {"keys": [("type", 1), ("event_date", -1)]},
            {"keys": [("animal_id", 1), ("type", 1), ("event_date", -1)]},
        ]
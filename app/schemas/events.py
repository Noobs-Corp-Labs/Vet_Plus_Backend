from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.events import Event, EventType

class EventCreate(BaseModel):
    animal_id: str = Field(..., description="ID do animal relacionado ao evento")
    type: EventType = Field(default=EventType.GENERAL, description="Tipo do evento")
    description: str = Field(..., min_length=1, description="Descrição do evento")
    event_date: Optional[datetime] = Field(
        default=None, 
        description="Data do evento (se não informada, usa a data atual)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "animal_id": "507f1f77bcf86cd799439011",
                "type": "Nutricional",
                "description": "Aplicação de suplemento vitamínico",
                "event_date": "2024-10-27T10:30:00"
            }
        }

class EventResponse(Event):
    id: str = Field(..., alias="_id")
    event_date: datetime

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {
            ObjectId: str
        }
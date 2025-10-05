from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class AnimalStatus(Enum):
    AVAILABLE = 0
    LACTATING = 1
    PREGNANT = 2
    INSEMINATED = 3

class Animal(BaseModel):
    id: str | None = Field(None, alias="_id")
    ear_tag: str
    breed_id: str
    name: str
    description: str
    birth_date: date
    status: AnimalStatus

    class Config:
        collection = "animals"
        json_encoders = {Enum: lambda e: e.name}
        indexes = [
            {"keys": [("ear_tag", 1)], "unique": True},
            {"keys": [("breed_id", 1)]},
            {"keys": [("status", 1)]}
        ]
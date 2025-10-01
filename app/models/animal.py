from datetime import date
from enum import Enum
from pydantic import BaseModel

class AnimalStatus(Enum):
    AVAILABLE = 0
    LACTATING = 1
    PREGNANT = 2
    INSEMINATED = 3

class Animal(BaseModel):
    id: str
    ear_tag: str
    breed_id: str
    name: str
    description: str
    birth_date: date
    status: AnimalStatus
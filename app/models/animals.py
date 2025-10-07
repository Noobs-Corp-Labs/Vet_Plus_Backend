from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class AnimalGender(str, Enum):
    MALE = "Macho"
    FEMALE = "Femea"
    UNKNOWN = "Desconhecido"

class AnimalStatus(str, Enum):
    AVAILABLE = "Disponivel"
    LACTATING = "Lactante"
    PREGNANT = "Gravida"
    INSEMINATED = "Inseminada"
    END_OF_LIFE = "Fim da Vida"

class Animal(BaseModel):
    id: str | None = Field(None, alias="_id")
    ear_tag: str
    breed_id: str
    name: str
    description: str
    birth_date: date
    weight: float
    gender: AnimalGender = AnimalGender.UNKNOWN
    status: AnimalStatus = AnimalStatus.AVAILABLE

    class Config:
        collection = "animals"
        indexes = [
            {"keys": [("ear_tag", 1)], "unique": True},
            {"keys": [("breed_id", 1)]},
            {"keys": [("status", 1)]}
        ]
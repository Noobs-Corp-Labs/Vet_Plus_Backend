from bson import ObjectId
from pydantic import Field

from app.models.breeds import Breed


class BreedResponse(Breed):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {
            ObjectId: str
        }
from pydantic import BaseModel

class Breed(BaseModel):
    id: str
    name: str
    description: str
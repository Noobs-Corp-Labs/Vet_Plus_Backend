from datetime import date
from pydantic import BaseModel, Field, field_validator

from Backend.app.models.raca import Breed
from Backend.app.models.animal import AnimalStatus

class AnimalCreate(BaseModel):
    ear_tag: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificação do brinco do animal"
    )
    breed_id: str = Field(
        ...,
        description="ID da raça do animal"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome do animal"
    )
    description: str = Field(
        default="",
        max_length=500,
        description="Descrição do animal"
    )
    birth_date: date = Field(
        ...,
        description="Data de nascimento do animal"
    )
    status: AnimalStatus = Field(
        default=AnimalStatus.AVAILABLE,
        description="Status do animal"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida e limpa o nome do animal"""
        v = v.strip()
        if not v:
            raise ValueError("Nome não pode ser vazio ou conter apenas espaços")
        return v

    @field_validator('ear_tag')
    @classmethod
    def validate_ear_tag(cls, v: str) -> str:
        """Valida e limpa o identificador do brinco"""
        v = v.strip().upper()
        if not v:
            raise ValueError("Brinco não pode ser vazio ou conter apenas espaços")
        return v
    
    @field_validator('breed_id')
    @classmethod
    def validate_breed_id(cls, v: str) -> str:
        """Valida o ID da raça"""
        v = v.strip()
        if not v:
            raise ValueError("ID da raça não pode ser vazio")
        # Validação adicional para ObjectId do MongoDB (24 caracteres hexadecimais)
        if len(v) != 24:
            raise ValueError("ID da raça deve ter 24 caracteres")
        if not all(c in '0123456789abcdefABCDEF' for c in v):
            raise ValueError("ID da raça deve ser um valor hexadecimal válido")
        return v.lower()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Limpa a descrição"""
        return v.strip()

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        """Valida se a data de nascimento não é futura"""
        today = date.today()
        if v > today:
            raise ValueError("Data de nascimento não pode ser no futuro")
        
        # Validação adicional: animal muito antigo (ex: mais de 30 anos)
        max_age_years = 30
        try:
            min_date = v.replace(year=today.year - max_age_years)
        except ValueError:
            # ajuste para 29/02 em ano não bissexto
            min_date = v.replace(month=2, day=28, year=today.year - max_age_years)
        if v < min_date:
            raise ValueError(f"Data de nascimento não pode ser anterior a {max_age_years} anos")
        
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ear_tag": "BR123456",
                    "breed_id": "507f1f77bcf86cd799439011",
                    "name": "Mimosa",
                    "description": "Animal de alta produção leiteira",
                    "birth_date": "2022-03-15",
                    "status": 0
                }
            ]
        }
    }

class AnimalResponse(BaseModel):
    id: str
    ear_tag: str
    breed: Breed
    name: str
    description: str
    birth_date: date
    status: AnimalStatus

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from app.utils.enums import ScaleFive, ScaleThree

# 🧬 ENUMS
class BreedType(str, Enum):
    TAURINE = "Taurina"
    ZEBU = "Zebuína"
    HYBRID = "Híbrido"

class Temperament(str, Enum):
    CALM = "Calmo"
    AGGRESSIVE = "Bravo"
    QUIET = "Quieto"
    RESTLESS = "Agitado"

class Size(str, Enum):
    SMALL = "Pequeno"
    MEDIUM = "Médio"
    LARGE = "Grande"

class CalvingEase(str, Enum):
    VERY_EASY = "Muito Fácil"
    EASY = "Fácil"
    MEDIUM = "Médio"
    DIFFICULT = "Difícil"
    VERY_DIFFICULT = "Muito Difícil"

class MaintenanceCost(str, Enum):
    LOW = "Baixo"
    MEDIUM = "Médio"
    HIGH = "Alto"

# 🧱 INTERNAL MODELS
class Morphology(BaseModel):
    withers_height: dict = Field(..., example={"male": 140, "female": 130})
    body_length: int
    average_weight: dict = Field(..., example={"male": 900.0, "female": 600.0})
    longevity: int
    size: Size

class Production(BaseModel):
    annual_average: int
    daily_peak: int
    fat: float
    protein: float
    lactations: float
    lactation_cycle_time: int

class Reproduction(BaseModel):
    age_first_calving: int
    calving_interval: int
    conception_rate: float
    calving_ease_index: CalvingEase

class Adaptation(BaseModel):
    heat_resistance: ScaleFive
    parasite_resistance: ScaleFive
    stress_resistance: ScaleFive
    ideal_environment: str
    thermal_sensitivity: ScaleThree

class Health(BaseModel):
    mastitis_incidence: float
    hoof_problems_incidence: float
    ketosis_susceptibility: ScaleThree
    average_scc: int

class Efficiency(BaseModel):
    feed_conversion_ratio: float
    energy_efficiency: ScaleThree
    maintenance_cost: MaintenanceCost

# 🐄 MAIN MODEL
class Breed(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    type: BreedType
    predominant_colors: List[str]
    temperament: Temperament
    morphology: Morphology
    production: Production
    reproduction: Reproduction
    adaptation: Adaptation
    health: Health
    efficiency: Efficiency
    
    class Config:
        collection = "breeds"
        indexes = [
            {"keys": [("name", 1)], "unique": True},
            {"keys": [("type", 1)]},
            {"keys": [("morphology.size", 1)]},
            {"keys": [("adaptation.heat_resistance", 1)]},
        ]
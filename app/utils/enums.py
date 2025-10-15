from enum import Enum

class ScaleThree(str, Enum):
    """Escala de avaliação em 3 níveis"""
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"

class ScaleFive(str, Enum):
    """Escala de avaliação em 5 níveis"""
    MUITO_BAIXA = "Muito Baixa"
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    MUITO_ALTA = "Muito Alta"
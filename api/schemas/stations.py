from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from decimal import Decimal

class StationOut(BaseModel):
    """Schema Pydantic representant une station"""
    model_config = ConfigDict(from_attributes=True)

    station_id : str = Field(max_length=4)
    nom : str = Field(max_length=100)
    commune : str = Field(max_length=50)
    capacite : int = Field(gt=0)
    latitude : Decimal = Field(max_digits=8, decimal_places=5) 
    longitude : Decimal = Field(max_digits=8, decimal_places=5) 
    date_mise_en_service : date

class PaginatedStationResponse(BaseModel):
    """Structure d'une réponse paginée contenant des stations"""
    resultats: list[StationOut]

    page: int
    taille_page: int
    total: int
    pages: int
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Literal, Optional

class IncidentOut(BaseModel):
    """Schema Pydantic representant un incident"""
    model_config = ConfigDict(from_attributes=True)

    incident_id : str = Field(max_length=12)
    date_signalement : datetime
    cible : Literal["velo", "station"]
    velo_id : Optional[str] = Field(max_length=5)
    type_incident : str = Field(max_length=30)
    statut : Literal["ouvert", "en_cours", "resolu"]
    date_resolution : Optional[date]
    technicien : Optional[str] = Field(max_length=50)
    station_id : Optional[str] = Field(max_length=4)

class IncidentPutStatut(BaseModel):
    statut : Literal["ouvert", "en_cours", "resolu"]

class PaginatedIncidentResponse(BaseModel):
    """Structure d'une réponse paginée contenant des incidents"""
    resultats: list[IncidentOut]

    page: int
    taille_page: int
    total: int
    pages: int
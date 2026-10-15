from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Literal, Optional

class TrajetOut(BaseModel):
    """Schema Pydantic representant un trajet"""
    model_config = ConfigDict(from_attributes=True)

    trajet_id : str = Field(max_length=10)
    velo_id : str = Field(max_length=8)
    depart_horodatage : date
    duree_secondes : int = Field(gt=0)
    type_usager : Literal["abonne", "occasionnel"]
    usager_ref : Optional[str] = Field(max_length=9)
    station_depart : str = Field(max_length=4)
    station_arrivee : Optional[str] = Field(max_length=4)

class PaginatedTrajetResponse(BaseModel):
    """Structure d'une réponse paginée contenant des trajets"""
    resultats: list[TrajetOut]

    page: int
    taille_page: int
    total: int
    pages: int
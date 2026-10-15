from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
import math

from api.database import get_db
from api.models.stations import Station
from api.schemas.stations import PaginatedStationResponse, StationOut

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
)

@router.get("", response_model=PaginatedStationResponse)
def liste_stations(
    commune: str = "Toutes",
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retourne une page de stations.
    cet endpoint est public.
    """
    query=select(Station)

    if commune!="Toutes":
        query=query.where(Station.commune==commune)
        
    total = len(db.scalars(query).all())
    
    offset = (page - 1) * taille_page

    stations = db.scalars(
        query
        .order_by(Station.station_id)
        .offset(offset)
        .limit(taille_page)
    ).all()

    pages = math.ceil(total / taille_page) if total else 0

    return PaginatedStationResponse(
        resultats=stations,
        page=page,
        taille_page=taille_page,
        total=total,
        pages=pages,
    )

@router.get("/{id}", response_model=StationOut)
def get_station_by_id(id: str, db: Session = Depends(get_db)):
    """Retourne une station en fonction de son id
    cet endpoint est public.
    """
    station = db.scalar(
        select(Station).where(
            Station.station_id == id
        )
    )

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station introuvable",
        )

    return station
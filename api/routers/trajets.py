from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
import math
from datetime import date

from api.database import get_db
from api.models.trajets import Trajet
from api.schemas.trajets import PaginatedTrajetResponse

router = APIRouter(
    prefix="/trajets",
    tags=["Trajets"],
)

@router.get("", response_model=PaginatedTrajetResponse) 
def liste_trajets(
    date_debut : date=None,
    date_fin : date=None,
    station : str=None,
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retourne une page de trajets.
    cet endpoint est public.
    """
    query=select(Trajet)
    
    if date_debut :
        query=query.where(Trajet.depart_horodatage>=date_debut)
    
    if date_fin :
        query=query.where(Trajet.depart_horodatage<=date_fin)

    if station :
        query=query.where((Trajet.station_depart==station) | (Trajet.station_arrivee==station))

    total = len(db.scalars(query).all())

    offset = (page - 1) * taille_page

    trajets = db.scalars(
        query
        .order_by(Trajet.depart_horodatage)
        .offset(offset)
        .limit(taille_page)
    ).all()

    pages = math.ceil(total / taille_page) if total else 0

    return PaginatedTrajetResponse(
        resultats=trajets,
        page=page,
        taille_page=taille_page,
        total=total,
        pages=pages,
    )
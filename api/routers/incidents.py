from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update
from sqlalchemy.orm import Session
import math
from typing import Literal

from api.database import get_db
from api.models.incidents import Incident
from api.schemas.incidents import IncidentOut, IncidentPutStatut, PaginatedIncidentResponse
from api.models.users import User
from api.securite.dependencies import require_roles

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)

@router.get("", response_model=PaginatedIncidentResponse)
def liste_incidents(
    statut: Literal["Tous", "ouvert", "en_cours", "resolu"] = "Tous",
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retourne une page d'incidents.
    cet endpoint est public.
    """
    query=select(Incident)

    if statut!="Tous" :
        query=query.where(Incident.statut==statut)
        
    total = len(db.scalars(query).all())
    
    offset = (page - 1) * taille_page

    incidents = db.scalars(
        query
        .order_by(Incident.station_id)
        .offset(offset)
        .limit(taille_page)
    ).all()

    pages = math.ceil(total / taille_page) if total else 0

    return PaginatedIncidentResponse(
        resultats=incidents,
        page=page,
        taille_page=taille_page,
        total=total,
        pages=pages
    )


@router.put("/{incident_id}/statut", response_model=IncidentOut)
def update_incident_statut(incident_id, new_statut : IncidentPutStatut, db: Session = Depends(get_db), current_user: User = Depends(require_roles("direction"))) :
    """Change le statut d'un incident.
    cet endpoint est privé, seul le rôle exploitant y à accès.
    """
    query=(
        select(Incident)
        .where(Incident.incident_id == incident_id)
    )
    incident=db.execute(query).scalar()

    if not incident :
        raise HTTPException(status_code=404, detail="Incident introuvable")
    
    # Vérifie que la transition est valide
    def is_transition_valide(old, new) :
        transition_valide=True
        if new == "ouvert" :
            transition_valide=False
        elif new == "en_cours" :
            transition_valide = False if old!="ouvert" else True
        elif new == "resolu" :
            transition_valide = False if old=="resolu" else True
        return transition_valide

    if not is_transition_valide(incident.statut, new_statut.statut) :
        raise HTTPException(status_code=422, detail="Transition de statut non autorisee")

    query=(update(Incident)
        .where(Incident.incident_id == incident_id)
        .values({"statut" : new_statut.statut}
    ))
    db.execute(query)
    db.commit()
    return(incident)
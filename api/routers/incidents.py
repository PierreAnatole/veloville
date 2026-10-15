from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.incidents import Incident
from api.schemas.incidents import IncidentOut, IncidentPutStatut

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)

@router.put("/{incident_id}/statut", response_model=IncidentOut)
def update_incident_statut(incident_id, new_statut : IncidentPutStatut, db: Session = Depends(get_db)) :
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
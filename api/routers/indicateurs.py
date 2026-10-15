from fastapi import APIRouter

from api.services.indicateurs import activite_par_jour, stations_actives, incidents_par_statut

router = APIRouter(
    prefix="/indicateurs",
    tags=["Indicateurs"],
)

@router.get("/activite-par-jour")
def get_activite_par_jour(date_debut : str = None, date_fin : str = None) :
    df_activite=activite_par_jour(date_debut, date_fin).to_dict("records")
    dict_wrapper={"donnees" : df_activite}

    return dict_wrapper

@router.get("/stations-actives")
def get_stations_actives(limite : int = None) :
    df_stations=stations_actives(limite).to_dict("records")
    dict_wrapper={"donnees" : df_stations}

    return dict_wrapper

@router.get("/incidents_par_statut")
def get_incidents_par_statut() :
    df_incidents=incidents_par_statut().fillna('').to_dict("records")
    dict_wrapper={"donnees" : df_incidents}

    return dict_wrapper
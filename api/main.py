from fastapi import FastAPI

from api.routers import stations, trajets, incidents, indicateurs, auth

app = FastAPI(title="Veloville", 
              description="API de la société Veloville",
              version="1.0.0")

app.include_router(auth.router)
app.include_router(stations.router)
app.include_router(trajets.router)
app.include_router(incidents.router)
app.include_router(indicateurs.router)

@app.get("/sante", tags=["Supervision"])
def sante():
    return {"statut": "ok"}
from sqlalchemy import create_engine
import pandas as pd

from api.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_communes():
    df_stations=pd.read_sql_table("station", con=engine)
    df_stations_c=df_stations.copy()

    return (df_stations_c["commune"].drop_duplicates().to_list())

def get_incident_ids():
    df_incidents=pd.read_sql_table("incident", con=engine)
    df_incidents_c=df_incidents.copy()

    return (df_incidents_c["incident_id"].drop_duplicates().to_list())
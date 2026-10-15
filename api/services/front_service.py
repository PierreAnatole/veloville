from sqlalchemy import create_engine
import pandas as pd

from api.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_communes():
    df_stations=pd.read_sql_table("station", con=engine)
    df_stations_c=df_stations.copy()

    return (df_stations_c["commune"].drop_duplicates().to_list())
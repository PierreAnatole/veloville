from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class StationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id : str = Field(max_length=4)
    nom : str = Field(max_length=100)
    commune : str = Field(max_length=50)
    capacite : int = Field(gt=0)
    latitude : float
    longitude : float
    date_mise_en_service : date

# TODO
    # station_id CHAR(4) PRIMARY KEY,
	# nom VARCHAR(100) NOT NULL,
	# commune VARCHAR(50) NOT NULL,
	# capacite INTEGER NOT NULL CHECK (capacite>0),
	# latitude NUMERIC(8,5) NOT NULL,
	# longitude NUMERIC(8,5) NOT NULL,
	# date_mise_en_service DATE NOT NULL
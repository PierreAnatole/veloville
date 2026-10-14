from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from api.database import Base

class Trajet(Base):
    """Table représentant les trajets"""
    __tablename__ = "trajet"

    trajet_id: Mapped[str] = mapped_column(primary_key=True)
    velo_id: Mapped[str] = mapped_column(String(8))
    depart_horodatage: Mapped[datetime.datetime]
    duree_secondes: Mapped[int]
    type_usager: Mapped[str] = mapped_column(String(15))
    usager_ref: Mapped[str|None] = mapped_column(String(9))
    station_depart: Mapped[str] = mapped_column(String(4))
    station_arrivee: Mapped[str|None] = mapped_column(String(4))
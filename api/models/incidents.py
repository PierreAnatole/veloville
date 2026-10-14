from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from api.database import Base

class Incident(Base):
    """Table représentant les incidents"""
    __tablename__ = "incident"

    incident_id: Mapped[str] = mapped_column(primary_key=True)
    date_signalement: Mapped[datetime.datetime] = mapped_column(String(100))
    cible: Mapped[str] = mapped_column(String(10))
    velo_id: Mapped[str|None] = mapped_column(String(5))
    type_incident: Mapped[str] = mapped_column(String(30))
    statut: Mapped[str] = mapped_column(String(10))
    date_resolution: Mapped[datetime.datetime|None]
    technicien: Mapped[str|None] = mapped_column(String(50))
    station_id: Mapped[str|None] = mapped_column(String(4))
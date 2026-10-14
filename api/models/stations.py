from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from api.database import Base

class Station(Base):
    """Table représentant les stations"""
    __tablename__ = "station"

    station_id: Mapped[str] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    commune: Mapped[str] = mapped_column(String(50))
    capacite: Mapped[int]
    latitude: Mapped[float]
    longitude: Mapped[float]
    date_mise_en_service: Mapped[datetime.datetime]
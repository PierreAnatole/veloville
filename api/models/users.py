from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base

class User(Base):
    """Utilisateur de l'API avec un rôle d'autorisation."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Identifiant utilisé lors du login.
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True
    )

    # Seul le hash bcrypt est stocké.
    password_hash: Mapped[str] = mapped_column(String(100))

    # Le rôle détermine les actions autorisées.
    role: Mapped[str] = mapped_column(
        String(50),
        default="exploitant"
    )
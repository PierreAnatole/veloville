"""Dépendances d'authentification et d'autorisation."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.users import User
from api.securite.security import decode_access_token

# Déclare dans FastAPI/Swagger une authentification Bearer.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Authentifie l'utilisateur à partir du JWT."""

    # Aucun token : on ne sait pas qui appelle l'API.
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # credentials.credentials contient le JWT sans le mot "Bearer".
        payload = decode_access_token(credentials.credentials)

        # sub contient le username placé dans le token.
        username = payload.get("sub")

    except jwt.ExpiredSignatureError:
        # Token correctement signé mais arrivé après exp.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    except jwt.InvalidTokenError:
        # Token modifié, mal signé ou invalide.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # On recharge l'utilisateur depuis PostgreSQL.
    user = db.scalar(
        select(User).where(User.username == username)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur inconnu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_roles(*allowed_roles: str):
    """Fabrique une dépendance limitée à certains rôles."""

    def check_role(
        # Authentification d'abord.
        current_user: User = Depends(get_current_user),
    ) -> User:

        # Ici l'utilisateur est connu : un refus devient donc un 403.
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle non autorisé pour cette action",
            )

        return current_user

    return check_role
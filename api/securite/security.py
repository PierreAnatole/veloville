"""Fonctions de sécurité : bcrypt et JWT."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from api.config import JWT_ALGORITHM, JWT_EXPIRATION_MINUTES, JWT_SECRET


def hash_password(plain_password: str) -> str:
    """Hache un mot de passe avant son stockage."""

    # gensalt() génère un sel aléatoire intégré au hash bcrypt.
    salt = bcrypt.gensalt()

    # hashpw() calcule le hash à partir du mot de passe et du sel.
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        salt,
    )

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash."""

    # checkpw() compare sans jamais déchiffrer le mot de passe stocké.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(username: str, role: str) -> str:
    """Crée un JWT signé contenant identité et rôle."""

    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=JWT_EXPIRATION_MINUTES)

    payload = {
        # sub identifie le propriétaire du token.
        "sub": username,

        # role est un claim applicatif utilisé pour expliquer les autorisations.
        "role": role,

        # iat indique quand le token a été créé.
        "iat": now,

        # exp indique quand le token devient invalide.
        "exp": expiration,
    }

    # encode() signe le payload avec le secret du serveur.
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Vérifie signature et expiration puis retourne le payload."""

    # decode() refuse les tokens modifiés, mal signés ou expirés.
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )
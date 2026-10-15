"""Génère un secret aléatoire pour la signature HS256."""

import secrets

print(secrets.token_hex(32))

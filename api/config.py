"""Chargement de la configuration depuis le fichier .env."""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
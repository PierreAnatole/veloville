"""Schémas Pydantic."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class RegisterRequest(BaseModel):
    """Le rôle n'est pas demandé : l'inscription crée toujours un viewer."""
    username: str = Field(max_length=50)
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_utilisateur: int
    username: str
    role: str

class RoleUpdateRequest(BaseModel):
    """Liste fermée des rôles acceptés."""
    role: Literal["exploitant", "direction"]

class CurrentUser(BaseModel):
    username: str
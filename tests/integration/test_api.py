"""Tests d'intégration de l'API avec TestClient.

À compléter : au moins /sante, /auth/login (OK et KO), une route protégée sans jeton
(401), PUT /incidents/{id}/statut avec le rôle direction (403).
"""
def test_get_sante(client):
    # Arrange
    expected_status_code=200

    # Act
    reponse = client.get("/sante")
    ouvrages = reponse.json()

    # Assert
    assert reponse.status_code == expected_status_code

def test_post_auth_login_success(client):
    # Arrange
    payload={
        "username": "exploitant01",
        "password": "Formation2026!"
    }
    expected_status_code=200

    # Act
    reponse = client.post("/auth/login", json=payload)
    token = reponse.json()

    # Assert
    assert reponse.status_code == expected_status_code
    assert token["access_token"] != None

def test_post_auth_login_fail(client):
    # Arrange
    payload={
        "username": "exploitant01",
        "password": "mauvais_mot_de_passe"
    }
    expected_status_code=401

    # Act
    reponse = client.post("/auth/login", json=payload)
    token = reponse.json()

    # Assert
    assert reponse.status_code==expected_status_code
    assert token["detail"] == "Identifiants invalides"

def  test_change_incident_not_logged_fails(client):
    # Arrange
    payload={
        "statut": "ouvert"
    }
    expected_status_code=401

    # Act
    reponse = client.put("/incidents/I2026-0001/statut", json=payload)
    token = reponse.json()

    # Assert
    assert reponse.status_code==expected_status_code
    assert token["detail"] == "Authentification requise"
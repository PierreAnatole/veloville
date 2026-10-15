import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

sys.path.append('../veloville')
from api.database import get_db
from api.main import app
from api.config import DATABASE_URL

engine_test = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionTest = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)

@pytest.fixture()
def db_session():
    connexion = engine_test.connect()
    transaction = connexion.begin()
    session = SessionTest(bind=connexion, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connexion.close()
        
@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
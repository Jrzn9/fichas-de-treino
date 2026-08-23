import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def admin_token(client):
    client.post("/usuarios/", json={
        "nome": "Admin",
        "email": "admin@example.com",
        "senha": "senha123"
    })

    db = TestingSessionLocal()
    from app.models import Usuario
    usuario = db.query(Usuario).filter(Usuario.email == "admin@example.com").first()
    usuario.is_admin = True
    db.commit()
    db.close()

    resposta = client.post("/login", json={
        "email": "admin@example.com",
        "senha": "senha123"
    })
    return resposta.json()["access_token"]
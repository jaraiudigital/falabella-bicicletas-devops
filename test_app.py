import os
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_csv_dataset_exists():
    """Verifica que el dataset extraído existe en el proyecto."""
    assert os.path.exists("productos_falabella_bicicletas.csv"), "Falta el archivo CSV del catálogo."


def test_health_endpoint(client):
    """Verifica que el endpoint /health responda HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_index_page_loads(client):
    """Verifica que la página principal renderice correctamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Bicicletas Falabella Colombia" in response.data


def test_api_bicicletas_json(client):
    """Verifica que la API REST entregue la estructura JSON esperada."""
    response = client.get("/api/bicicletas")
    assert response.status_code == 200
    payload = response.get_json()
    assert "total" in payload
    assert isinstance(payload["productos"], list)

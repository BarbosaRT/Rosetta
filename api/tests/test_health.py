"""Smoke test da API. Rodar: uv run pytest api/tests"""

from fastapi.testclient import TestClient

from hmer_api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_recognize_validates_contract():
    """Payload de tinta válido é aceito pela validação (mesmo que o modelo devolva 501)."""
    payload = {"strokes": [{"points": [{"x": 1, "y": 2}]}]}
    r = client.post("/recognize", json=payload)
    # 501 = contrato ok, modelo ainda não treinado (stub). 422 seria contrato quebrado.
    assert r.status_code in (200, 501)


# TODO(Fase 3): test /evaluate com "1+1" → "2" após implementar SymPy.

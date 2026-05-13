import pytest
from app.main import app


@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as c:
        yield c


class TestHealthEndpoints:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "healthy"}

    def test_ready(self, client):
        resp = client.get("/ready")
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "ready"}


class TestGetIp:
    def test_returns_remote_addr(self, client):
        resp = client.get("/", environ_base={"REMOTE_ADDR": "1.2.3.4"})
        assert resp.status_code == 200
        assert resp.get_json() == {"your_ip": "1.2.3.4"}

    def test_uses_x_forwarded_for(self, client):
        resp = client.get("/", headers={"X-Forwarded-For": "10.0.0.1"})
        assert resp.status_code == 200
        assert resp.get_json() == {"your_ip": "10.0.0.1"}

    def test_multiple_x_forwarded_for(self, client):
        resp = client.get("/", headers={"X-Forwarded-For": "10.0.0.1, 10.0.0.2, 10.0.0.3"})
        assert resp.status_code == 200
        assert resp.get_json() == {"your_ip": "10.0.0.1"}

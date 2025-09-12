from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get('/api/users')
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    if users:
        assert 'email' in users[0]
        assert 'id' in users[0]

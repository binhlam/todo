from fastapi import status
from fastapi.testclient import TestClient

from .. import main

client = TestClient(main.app)


def test_health_check():
  response = client.get("/api/health_check")
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'status': 'healthy'}

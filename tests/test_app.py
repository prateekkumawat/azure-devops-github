from app import create_app


def test_home_page_loads():
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Your Flask app is running" in response.data


def test_health_endpoint_returns_ok():
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
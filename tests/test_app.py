from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from app import create_app


def test_home_page_loads():
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Inventory dashboard" in response.data
    assert b"Low stock alerts" in response.data


def test_health_endpoint_returns_ok():
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_about_and_contact_pages_load():
    client = create_app().test_client()

    assert client.get("/about").status_code == 200
    assert client.get("/contact").status_code == 200


def test_contact_form_confirms_submission():
    client = create_app().test_client()

    response = client.post(
        "/contact",
        data={"name": "Ada", "email": "ada@example.com", "message": "Hello"},
    )

    assert response.status_code == 200
    assert b"Your message was received" in response.data


def test_database_url_is_configured():
    app = create_app()

    assert app.config["DATABASE_URL"].startswith("mysql+pymysql://")


def test_database_health_reports_unavailable_on_connection_error(monkeypatch):
    def fail_connect(_engine):
        raise SQLAlchemyError("database unavailable")

    monkeypatch.setattr(Engine, "connect", fail_connect)
    client = create_app().test_client()

    response = client.get("/db-health")

    assert response.status_code == 503
    assert response.get_json() == {"status": "unavailable", "database": "mysql"}
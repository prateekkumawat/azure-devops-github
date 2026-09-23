# Flask Contact API

A production-oriented Flask app with a server-rendered contact form, SQL-backed message storage, JSON API, health endpoints, and tests.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run --debug
```

Open <http://127.0.0.1:5000> in a browser. The health endpoint is available at <http://127.0.0.1:5000/health>.

## MySQL connection

Create a MySQL database named `flask_app`, then set the connection string before starting Flask:

```powershell
$env:DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3306/flask_app"
flask --app app run --debug
```

Use <http://127.0.0.1:5000/db-health> to check the connection. It returns `200` when MySQL is reachable and `503` when it is unavailable.

## Test

```powershell
pytest
```

## Configuration

The app accepts `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`, `SECRET_KEY`, and `DATABASE_URL` environment variables.

## API

Create a message:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/messages `
	-ContentType "application/json" `
	-Body '{"name":"Ada Lovelace","email":"ada@example.com","message":"Hello"}'
```

List messages with `GET /api/messages`. Set `API_KEY` in production and send it as the `X-API-Key` header for this administrative endpoint. The schema is created lazily on the first database-backed request; use a migration tool such as Alembic for controlled production schema changes.
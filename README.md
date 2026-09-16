# Flask Basics

A minimal Flask app with a server-rendered page, static CSS, a health endpoint, and tests.

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
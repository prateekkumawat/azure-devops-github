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

## Test

```powershell
pytest
```

## Configuration

The app accepts `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`, and `SECRET_KEY` environment variables.
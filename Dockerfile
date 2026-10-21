FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY --chown=app:app app.py ./
COPY --chown=app:app static/ ./static/
COPY --chown=app:app templates/ ./templates/

USER app

EXPOSE 8000

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app:app"]
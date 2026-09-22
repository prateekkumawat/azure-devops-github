import os

from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["DATABASE_URL"] = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:NewStrongPassword123@127.0.0.1:3306/flask_app",
    )
    database_engine = create_engine(
        app.config["DATABASE_URL"],
        pool_pre_ping=True,
        pool_recycle=280,
    )

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        submitted = request.method == "POST"
        return render_template("contact.html", submitted=submitted)

    @app.get("/db-health")
    def database_health():
        try:
            with database_engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return jsonify(status="unavailable", database="mysql"), 503

        return jsonify(status="ok", database="mysql")

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
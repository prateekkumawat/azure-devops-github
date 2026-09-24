import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
    insert,
    select,
    text,
)
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
    metadata = MetaData()
    contact_messages = Table(
        "contact_messages",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(120), nullable=False),
        Column("email", String(320), nullable=False),
        Column("message", Text, nullable=False),
        Column("created_at", DateTime(timezone=True), nullable=False),
    )
    inventory_categories = Table(
        "categories",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(120), nullable=False),
        Column("slug", String(120), nullable=False, unique=True),
        Column("description", Text, nullable=True),
        Column("created_at", DateTime(timezone=True), nullable=False),
    )
    inventory_products = Table(
        "products",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(180), nullable=False),
        Column("sku", String(120), nullable=False, unique=True),
        Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
        Column("price", Float, nullable=False),
        Column("stock_quantity", Integer, nullable=False),
        Column("status", String(30), nullable=False, default="in_stock"),
        Column("created_at", DateTime(timezone=True), nullable=False),
    )

    def initialise_database():
        metadata.create_all(database_engine)
        with database_engine.begin() as connection:
            category_count = connection.execute(
                select(func.count()).select_from(inventory_categories)
            ).scalar_one()
            if category_count == 0:
                category_rows = [
                    {
                        "name": "Electronics",
                        "slug": "electronics",
                        "description": "Gadgets, accessories, and digital tools.",
                        "created_at": datetime.now(timezone.utc),
                    },
                    {
                        "name": "Office Supplies",
                        "slug": "office-supplies",
                        "description": "Daily essentials for desks and teams.",
                        "created_at": datetime.now(timezone.utc),
                    },
                    {
                        "name": "Furniture",
                        "slug": "furniture",
                        "description": "Workspaces and comfort-focused essentials.",
                        "created_at": datetime.now(timezone.utc),
                    },
                ]
                connection.execute(insert(inventory_categories), category_rows)

            product_count = connection.execute(
                select(func.count()).select_from(inventory_products)
            ).scalar_one()
            if product_count == 0:
                category_lookup = {
                    row["slug"]: row["id"]
                    for row in connection.execute(
                        select(inventory_categories.c.slug, inventory_categories.c.id)
                    ).mappings().all()
                }
                product_rows = [
                    {
                        "name": "Wireless Mouse",
                        "sku": "ELE-1001",
                        "category_id": category_lookup["electronics"],
                        "price": 24.99,
                        "stock_quantity": 12,
                        "status": "in_stock",
                        "created_at": datetime.now(timezone.utc),
                    },
                    {
                        "name": "USB-C Hub",
                        "sku": "ELE-1002",
                        "category_id": category_lookup["electronics"],
                        "price": 49.5,
                        "stock_quantity": 7,
                        "status": "low_stock",
                        "created_at": datetime.now(timezone.utc),
                    },
                    {
                        "name": "Ergonomic Keyboard",
                        "sku": "OFF-2001",
                        "category_id": category_lookup["office-supplies"],
                        "price": 68.0,
                        "stock_quantity": 18,
                        "status": "in_stock",
                        "created_at": datetime.now(timezone.utc),
                    },
                    {
                        "name": "Office Chair",
                        "sku": "FUR-3001",
                        "category_id": category_lookup["furniture"],
                        "price": 139.99,
                        "stock_quantity": 3,
                        "status": "critical",
                        "created_at": datetime.now(timezone.utc),
                    },
                ]
                connection.execute(insert(inventory_products), product_rows)

    def message_payload(data):
        values = {
            field: str(data.get(field, "")).strip()
            for field in ("name", "email", "message")
        }
        errors = {
            field: f"{field.capitalize()} is required."
            for field, value in values.items()
            if not value
        }
        if values["email"] and ("@" not in values["email"] or "." not in values["email"].split("@")[-1]):
            errors["email"] = "Enter a valid email address."
        if len(values["name"]) > 120:
            errors["name"] = "Name must be 120 characters or fewer."
        if len(values["message"]) > 10000:
            errors["message"] = "Message must be 10,000 characters or fewer."
        return values, errors

    def api_key_is_valid():
        configured_key = os.environ.get("API_KEY")
        return not configured_key or request.headers.get("X-API-Key") == configured_key

    @app.get("/")
    def home():
        try:
            initialise_database()
            with database_engine.connect() as connection:
                total_products = connection.execute(
                    select(func.count()).select_from(inventory_products)
                ).scalar_one()
                low_stock = connection.execute(
                    select(func.count()).select_from(inventory_products).where(
                        inventory_products.c.stock_quantity <= 10
                    )
                ).scalar_one()
                categories_count = connection.execute(
                    select(func.count()).select_from(inventory_categories)
                ).scalar_one()
        except SQLAlchemyError:
            total_products = 0
            low_stock = 0
            categories_count = 0
        return render_template(
            "index.html",
            total_products=total_products,
            low_stock=low_stock,
            categories_count=categories_count,
        )

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/categories")
    def categories():
        try:
            initialise_database()
            with database_engine.connect() as connection:
                rows = connection.execute(
                    select(inventory_categories).order_by(inventory_categories.c.name.asc())
                ).mappings().all()
        except SQLAlchemyError:
            rows = []
        return render_template("categories.html", categories=rows)

    @app.get("/inventory")
    def inventory():
        try:
            initialise_database()
            with database_engine.connect() as connection:
                rows = connection.execute(
                    select(
                        inventory_products.c.id,
                        inventory_products.c.name,
                        inventory_products.c.sku,
                        inventory_products.c.price,
                        inventory_products.c.stock_quantity,
                        inventory_products.c.status,
                        inventory_categories.c.name.label("category_name"),
                    )
                    .select_from(
                        inventory_products.join(
                            inventory_categories,
                            inventory_products.c.category_id == inventory_categories.c.id,
                        )
                    )
                    .order_by(inventory_products.c.name.asc())
                ).mappings().all()
        except SQLAlchemyError:
            rows = []
        return render_template("inventory.html", products=rows)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "GET":
            return render_template("contact.html", submitted=False)

        values, errors = message_payload(request.form)
        if errors:
            return render_template("contact.html", submitted=False, errors=errors, values=values), 400

        try:
            initialise_database()
            with database_engine.begin() as connection:
                connection.execute(insert(contact_messages).values(
                    **values,
                    created_at=datetime.now(timezone.utc),
                ))
        except SQLAlchemyError:
            return render_template("contact.html", submitted=False, errors={"database": "Messages are temporarily unavailable."}, values=values), 503

        return render_template("contact.html", submitted=True)

    @app.post("/api/messages")
    def create_message():
        data = request.get_json(silent=True) or {}
        values, errors = message_payload(data)
        if errors:
            return jsonify(error="Validation failed", fields=errors), 400

        try:
            initialise_database()
            with database_engine.begin() as connection:
                result = connection.execute(insert(contact_messages).values(
                    **values,
                    created_at=datetime.now(timezone.utc),
                ))
        except SQLAlchemyError:
            return jsonify(error="Database unavailable"), 503

        return jsonify(id=result.inserted_primary_key[0], **values), 201

    @app.get("/api/messages")
    def list_messages():
        if not api_key_is_valid():
            return jsonify(error="Unauthorized"), 401

        try:
            initialise_database()
            with database_engine.connect() as connection:
                rows = connection.execute(
                    select(contact_messages).order_by(contact_messages.c.created_at.desc())
                ).mappings().all()
        except SQLAlchemyError:
            return jsonify(error="Database unavailable"), 503

        return jsonify(messages=[
            {
                **{key: row[key] for key in ("id", "name", "email", "message")},
                "created_at": row["created_at"].isoformat(),
            }
            for row in rows
        ])

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
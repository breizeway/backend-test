from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from ariadne import make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphQL
from dotenv import load_dotenv

from .schema import type_defs, resolvers

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration
    if config_name:
        app.config.from_object(f"config.{config_name}")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models to register them
    from . import models

    # GraphQL Schema
    schema = make_executable_schema(type_defs, resolvers)

    # GraphQL Explorer (development)
    explorer_html = ExplorerGraphQL().html(None)

    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        return explorer_html, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        success, result = graphql_sync(
            schema, request.get_json(), context_value={"request": request, "db": db}
        )
        status_code = 200 if success else 400
        return result, status_code

    @app.route("/health")
    def health_check():
        return {"status": "healthy", "service": "backend-test"}, 200

    return app

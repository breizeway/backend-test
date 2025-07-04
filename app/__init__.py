from flask import Flask, request
from flask_migrate import Migrate
from flask_cors import CORS
from ariadne import make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from dotenv import load_dotenv

# Import db and models
from .models import db
from .schema import type_defs, resolvers

load_dotenv()

migrate = Migrate()


def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration
    from config import config

    config_name = config_name or "default"
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # GraphQL Schema
    schema = make_executable_schema(type_defs, resolvers)

    # GraphQL Explorer (development)
    explorer_html = ExplorerGraphiQL().html(None)

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

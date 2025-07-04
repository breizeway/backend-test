from app import create_app, db
from app.models import User, Post
import os

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)


@app.before_first_request
def create_tables():
    print("Creating database tables...")
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

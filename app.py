import os
from app import create_app
from app.models import db, User, Post

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)


@app.cli.command()
def init_db():
    """Initialize the database."""
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")


# Create tables when app starts (for development)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)

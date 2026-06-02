"""Flask application factory for Mkulima Chapchap.

Run locally:
    flask --app app run --debug
or:
    python app.py
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, jwt, migrate
from routes.auth_routes import auth_bp
from routes.animal_routes import animals_bp
from routes.record_routes import records_bp
from routes.reminder_routes import reminders_bp


def create_app(config_class=Config):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Allow the React frontend to call the Flask API during local development.
    CORS(app, origins=[app.config["FRONTEND_URL"], "http://localhost:5173"], supports_credentials=True)

    # Initialize extensions.
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints.
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(animals_bp, url_prefix="/api")
    app.register_blueprint(records_bp, url_prefix="/api")
    app.register_blueprint(reminders_bp, url_prefix="/api")

    @app.get("/")
    def index():
        """Simple health check route."""
        return jsonify({"message": "Mkulima Chapchap Flask API is running."})

    @app.cli.command("create-db")
    def create_db_command():
        """Create database tables without using migrations."""
        db.create_all()
        print("Database tables created.")

    return app


app = create_app()

if __name__ == "__main__":
    # Debug=True is acceptable for a local student project only.
    app.run(debug=True)

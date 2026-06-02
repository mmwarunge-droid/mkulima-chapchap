"""Application extensions.

Keeping extensions in one file avoids circular imports between the app,
models, and route blueprints.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# SQLAlchemy database object used by all models.
db = SQLAlchemy()

# JWT manager handles token creation and protected route validation.
jwt = JWTManager()

# Flask-Migrate is optional for a bootcamp project, but useful for real projects.
migrate = Migrate()

"""Database models and simple serializers for Mkulima Chapchap."""

from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

# Many-to-many association table:
# many users can favorite many animals.
favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("animal_id", db.Integer, db.ForeignKey("animals.id"), primary_key=True),
)


class User(db.Model):
    """System user/farmer."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user can own many animals: one-to-many relationship.
    animals = db.relationship("Animal", back_populates="owner", cascade="all, delete-orphan")

    # Many users can favorite many animals: many-to-many relationship.
    favorite_animals = db.relationship(
        "Animal",
        secondary=favorites,
        back_populates="favorited_by",
    )

    def set_password(self, password):
        """Hash a plain password before saving it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Compare a plain password with the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize user data without exposing password_hash."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Animal(db.Model):
    """Animal owned by a farmer."""

    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(80), nullable=False)  # Cow, goat, sheep, chicken, etc.
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    status = db.Column(db.String(30), default="active")  # active or sold
    sale_price = db.Column(db.Float, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", back_populates="animals")
    weights = db.relationship("WeightRecord", back_populates="animal", cascade="all, delete-orphan")
    health_records = db.relationship("HealthRecord", back_populates="animal", cascade="all, delete-orphan")
    favorited_by = db.relationship("User", secondary=favorites, back_populates="favorite_animals")

    def to_dict(self, include_records=True, current_user=None):
        """Serialize an animal with optional child records."""
        data = {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "status": self.status,
            "sale_price": self.sale_price,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_favorite": bool(current_user and current_user in self.favorited_by),
        }
        if include_records:
            data["weights"] = [weight.to_dict() for weight in self.weights]
            data["health_records"] = [record.to_dict() for record in self.health_records]
        return data


class WeightRecord(db.Model):
    """Animal weight captured at a specific stage/date."""

    __tablename__ = "weight_records"

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animals.id"), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    measured_on = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    animal = db.relationship("Animal", back_populates="weights")

    def to_dict(self):
        """Serialize weight record."""
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "weight_kg": self.weight_kg,
            "measured_on": self.measured_on.isoformat() if self.measured_on else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class HealthRecord(db.Model):
    """Veterinary or farm management record for an animal."""

    __tablename__ = "health_records"

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey("animals.id"), nullable=False)
    record_type = db.Column(db.String(40), nullable=False)  # vaccination, deworming, medical, breeding
    title = db.Column(db.String(150), nullable=False)
    due_date = db.Column(db.Date)
    completed_on = db.Column(db.Date)
    cost = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    animal = db.relationship("Animal", back_populates="health_records")

    def to_dict(self):
        """Serialize health record."""
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "record_type": self.record_type,
            "title": self.title,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_on": self.completed_on.isoformat() if self.completed_on else None,
            "cost": self.cost,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

"""Animal CRUD routes.

All routes in this file are protected using JWT authentication.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Animal, User

animals_bp = Blueprint("animals", __name__)


def parse_date(value):
    """Convert YYYY-MM-DD text from the frontend into a Python date."""
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def current_user():
    """Get the logged-in user from the JWT identity."""
    return User.query.get_or_404(int(get_jwt_identity()))


def owned_animal_or_404(animal_id, user_id):
    """Return an animal only if it belongs to the logged-in user."""
    return Animal.query.filter_by(id=animal_id, owner_id=user_id).first_or_404()


@animals_bp.get("/animals")
@jwt_required()
def list_animals():
    """READ: List all animals owned by the logged-in farmer."""
    user = current_user()
    animals = Animal.query.filter_by(owner_id=user.id).order_by(Animal.created_at.desc()).all()
    return jsonify([animal.to_dict(include_records=False, current_user=user) for animal in animals]), 200


@animals_bp.post("/animals")
@jwt_required()
def create_animal():
    """CREATE: Add a new animal to farm records."""
    user = current_user()
    data = request.get_json() or {}

    if not data.get("name") or not data.get("species"):
        return jsonify({"error": "Animal name and species are required."}), 400

    animal = Animal(
        name=data.get("name"),
        species=data.get("species"),
        breed=data.get("breed"),
        gender=data.get("gender"),
        date_of_birth=parse_date(data.get("date_of_birth")),
        status=data.get("status", "active"),
        sale_price=float(data.get("sale_price") or 0),
        owner_id=user.id,
    )
    db.session.add(animal)
    db.session.commit()
    return jsonify(animal.to_dict(current_user=user)), 201


@animals_bp.get("/animals/<int:animal_id>")
@jwt_required()
def get_animal(animal_id):
    """READ: Get one animal with weights and health records."""
    user = current_user()
    animal = owned_animal_or_404(animal_id, user.id)
    return jsonify(animal.to_dict(current_user=user)), 200


@animals_bp.put("/animals/<int:animal_id>")
@jwt_required()
def update_animal(animal_id):
    """UPDATE: Edit an animal's details."""
    user = current_user()
    animal = owned_animal_or_404(animal_id, user.id)
    data = request.get_json() or {}

    animal.name = data.get("name", animal.name)
    animal.species = data.get("species", animal.species)
    animal.breed = data.get("breed", animal.breed)
    animal.gender = data.get("gender", animal.gender)
    animal.status = data.get("status", animal.status)
    animal.sale_price = float(data.get("sale_price", animal.sale_price) or 0)

    if "date_of_birth" in data:
        animal.date_of_birth = parse_date(data.get("date_of_birth"))

    db.session.commit()
    return jsonify(animal.to_dict(current_user=user)), 200


@animals_bp.delete("/animals/<int:animal_id>")
@jwt_required()
def delete_animal(animal_id):
    """DELETE: Remove an animal and all its related records."""
    user = current_user()
    animal = owned_animal_or_404(animal_id, user.id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deleted successfully."}), 200


@animals_bp.post("/animals/<int:animal_id>/favorite")
@jwt_required()
def favorite_animal(animal_id):
    """Many-to-many action: favorite an animal for quick tracking."""
    user = current_user()
    animal = Animal.query.get_or_404(animal_id)

    if animal not in user.favorite_animals:
        user.favorite_animals.append(animal)
        db.session.commit()

    return jsonify({"message": "Animal added to favorites.", "animal": animal.to_dict(current_user=user)}), 200


@animals_bp.delete("/animals/<int:animal_id>/favorite")
@jwt_required()
def unfavorite_animal(animal_id):
    """Many-to-many action: remove an animal from favorites."""
    user = current_user()
    animal = Animal.query.get_or_404(animal_id)

    if animal in user.favorite_animals:
        user.favorite_animals.remove(animal)
        db.session.commit()

    return jsonify({"message": "Animal removed from favorites.", "animal": animal.to_dict(current_user=user)}), 200

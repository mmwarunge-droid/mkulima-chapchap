"""Weight and health record routes.

These routes give the project proper CRUD operations beyond simple animal CRUD.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Animal, WeightRecord, HealthRecord

records_bp = Blueprint("records", __name__)


def parse_date(value):
    """Convert optional YYYY-MM-DD text into a Python date."""
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def get_owned_animal(animal_id):
    """Return an animal only if it belongs to the logged-in farmer."""
    user_id = int(get_jwt_identity())
    return Animal.query.filter_by(id=animal_id, owner_id=user_id).first_or_404()


def get_owned_health_record(record_id):
    """Return a health record only if it belongs to the logged-in farmer."""
    user_id = int(get_jwt_identity())
    return (
        HealthRecord.query.join(Animal)
        .filter(HealthRecord.id == record_id, Animal.owner_id == user_id)
        .first_or_404()
    )


def get_owned_weight_record(record_id):
    """Return a weight record only if it belongs to the logged-in farmer."""
    user_id = int(get_jwt_identity())
    return (
        WeightRecord.query.join(Animal)
        .filter(WeightRecord.id == record_id, Animal.owner_id == user_id)
        .first_or_404()
    )


@records_bp.get("/animals/<int:animal_id>/weights")
@jwt_required()
def list_weights(animal_id):
    """READ: List weight records for one animal."""
    animal = get_owned_animal(animal_id)
    return jsonify([weight.to_dict() for weight in animal.weights]), 200


@records_bp.post("/animals/<int:animal_id>/weights")
@jwt_required()
def create_weight(animal_id):
    """CREATE: Add an animal weight record."""
    animal = get_owned_animal(animal_id)
    data = request.get_json() or {}

    if not data.get("weight_kg"):
        return jsonify({"error": "weight_kg is required."}), 400

    weight = WeightRecord(
        animal_id=animal.id,
        weight_kg=float(data.get("weight_kg")),
        measured_on=parse_date(data.get("measured_on")) or datetime.utcnow().date(),
        notes=data.get("notes"),
    )
    db.session.add(weight)
    db.session.commit()
    return jsonify(weight.to_dict()), 201


@records_bp.delete("/weights/<int:record_id>")
@jwt_required()
def delete_weight(record_id):
    """DELETE: Remove a weight record."""
    weight = get_owned_weight_record(record_id)
    db.session.delete(weight)
    db.session.commit()
    return jsonify({"message": "Weight record deleted."}), 200


@records_bp.get("/animals/<int:animal_id>/health-records")
@jwt_required()
def list_health_records(animal_id):
    """READ: List health records for one animal."""
    animal = get_owned_animal(animal_id)
    return jsonify([record.to_dict() for record in animal.health_records]), 200


@records_bp.post("/animals/<int:animal_id>/health-records")
@jwt_required()
def create_health_record(animal_id):
    """CREATE: Add vaccination, deworming, medical, or breeding record."""
    animal = get_owned_animal(animal_id)
    data = request.get_json() or {}

    if not data.get("record_type") or not data.get("title"):
        return jsonify({"error": "record_type and title are required."}), 400

    record = HealthRecord(
        animal_id=animal.id,
        record_type=data.get("record_type"),
        title=data.get("title"),
        due_date=parse_date(data.get("due_date")),
        completed_on=parse_date(data.get("completed_on")),
        cost=float(data.get("cost") or 0),
        notes=data.get("notes"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@records_bp.put("/health-records/<int:record_id>")
@jwt_required()
def update_health_record(record_id):
    """UPDATE: Edit a health record or mark it as completed."""
    record = get_owned_health_record(record_id)
    data = request.get_json() or {}

    record.record_type = data.get("record_type", record.record_type)
    record.title = data.get("title", record.title)
    record.cost = float(data.get("cost", record.cost) or 0)
    record.notes = data.get("notes", record.notes)

    if "due_date" in data:
        record.due_date = parse_date(data.get("due_date"))
    if "completed_on" in data:
        record.completed_on = parse_date(data.get("completed_on"))

    db.session.commit()
    return jsonify(record.to_dict()), 200


@records_bp.delete("/health-records/<int:record_id>")
@jwt_required()
def delete_health_record(record_id):
    """DELETE: Remove a health record."""
    record = get_owned_health_record(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Health record deleted."}), 200

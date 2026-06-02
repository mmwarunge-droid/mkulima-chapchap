"""Dashboard reminder routes."""

from datetime import date, timedelta
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Animal, HealthRecord

reminders_bp = Blueprint("reminders", __name__)


@reminders_bp.get("/reminders")
@jwt_required()
def reminders():
    """Return pending health reminders due in the next 30 days."""
    user_id = int(get_jwt_identity())
    today = date.today()
    next_30_days = today + timedelta(days=30)

    records = (
        HealthRecord.query.join(Animal)
        .filter(
            Animal.owner_id == user_id,
            HealthRecord.completed_on.is_(None),
            HealthRecord.due_date.isnot(None),
            HealthRecord.due_date >= today,
            HealthRecord.due_date <= next_30_days,
        )
        .order_by(HealthRecord.due_date.asc())
        .all()
    )

    results = []
    for record in records:
        item = record.to_dict()
        item["animal_name"] = record.animal.name
        item["days_remaining"] = (record.due_date - today).days if record.due_date else None
        results.append(item)

    return jsonify(results), 200

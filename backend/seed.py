"""Seed script for sample data.

Run:
    python seed.py

This creates a demo farmer, animals, weight records, health records, and favorites.
"""

from datetime import date, timedelta
from app import create_app
from extensions import db
from models import User, Animal, WeightRecord, HealthRecord

app = create_app()

with app.app_context():
    print("Clearing old data...")
    db.drop_all()
    db.create_all()

    print("Creating users...")
    farmer = User(username="Demo Farmer", email="farmer@example.com")
    farmer.set_password("password123")

    neighbour = User(username="Neighbour Farmer", email="neighbour@example.com")
    neighbour.set_password("password123")

    db.session.add_all([farmer, neighbour])
    db.session.commit()

    print("Creating animals...")
    cow = Animal(
        name="Maziwa",
        species="Cow",
        breed="Friesian",
        gender="Female",
        date_of_birth=date(2023, 5, 12),
        owner_id=farmer.id,
    )
    goat = Animal(
        name="Kijana",
        species="Goat",
        breed="Galla",
        gender="Male",
        date_of_birth=date(2024, 2, 3),
        owner_id=farmer.id,
    )
    sheep = Animal(
        name="Pamba",
        species="Sheep",
        breed="Dorper",
        gender="Female",
        date_of_birth=date(2024, 8, 18),
        owner_id=neighbour.id,
    )
    db.session.add_all([cow, goat, sheep])
    db.session.commit()

    print("Creating weight records...")
    db.session.add_all([
        WeightRecord(animal_id=cow.id, weight_kg=350, measured_on=date.today() - timedelta(days=60), notes="Healthy growth."),
        WeightRecord(animal_id=cow.id, weight_kg=370, measured_on=date.today() - timedelta(days=10), notes="Good progress."),
        WeightRecord(animal_id=goat.id, weight_kg=38, measured_on=date.today() - timedelta(days=20), notes="Normal."),
    ])

    print("Creating health records...")
    db.session.add_all([
        HealthRecord(
            animal_id=cow.id,
            record_type="vaccination",
            title="FMD vaccination",
            due_date=date.today() + timedelta(days=7),
            cost=500,
            notes="Book vet visit before due date.",
        ),
        HealthRecord(
            animal_id=goat.id,
            record_type="deworming",
            title="Routine deworming",
            due_date=date.today() + timedelta(days=14),
            cost=200,
            notes="Use correct dosage by weight.",
        ),
        HealthRecord(
            animal_id=cow.id,
            record_type="breeding",
            title="Artificial insemination",
            completed_on=date.today() - timedelta(days=40),
            cost=1500,
            notes="Breeding cost recorded.",
        ),
    ])

    # Demonstrate many-to-many favorites.
    farmer.favorite_animals.append(cow)
    farmer.favorite_animals.append(sheep)

    db.session.commit()
    print("Seed complete!")
    print("Demo login: farmer@example.com / password123")

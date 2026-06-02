"""Authentication routes: register, login, logout, and profile."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User

# URL prefix is added in app.py: /api/auth
auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    """Create a new farmer account and return a JWT token."""
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Username, email and password are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered."}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Account created successfully.", "token": token, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    """Validate credentials and return a JWT token."""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful.", "token": token, "user": user.to_dict()}), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    """Stateless JWT logout.

    The backend confirms logout; the frontend removes the token from localStorage.
    """
    return jsonify({"message": "Logged out successfully. Remove the token on the client."}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    """Return the currently logged-in user."""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

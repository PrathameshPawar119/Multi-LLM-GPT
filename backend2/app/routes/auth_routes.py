from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.dbconnect import dbconnect

bp = Blueprint('auth', __name__)

auth_service = AuthService(dbconnect())

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status_code = auth_service.create_user(data['email'], data['password'])
    return jsonify(response), status_code

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    token, user_id = auth_service.login_user(data['email'], data['password'])
    if token:
        return jsonify({"token": token, "user_id": str(user_id)}), 200
    return jsonify({"message": "Invalid credentials"}), 401

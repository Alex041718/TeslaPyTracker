from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users)

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    result = UserService.create_user(user_data)
    if 'errors' in result:
        return jsonify(result[0]), result[1]
    return jsonify(result), 201

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    result = UserService.update_user(user_id, user_data)
    if isinstance(result, tuple) and len(result) == 2:
        return jsonify(result[0]), result[1]
    return jsonify(result)

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserService.delete_user(user_id)
    if isinstance(result, tuple) and len(result) == 2:
        return jsonify(result[0]), result[1]
    return jsonify(result)
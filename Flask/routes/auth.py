from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User, db
from werkzeug.security import check_password_hash

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and returns a JWT access token.
    Expected JSON:
    {
        "username": "your_username",
        "password": "your_password"
    }
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify the provided password against the stored hash
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create a new access token (optionally include additional claims)
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    """
    Registers a new user with an optional permission level.
    Expected JSON payload:
    {
        "username": "your_username",
        "password": "your_password",
        "permission": 1
    }
    """
    data = request.get_json()

    # Validate input
    username = data.get('username')
    password = data.get('password')
    permission = data.get('permission', 0)  # Default to '0' if not provided

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # For example, only allow a predefined list
    allowed_permissions = [0]
    if permission not in allowed_permissions:
        permission = 0

    # Create the new user (password will be hashed via the User model)
    new_user = User(username=username, password=password, permission=permission)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import User, db
from werkzeug.security import generate_password_hash

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    """
    Updates the currently authenticated user's details.
    
    Expected JSON payload:
    {
        "username": "new_username",      // Optional
        "password": "new_password",      // Optional
        "permission": 1           // Optional
    }
    
    Returns:
        JSON response indicating success or error.
    """
    current_user_id = get_jwt_identity()  # Retrieves the user ID from the JWT
    data = request.get_json()

    # Query the database for the current user
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update username if provided and ensure it's not already taken by someone else
    new_username = data.get('username')
    if new_username:
        if User.query.filter(User.username == new_username, User.id != current_user_id).first():
            return jsonify({"error": "Username already exists"}), 409
        user.username = new_username

    # Update password if provided (hash the new password)
    new_password = data.get('password')
    if new_password:
        user.password = generate_password_hash(new_password)

    # Update permission if provided, but restrict to allowed values
    new_permission = data.get('permission')
    if new_permission:
        allowed_permissions = [0]
        if new_permission not in allowed_permissions:
            return jsonify({"error": "Invalid permission level"}), 400
        user.permission = new_permission

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

@user_blueprint.route('/users/<int:user_id>/permission', methods=['PUT'])
@jwt_required()
def update_user_permission(user_id):
    """
    Updates the permission level (role) of a specified user.
    This endpoint should only be accessible to admin users.
    
    Expected JSON payload:
    {
        "permission": 1
    }
    """
    # Retrieve JWT claims to verify the role of the requestor
    claims = get_jwt()
    if claims.get('permission') != 1:
        return jsonify({"error": "Admins only"}), 403

    # Retrieve the new permission from the request
    data = request.get_json()
    new_permission = data.get('permission')
    allowed_permissions = [0,1,2,3,4,5]  # Define the allowed roles

    if not new_permission or new_permission not in allowed_permissions:
        return jsonify({"error": "Invalid or missing permission level"}), 400

    # Find the user to update
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update the user's permission (role)
    user.role = new_permission
    db.session.commit()

    return jsonify({"message": "User permission updated successfully"}), 200
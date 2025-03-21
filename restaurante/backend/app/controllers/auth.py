from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
import requests
from app.utils.validation import validate_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if not validate_email(data.get('email')):
        return jsonify({'message': 'Invalid email format'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'User already exists'}), 409
    
    user = User(
        email=data.get('email'),
        name=data.get('name', ''),
        phone=data.get('phone', '')
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    data = request.get_json()
    
    if not data or not data.get('id_token'):
        return jsonify({'message': 'Missing ID token'}), 400
    
    # TODO: Verify Google token with Google's API
    # For now, we'll mock this verification
    
    # Mock response data from Google
    google_user = {
        'sub': '123googleid456',
        'email': 'user@example.com',
        'name': 'Example User'
    }
    
    # Check if user exists
    user = User.query.filter_by(google_id=google_user['sub']).first()
    
    # If not, check by email
    if not user:
        user = User.query.filter_by(email=google_user['email']).first()
    
    # If still not, create new user
    if not user:
        user = User(
            google_id=google_user['sub'],
            email=google_user['email'],
            name=google_user['name']
        )
        db.session.add(user)
    else:
        # Update existing user's Google ID if they logged in with email before
        if not user.google_id:
            user.google_id = google_user['sub']
    
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    
    if data.get('name'):
        user.name = data.get('name')
    
    if data.get('phone'):
        user.phone = data.get('phone')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200
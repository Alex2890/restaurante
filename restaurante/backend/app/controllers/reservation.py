from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models.reservation import Reservation
from app.models.user import User
from datetime import datetime, timedelta

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('', methods=['GET'])
@jwt_required()
def get_reservations():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'admin' or user.role == 'staff':
        # For staff and admin, return all reservations
        reservations = Reservation.query.order_by(Reservation.date.desc(), Reservation.time.desc()).all()
    else:
        # For regular customers, return only their reservations
        reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.date.desc(), Reservation.time.desc()).all()
    
    return jsonify([reservation.to_dict() for reservation in reservations]), 200

@reservation_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_reservation(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    reservation = Reservation.query.get(id)
    
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404
    
    # Check if user is authorized to view this reservation
    if user.role != 'admin' and user.role != 'staff' and reservation.user_id != user_id:
        return jsonify({'message': 'Unauthorized to view this reservation'}), 403
    
    return jsonify(reservation.to_dict()), 200

@reservation_bp.route('', methods=['POST'])
def create_reservation():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'email', 'phone', 'date', 'time', 'party_size']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user is authenticated (optional)
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        pass
    
    # Parse date string to datetime
    try:
        reservation_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    
    # Create reservation
    reservation = Reservation(
        user_id=user_id,
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        date=reservation_date,
        time=data['time'],
        party_size=data['party_size'],
        occasion=data.get('occasion', ''),
        special_requests=data.get('special_requests', '')
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        'message': 'Reservation created successfully',
        'reservation': reservation.to_dict()
    }), 201

@reservation_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_reservation(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    reservation = Reservation.query.get(id)
    
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404
    
    # Check if user is authorized to update this reservation
    if user.role != 'admin' and user.role != 'staff' and reservation.user_id != user_id:
        return jsonify({'message': 'Unauthorized to update this reservation'}), 403
    
    data = request.get_json()
    
    # Update fields
    if data.get('name'):
        reservation.name = data['name']
    if data.get('email'):
        reservation.email = data['email']
    if data.get('phone'):
        reservation.phone = data['phone']
    if data.get('date'):
        try:
            reservation.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    if data.get('time'):
        reservation.time = data['time']
    if data.get('party_size'):
        reservation.party_size = data['party_size']
    if 'occasion' in data:
        reservation.occasion = data['occasion']
    if 'special_requests' in data:
        reservation.special_requests = data['special_requests']
    if data.get('status') and (user.role == 'admin' or user.role == 'staff'):
        reservation.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Reservation updated successfully',
        'reservation': reservation.to_dict()
    }), 200

@reservation_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    reservation = Reservation.query.get(id)
    
    if not reservation:
        return jsonify({'message': 'Reservation not found'}), 404
    
    # Check if user is authorized to delete this reservation
    if user.role != 'admin' and user.role != 'staff' and reservation.user_id != user_id:
        return jsonify({'message': 'Unauthorized to delete this reservation'}), 403
    
    db.session.delete(reservation)
    db.session.commit()
    
    return jsonify({'message': 'Reservation deleted successfully'}), 200

@reservation_bp.route('/availability', methods=['GET'])
def check_availability():
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    party_size = request.args.get('partySize')
    
    if not date_str or not time_str or not party_size:
        return jsonify({'message': 'Missing required parameters'}), 400
    
    try:
        reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        party_size = int(party_size)
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid date format or party size'}), 400
    
    # Here we would check our existing reservations against capacity
    # For simplicity, we'll just check if we have less than 5 reservations for this time
    existing_reservations = Reservation.query.filter_by(
        date=reservation_date,
        time=time_str,
    ).count()
    
    # Also factor in the requested party size
    has_capacity = existing_reservations < 5 and party_size <= 10
    
    return jsonify({
        'available': has_capacity,
        'message': 'Available' if has_capacity else 'Not available for the selected time and party size'
    }), 200
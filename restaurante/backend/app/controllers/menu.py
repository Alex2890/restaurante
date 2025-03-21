from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.menu import MenuItem
from app.models.user import User

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('', methods=['GET'])
def get_menu_items():
    # Get query parameters for filtering
    category = request.args.get('category')
    is_vegetarian = request.args.get('vegetarian')
    is_vegan = request.args.get('vegan')
    is_gluten_free = request.args.get('gluten_free')
    is_featured = request.args.get('featured')
    
    # Start with base query
    query = MenuItem.query.filter_by(is_active=True)
    
    # Apply filters
    if category:
        query = query.filter_by(category=category)
    if is_vegetarian == 'true':
        query = query.filter_by(is_vegetarian=True)
    if is_vegan == 'true':
        query = query.filter_by(is_vegan=True)
    if is_gluten_free == 'true':
        query = query.filter_by(is_gluten_free=True)
    if is_featured == 'true':
        query = query.filter_by(is_featured=True)
    
    # Get the items
    menu_items = query.order_by(MenuItem.category, MenuItem.name).all()
    
    return jsonify([item.to_dict() for item in menu_items]), 200

@menu_bp.route('/<int:id>', methods=['GET'])
def get_menu_item(id):
    menu_item = MenuItem.query.get(id)
    
    if not menu_item or not menu_item.is_active:
        return jsonify({'message': 'Menu item not found'}), 404
    
    return jsonify(menu_item.to_dict()), 200

@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(MenuItem.category).distinct().all()
    return jsonify([category[0] for category in categories]), 200

@menu_bp.route('/featured', methods=['GET'])
def get_featured_items():
    featured_items = MenuItem.query.filter_by(is_featured=True, is_active=True).all()
    return jsonify([item.to_dict() for item in featured_items]), 200

# Admin routes for menu management
@menu_bp.route('', methods=['POST'])
@jwt_required()
def create_menu_item():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admin can add menu items
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'price', 'category']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    menu_item = MenuItem(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        category=data['category'],
        image_url=data.get('image_url', ''),
        is_vegetarian=data.get('is_vegetarian', False),
        is_vegan=data.get('is_vegan', False),
        is_gluten_free=data.get('is_gluten_free', False),
        is_featured=data.get('is_featured', False)
    )
    
    db.session.add(menu_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Menu item created successfully',
        'menu_item': menu_item.to_dict()
    }), 201

@menu_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_menu_item(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admin can update menu items
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    menu_item = MenuItem.query.get(id)
    
    if not menu_item:
        return jsonify({'message': 'Menu item not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if data.get('name'):
        menu_item.name = data['name']
    if 'description' in data:
        menu_item.description = data['description']
    if data.get('price'):
        menu_item.price = data['price']
    if data.get('category'):
        menu_item.category = data['category']
    if 'image_url' in data:
        menu_item.image_url = data['image_url']
    if 'is_vegetarian' in data:
        menu_item.is_vegetarian = data['is_vegetarian']
    if 'is_vegan' in data:
        menu_item.is_vegan = data['is_vegan']
    if 'is_gluten_free' in data:
        menu_item.is_gluten_free = data['is_gluten_free']
    if 'is_featured' in data:
        menu_item.is_featured = data['is_featured']
    if 'is_active' in data:
        menu_item.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Menu item updated successfully',
        'menu_item': menu_item.to_dict()
    }), 200

@menu_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admin can delete menu items
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    menu_item = MenuItem.query.get(id)
    
    if not menu_item:
        return jsonify({'message': 'Menu item not found'}), 404
    
    # Instead of hard delete, we'll soft delete by setting is_active to False
    menu_item.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Menu item deleted successfully'}), 200
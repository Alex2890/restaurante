from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Enable CORS with specific settings
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.controllers.auth import auth_bp
    from app.controllers.reservation import reservation_bp
    from app.controllers.menu import menu_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(reservation_bp, url_prefix='/api/reservations')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app
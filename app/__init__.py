import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import models and create db instance
from .models import db, bcrypt

# Import auth utils
from .routes.auth import is_token_blacklisted

def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://splash25user:splash25password@localhost:5432/splash25_core_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000  # 30 days
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Configure CORS
    CORS(app, 
         resources={r"/api/*": {
             "origins": [
                 "http://localhost:3000",  # React dev server
                 "http://localhost:5173",  # Vite dev server
                 "http://localhost:8080",  # Vue dev server
                 "http://localhost:8081"   # Alternative dev server
             ],
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "supports_credentials": True,
             "allow_credentials": True,
             "expose_headers": ["Content-Type", "Authorization"]
         }})
    
    # Register token blacklist loader
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_blacklisted(jwt_header, jwt_payload)
    
    # Register blueprints
    from .routes import main, auth, buyer, seller, admin, system, timeslot, meeting, buyers
    from .routes.health import health_bp
    from .routes.stall import stall
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(buyer)
    app.register_blueprint(seller)
    app.register_blueprint(admin)
    app.register_blueprint(system)
    app.register_blueprint(timeslot)
    app.register_blueprint(meeting)
    app.register_blueprint(buyers)
    app.register_blueprint(stall)
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Create database tables (only if database is available)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Database not available - this is fine for testing configuration
            app.logger.warning(f"Database not available during initialization: {e}")
    
    return app

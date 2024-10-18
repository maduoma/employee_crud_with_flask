import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import Config
from .logging_config import setup_logging

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_class=Config):
    # Set up logging when the application starts
    setup_logging()
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions with the app instance
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints (routes)
    from app.routes.employee_routes import employee_bp
    app.register_blueprint(employee_bp)

    # Import models so Alembic can detect them
    from app.models import employee

    return app

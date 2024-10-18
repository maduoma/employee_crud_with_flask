from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Function to initialize database with Flask app
def init_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

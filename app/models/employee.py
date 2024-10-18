from app import db
from datetime import datetime, timezone

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    date_hired = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    profile_picture = db.Column(db.String(200), nullable=True)

    def __init__(self, name, email, position, salary, profile_picture=None):
        self.name = name
        self.email = email
        self.position = position
        self.salary = salary
        self.profile_picture = profile_picture

    def __repr__(self):
        return f"<Employee {self.name}>"

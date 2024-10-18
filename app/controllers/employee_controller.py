import re
from sqlalchemy.exc import SQLAlchemyError
from app.models.employee import Employee
from app import db

def is_valid_email(email):
    """Validate email format using a regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def get_all_employees(search_query=None):
    """Fetch all employee records from the database."""
    query = Employee.query
    if search_query:
        search = f'%{search_query}%'
        query = query.filter(
            Employee.name.ilike(search) |
            Employee.email.ilike(search) |
            Employee.position.ilike(search)
        )
    return query.all()

def get_employee_by_id(employee_id):
    """Fetch a single employee by ID."""
    return db.session.get(Employee, employee_id)

def create_employee(name, email, position, salary, profile_picture=None):
    """Create a new employee."""
    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    if Employee.query.filter_by(email=email).first():
        raise ValueError("Employee with this email already exists")

    new_employee = Employee(
        name=name,
        email=email,
        position=position,
        salary=float(salary),
        profile_picture=profile_picture
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    return new_employee

def update_employee(employee_id, name=None, email=None, position=None, salary=None, profile_picture=None):
    """Update an existing employee."""
    employee = get_employee_by_id(employee_id)
    if employee is None:
        raise ValueError("Employee not found")

    if email and email != employee.email:
        if not is_valid_email(email):
            raise ValueError("Invalid email format")
        if Employee.query.filter_by(email=email).first():
            raise ValueError("Another employee with this email already exists")
        employee.email = email

    if name:
        employee.name = name
    if position:
        employee.position = position
    if salary:
        employee.salary = float(salary)
    if profile_picture:
        employee.profile_picture = profile_picture

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    return employee

def delete_employee(employee_id):
    """Delete an employee by ID."""
    employee = get_employee_by_id(employee_id)
    if employee is None:
        raise ValueError("Employee not found")

    try:
        db.session.delete(employee)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
    return {"message": f"Employee {employee_id} deleted successfully"}

from datetime import datetime
from app.models.employee import Employee
from app import db
from flask import abort

def calculate_average_salary():
    """Calculate the average salary of all employees."""
    total_salary = db.session.query(db.func.sum(Employee.salary)).scalar()
    count = db.session.query(db.func.count(Employee.id)).scalar()
    if count == 0:
        return 0
    return total_salary / count

def update_hiring_date(employee_id, new_date):
    """Update the hiring date for an employee."""
    employee = db.session.get(Employee, employee_id)
    if employee is None:
        abort(404, description="Employee not found")

    try:
        new_date_parsed = datetime.strptime(new_date, '%Y-%m-%d')
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD.")

    employee.date_hired = new_date_parsed
    db.session.commit()
    return employee

def get_employees_hired_after(date_string):
    """Get a list of employees hired after a specific date."""
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD.")

    employees = Employee.query.filter(Employee.date_hired > date).all()
    return employees

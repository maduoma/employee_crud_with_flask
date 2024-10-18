import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from app.models.employee import Employee

@pytest.fixture
def test_client():
    # Set up the application for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory SQLite database
        "WTF_CSRF_ENABLED": False,
        "PRESERVE_CONTEXT_ON_EXCEPTION": False
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the tables
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Tear down the database

@pytest.fixture
def new_employee_data():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "position": "Software Engineer",
        "salary": 70000.0
    }

def test_create_employee(test_client, new_employee_data):
    # Test creating an employee via form submission
    response = test_client.post('/add', data=new_employee_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Employee created successfully!' in response.data
    # Verify employee is in the database
    with test_client.application.app_context():
        employee = Employee.query.filter_by(email="john.doe@example.com").first()
        assert employee is not None

def test_read_all_employees(test_client, new_employee_data):
    # Create an employee first
    test_client.post('/add', data=new_employee_data)

    # Simulate the AJAX request to fetch employees
    response = test_client.get('/search', query_string={'q': ''}, headers={'X-Requested-With': 'XMLHttpRequest'})
    assert response.status_code == 200

    # Parse the JSON response
    data = response.get_json()
    assert data is not None
    employees = data['employees']
    assert len(employees) > 0

    # Check if 'John Doe' is in the list of employees
    assert any(emp['name'] == 'John Doe' for emp in employees)


def test_update_employee(test_client, new_employee_data):
    # Create an employee first
    test_client.post('/add', data=new_employee_data)
    with test_client.application.app_context():
        employee = Employee.query.filter_by(email="john.doe@example.com").first()
        employee_id = employee.id
    # Test updating the employee
    update_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "position": "Senior Software Engineer",
        "salary": 80000.0
    }
    response = test_client.post(f'/edit/{employee_id}', data=update_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Employee updated successfully!' in response.data
    # Verify the employee is updated in the database
    with test_client.application.app_context():
        employee = db.session.get(Employee, employee_id)
        assert employee.name == "Jane Doe"
        assert employee.email == "jane.doe@example.com"

def test_delete_employee(test_client, new_employee_data):
    # Create an employee first
    test_client.post('/add', data=new_employee_data)
    with test_client.application.app_context():
        employee = Employee.query.filter_by(email="john.doe@example.com").first()
        employee_id = employee.id
    # Test deleting the employee
    response = test_client.post(f'/delete/{employee_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Employee deleted successfully!' in response.data
    # Verify employee no longer exists
    with test_client.application.app_context():
        employee = db.session.get(Employee, employee_id)
        assert employee is None
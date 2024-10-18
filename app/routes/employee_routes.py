from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename
import os

from app.controllers.employee_controller import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)

employee_bp = Blueprint('employee_bp', __name__)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@employee_bp.route('/', methods=['GET'])
def list_employees():
    """Show the employee directory page."""
    return render_template('index.html')

@employee_bp.route('/search', methods=['GET'])
def search_employees():
    """Handle Ajax search requests."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_query = request.args.get('q', '').strip()
        employees = get_all_employees(search_query)
        employees_data = []

        for emp in employees:
            employees_data.append({
                'id': emp.id,
                'name': emp.name,
                'email': emp.email,
                'position': emp.position,
                'salary': emp.salary,
                'date_hired': emp.date_hired.strftime('%Y-%m-%d %H:%M:%S'),
                'profile_picture': emp.profile_picture
            })

        return jsonify({'employees': employees_data})
    else:
        # Fallback to regular search if not an Ajax request
        return redirect(url_for('employee_bp.list_employees'))

@employee_bp.route('/add', methods=['GET', 'POST'])
def add_employee():
    """Handle adding a new employee."""
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        position = data.get('position')
        salary = data.get('salary')
        profile_picture = request.files.get('profile_picture')

        filename = None
        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(filepath)

        try:
            create_employee(name, email, position, salary, filename)
            flash('Employee created successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception:
            flash('An unexpected error occurred while creating the employee.', 'error')

        return redirect(url_for('employee_bp.list_employees'))

    return render_template('add_employee.html')

@employee_bp.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def modify_employee(employee_id):
    """Handle editing an employee."""
    employee = get_employee_by_id(employee_id)
    if not employee:
        flash('Employee not found!', 'error')
        return redirect(url_for('employee_bp.list_employees'))

    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        email = data.get('email')
        position = data.get('position')
        salary = data.get('salary')
        profile_picture = request.files.get('profile_picture')

        filename = employee.profile_picture  # Keep existing picture by default
        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(filepath)

        try:
            update_employee(employee_id, name, email, position, salary, filename)
            flash('Employee updated successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception:
            flash('An unexpected error occurred while updating the employee.', 'error')

        return redirect(url_for('employee_bp.list_employees'))

    return render_template('edit_employee.html', employee=employee)

@employee_bp.route('/delete/<int:employee_id>', methods=['POST'])
def remove_employee(employee_id):
    """Handle deleting an employee."""
    try:
        delete_employee(employee_id)
        flash('Employee deleted successfully!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception:
        flash('An unexpected error occurred while deleting the employee.', 'error')
    return redirect(url_for('employee_bp.list_employees'))

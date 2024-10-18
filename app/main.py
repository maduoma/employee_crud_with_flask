from app import create_app, db
from flask import render_template
from app.models.employee import Employee

app = create_app()

# Define Root Route
@app.route('/')
def home():
    """Render the home page displaying employee records."""
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Run the application
if __name__ == "__main__":
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    app.run(debug=True)
# Employee CRUD Application with Flask

## Overview

This project is a web-based CRUD (Create, Read, Update, Delete) application for managing employee information. It is developed using Flask, SQLAlchemy, and Jinja2 templating, with additional support for JavaScript, CSS, and Bootstrap for frontend functionality and styling.

The application allows users to manage employee details such as their name, email, position, salary, and profile picture. The interface is designed to be simple, intuitive, and responsive, ensuring usability across desktop and mobile devices.

## Features

- **Add Employee**: Create a new employee by filling out a form with personal and professional information.
- **View Employee List**: Display all employees in a tabular format, with profile pictures, and provide options to edit or delete each employee.
- **Edit Employee**: Update the information of existing employees.
- **Delete Employee**: Remove an employee from the system.
- **Search Functionality**: Search for employees based on name or other identifying details.
- **User Interface**: A clean and user-friendly UI, utilizing Bootstrap for responsive layout and components.

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Jinja2 Templating
- **Database**: PostgreSQL (or SQLite for testing)
- **Testing**: Pytest
- **CI/CD**: GitHub Actions for automated testing and deployment

## Prerequisites

- Python 3.8+
- PostgreSQL Database (or SQLite for local development)
- Git (for version control)
- Docker (optional, for containerization)

## Installation and Setup

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/your-username/employee_crud_with_flask.git
$ cd employee_crud_with_flask
```

### Step 2: Set Up Virtual Environment
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
$ pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the root directory with the following content:

```
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/employee_db
SECRET_KEY=your_secret_key
```

### Step 5: Database Migration
Initialize the database and run migrations:
```bash
$ flask db init
$ flask db migrate -m "Initial migration."
$ flask db upgrade
```

### Step 6: Run the Application
```bash
$ flask run
```
Visit `http://127.0.0.1:5000` in your browser to see the app in action.

## Testing

Unit tests have been set up using Pytest. To run the tests:
```bash
$ pytest tests/test_employee.py
```
Ensure that all tests pass to verify the core functionalities of the application.

## CI/CD with GitHub Actions
This project uses GitHub Actions for CI/CD. The GitHub Actions workflow is set up to automatically:
- Install dependencies
- Run tests
- Deploy to your chosen platform (e.g., Docker Hub, AWS, or Heroku)

### GitHub Actions Workflow File
A typical `.github/workflows/main.yml` file might look like this:

```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest tests/test_employee.py

    - name: Deploy to Heroku
      if: github.ref == 'refs/heads/main'
      run: |
        # Add your deployment commands here (e.g., using Heroku CLI or Docker)
```

## Project Structure

```
employee_crud_with_flask/
|— app/
    |— __init__.py
    |— config.py
    |— logging_config.py
    |— models/
        |— employee.py
    |— controllers/
        |— employee_controller.py
    |— routes/
        |— employee_routes.py
    |— templates/
        |— base.html
        |— add_employee.html
        |— edit_employee.html
        |— index.html
    |— static/
        |— css/
            |— style.css
        |— js/
            |— main.js
|— migrations/
|— tests/
    |— test_employee.py
|— .gitignore
|— requirements.txt
|— Dockerfile
|— docker-compose.yml
|— .env
|— README.md
```

## Docker Deployment

To run the app using Docker, follow these steps:

### Step 1: Build the Docker Image
```bash
$ docker build -t employee_crud_app .
```

### Step 2: Run the Docker Container
```bash
$ docker run -p 5000:5000 employee_crud_app
```

### Step 3: Access the Application
Visit `http://127.0.0.1:5000` in your browser.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss proposed changes.

## Authors
- Maduabughichi Achilefu (aachilefu@yahoo.com)

## Acknowledgments
- Flask Documentation
- SQLAlchemy Documentation
- Bootstrap 5 for frontend components.


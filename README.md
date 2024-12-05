# Ecommerce Shop API

## Project Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Installation Steps
1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## API Documentation
Access Swagger documentation at: `http://localhost:8000/api/docs/`

## Features
- Product CRUD operations
- Shopping Cart management
- Admin product management
- Authentication for cart and admin operations

## Running Tests
```bash
python manage.py test
```

# Django Skill App

A simple tweet app built with Django to handle user authentication, tweet creation, and management.

## Features

- User registration and login
- Post tweets
- View all tweets
- User profile management

## Requirements

- Python 3.x
- Django 4.x
- PostgreSQL (or any other database you prefer)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/django-tweet-app.git
cd django-tweet-app
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate  # For Linux/macOS
```

```powershell
py -m venv env
env\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database
Make sure you have PostgreSQL installed and create a database for the app.

Update DATABASES settings in settings.py with your database credentials:
python

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the server
```bash
python manage.py runserver
```


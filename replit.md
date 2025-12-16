# Pet Shop Amigo

## Overview
A Django-based website for a pet shop business in Brazil. The site includes:
- Home page with services overview
- Services listing
- About page
- Contact page
- Admin panel for managing services and testimonials

## Tech Stack
- Python 3.11
- Django 5.2.9
- SQLite database
- Gunicorn for production

## Project Structure
```
/
├── apps/               # Django applications
│   ├── admin_panel/    # Custom admin panel
│   ├── pages/          # Static pages (home, about, contact)
│   └── services/       # Services management
├── core/               # Django project settings
├── static/             # CSS and static files
├── templates/          # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Running the Project
- Development: `python manage.py runserver 0.0.0.0:5000`
- Production: `gunicorn --bind=0.0.0.0:5000 --reuse-port core.wsgi:application`

## Database
Using SQLite (`db.sqlite3`). Run migrations with:
```
python manage.py migrate
```

## Recent Changes
- December 16, 2025: Initial setup for Replit environment
  - Installed Python 3.11 and dependencies
  - Fixed requirements.txt encoding
  - Ran database migrations
  - Configured workflow for development server
  - Set up deployment configuration

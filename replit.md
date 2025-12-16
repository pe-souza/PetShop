# Pet Shop Amigo - Sistema de Gestão

## Overview
A comprehensive Django-based pet shop management system with:
- Client/pet registration and management
- Service management with duration tracking
- Professional staff scheduling with availability and time-off
- Intelligent appointment booking with conflict prevention
- Calendar view for agenda management
- Dashboard with reports and statistics
- WhatsApp API integration for automated notifications (Twilio ready)
- Public online booking page for customers

## Tech Stack
- Python 3.11
- Django 5.2.9
- SQLite database (development)
- PostgreSQL (production ready)
- Gunicorn for production
- FullCalendar.js for agenda visualization

## Project Structure
```
/
├── clientes/           # Client management app
├── pets/               # Pet management app
├── servicos/           # Service management app
├── profissionais/      # Staff scheduling app
├── agendamentos/       # Appointment booking app
├── relatorios/         # Reports and analytics app
├── whatsapp/           # WhatsApp API integration app
├── admin_panel/        # Custom admin dashboard
├── pages/              # Public pages (home, about, contact, booking)
├── core/               # Django project settings
├── static/             # CSS and static files
├── templates/          # HTML templates
│   ├── admin_panel/    # Admin panel templates
│   ├── pages/          # Public page templates
│   └── services/       # Service listing template
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Key Features

### Admin Panel (/admin-panel/)
- Login: admin / admin123
- Dashboard with statistics
- Client CRUD with search
- Pet CRUD linked to clients
- Service management with duration
- Professional management with schedules
- Calendar view for appointments
- Appointment creation with conflict detection
- WhatsApp message templates
- Reports dashboard

### Public Pages
- Home page (/)
- Services list (/servicos/)
- Online booking (/agendar/)
- About page (/sobre/)
- Contact page (/contato/)

### WhatsApp Integration (Twilio)
- **Fully configured with Twilio API**
- WhatsApp number: 5511949694654
- Required secrets (configured in Replit Secrets):
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
  - TWILIO_WHATSAPP_FROM
- Message templates for: confirmations, reminders, cancellations
- Variable substitution: {cliente_nome}, {pet_nome}, {servico_nome}, {data}, {hora}
- Automatic confirmation on appointment creation
- Automatic cancellation notification on status change

## Running the Project
- Development: `python manage.py runserver 0.0.0.0:5000`
- Production: `gunicorn --bind=0.0.0.0:5000 --reuse-port core.wsgi:application`

## Database
Using SQLite (`db.sqlite3`). Run migrations with:
```
python manage.py makemigrations
python manage.py migrate
```

## User Preferences
- Language: Portuguese (Brazil)
- Interface: Professional, responsive design
- WhatsApp integration priority

## Recent Changes
- December 16, 2025: Twilio WhatsApp Integration Completed
  - Fully integrated Twilio API for WhatsApp messaging
  - Updated all templates with correct WhatsApp number (5511949694654)
  - Automatic appointment confirmations via WhatsApp
  - Automatic cancellation notifications via WhatsApp
  - Automatic reminders via WhatsApp
  - Added twilio package to requirements.txt

- December 16, 2025: Major restructure and feature expansion
  - Reorganized apps from /apps/ folder to root level
  - Added client management (clientes app)
  - Added pet management linked to clients (pets app)
  - Enhanced services with duration tracking
  - Added professional staff management with schedules (profissionais app)
  - Added appointment booking with conflict prevention (agendamentos app)
  - Added reports dashboard (relatorios app)
  - Added WhatsApp integration with Twilio (whatsapp app)
  - Created public online booking page
  - Updated admin panel with all new features
  - Created comprehensive templates for all views

# Kabon-Hotel Online Services Management System

A modern, responsive, and secure Hotel Online Services Management System built with Django REST Framework and React.

## Features

### Visitor Features
- Public Home page with hotel introduction
- User Registration & Login with JWT authentication
- Protected pages: Services, Gallery, Facilities, Accommodation, Restaurant, Events, Contact, About, Profile
- Image gallery with search and filtering
- Responsive design with Tailwind CSS

### Administrator Features
- Secure admin dashboard with role-based access
- Manage services, categories, facilities, amenities
- Upload and manage gallery images
- Manage accommodation, restaurant, events, contact info
- User management and activity logging
- Publish/unpublish services

## Tech Stack

- **Backend:** Django, Django REST Framework, SQLite, JWT Authentication
- **Frontend:** React, Vite, Tailwind CSS, React Router, Axios
- **Documentation:** DRF Spectacular (OpenAPI/Swagger)
- **Deployment:** Docker, Docker Compose

## Project Structure

```
kabon-hotel/
├── docker-compose.yml
├── .env
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── kabon_hotel/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── api/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── permissions.py
│       └── admin.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── tailwind.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── components/
        ├── pages/
        ├── layouts/
        ├── context/
        ├── hooks/
        └── services/
```

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### Run the Application

```bash
# Clone or navigate to the project directory
cd kabon-hotel

# Build and start all services
docker compose up --build

# If Docker shows a permission error for /var/run/docker.sock, run:
# sudo usermod -aG docker $USER
# newgrp docker

# Access the application
Frontend: http://localhost:5173
Backend API: http://localhost:8000/api
API Documentation: http://localhost:8000/api/schema/swagger-ui/
Admin Panel: http://localhost:8000/admin/
```

### Create Superuser (Admin)

```bash
docker exec -it kabon-backend python manage.py createsuperuser
```

### Development Setup (without Docker)

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT)
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/user/` - Current user info

### Public
- `GET /api/home/` - Homepage content
- `GET /api/contact/` - Contact information

### Protected (Requires Authentication)
- `GET /api/services/` - List all services
- `GET /api/services/<id>/` - Service detail
- `GET /api/categories/` - Service categories
- `GET /api/gallery/` - Gallery images
- `GET /api/facilities/` - Hotel facilities
- `GET /api/accommodation/` - Accommodation types
- `GET /api/restaurant/` - Restaurant & dining info
- `GET /api/events/` - Events & conference facilities
- `GET /api/about/` - About us

### Admin (Requires Admin Role)
- `GET /api/admin/dashboard/` - Dashboard statistics
- `GET /api/admin/users/` - Manage users
- All CRUD operations for services, categories, gallery, facilities, etc.

## Database Models

1. **User** - Extended Django user with roles
2. **ServiceCategory** - Categories for hotel services
3. **HotelService** - Hotel services and amenities
4. **Gallery** - Image gallery
5. **Facility** - Hotel facilities
6. **Restaurant** - Restaurant and dining information
7. **Accommodation** - Accommodation types
8. **EventFacility** - Events and conference facilities
9. **ContactInformation** - Hotel contact details
10. **HomePageContent** - Homepage content management

## Authentication & Authorization

- JWT-based authentication using Django REST Framework SimpleJWT
- Role-based access control (Guest, Registered Client, Administrator)
- Protected React routes and Django API endpoints
- Password hashing with Django's default hasher
- CSRF protection and CORS configuration

## License

MIT License

## Production deployment on Render

This repository is configured for a Render Python web service. The `render.yaml`
Blueprint creates a web service and a PostgreSQL database. It also declares the
required environment variables; secret values marked `sync: false` must be
entered in the Render dashboard.

### Render settings

- **Build command:** `./build.sh`
- **Start command:** `gunicorn kabon_hotel.wsgi:application --bind 0.0.0.0:$PORT`
- **Health check:** `/health/`
- **Python:** `3.11.11` (also recorded in `runtime.txt`)
- **Database:** Render PostgreSQL through `DATABASE_URL`
- **Media:** Cloudinary through `CLOUDINARY_URL`; Render disks are not used

The build script runs `collectstatic`, applies migrations, and runs Django's
deployment checks. Do not use SQLite or `runserver` in production: Render's
filesystem is ephemeral and SQLite is not suitable for a multi-process web
service. Do not commit `.env`; copy `.env.example` only as a variable checklist.

### Required production environment variables

Set `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`,
`CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `CLOUDINARY_URL`,
`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and
`DEFAULT_FROM_EMAIL`. The frontend origin must be exactly
`https://kabon-hotel1-frontend.vercel.app` without a trailing slash.

After the first deploy, create an admin account from a one-off Render shell:

```text
python manage.py createsuperuser
```

Useful production URLs are `/health/`, `/api/`, `/api/schema/swagger-ui/`, and
`/admin/`.

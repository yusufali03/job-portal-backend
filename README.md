# Job Portal Backend

Backend API for the Job Portal Web Application built for a university exam project.

This project is developed using:

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular (Swagger/OpenAPI)

## Features

The backend supports:

- Custom user model with roles
  - Applicant
  - Employer
  - Admin
- JWT authentication
- Role-based access control
- Applicant and employer profile management
- Job creation and management
- Job applications
- Employer dashboard summary API
- Swagger/OpenAPI documentation
- File uploads for applicant profile image and resume

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT
- drf-spectacular
- django-filter
- django-cors-headers

## Project Structure

```bash
JobPortalBackend/
├── apps/
│   ├── users/
│   ├── profiles/
│   ├── jobs/
│   └── applications/
├── JobPortalBackend/
├── manage.py
├── requirements.txt
└── .env
```


## Installation
### 1. Clone the repository

```bash
git clone <your-backend-repo-url>
cd JobPortalBackend
```

### 2. Create virtual environment

```bash
python -m venv .venv

```
### 3. Activate virtual environment
Windows
```bash
.venv\Scripts\activate
```
macOS / Linux
```bash
source .venv/bin/activate
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```
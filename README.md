# Scribly

Scribly is a web application for managing and publishing articles, built with Django and Django REST Framework (DRF).

---

## Features

- User registration and authentication with JWT  
- Create, update, delete, and view articles  
- Secure API endpoints with JWT authentication  
- Password reset functionality  
- Profile management

---

## Prerequisites

- Python   
- Django   
- Django REST Framework  
- Django REST Framework SimpleJWT  
- Pillow  
---

## Installation

1. Clone the repository:

   git clone https://github.com/aliakhy/scribly-api.git
   
   cd scribly-api
   
3. Create  a virtual environment:

python -m venv env

.\env\Scripts\activate

3. Install dependencies:

cd scribly_api

pip install -r requirements.txt

4. Apply migrations:
   
pythom manage.py makemigrations

python manage.py migrate

6. Run the development server:

python manage.py runserver


## Usage

###  User Management

- `POST /accounts/register/` – Register   
- `POST /accounts/login/` –  JWT access and refresh tokens  
- `POST /accounts/token-refresh/` – Refresh  access   
- `POST /accounts/logout/` – Log out and blacklist the refresh token  
- `GET /accounts/protected/` – Access a protected view 
- `GET /accounts/profile/` – Retrieve user profile (requires authentication)  
- `POST /accounts/profile/change-password/` – Change password (requires authentication)  

### Password Reset 

- `POST /accounts/password-reset/` – password reset with email  
- `POST /accounts/password-reset/confirm/<uidb64>/<token>/` –  set new password  

### Article Management

- `/articles/` – a view set


















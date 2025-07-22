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

- Python 3.8 or higher  
- Django 4.x  
- Django REST Framework  
- Django REST Framework SimpleJWT  
- Pillow  
---

## Installation

1. Clone the repository:

   git clone https://github.com/username/scribly.git
   cd scribly
   
Create  a virtual environment:


python -m venv env
.\env\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

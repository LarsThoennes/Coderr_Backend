## Coderr_Backend

**Coderr Backend** is the server-side application for a freelancer platform where business users can offer services (e.g. app or website development) and customer users can purchase these offers and leave reviews.

---

## Technologies
- **Python**
- **Django**
- **Django REST Framework**

---

## Features
- User registration & authentication (customer & business users)
- Offer creation and management by business users
- Order creation by customers
- Review system for completed orders
- Public platform statistics endpoint
- RESTful API architecture
  
---

Installation

## 1. Clone the repository
```bash
git clone https://github.com/LarsThoennes/Coderr_Backend
cd Coderr_Backend

```
## Create a virtual environment
```bash
python -m venv venv
```
## Activate the environment

## macOS/Linux
```bash
source venv/bin/activate
```
## Windows
```bash
venv\Scripts\activate
```
## Install dependencies
```bash
pip install -r requirements.txt
```

## Create migrations
```bash
python manage.py makemigrations
```
## Apply migrations
```bash
python manage.py migrate
```
## (Optional) Create a superuser for the admin panel
```bash
python manage.py createsuperuser
```
## Run the Development Server
```bash
python manage.py runserver
```
## The server will start at:
```bash
http://127.0.0.1:8000/
```

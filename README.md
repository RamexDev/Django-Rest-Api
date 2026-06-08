# Products API

A robust Django Rest Framework (DRF) based API for managing products, users, and orders. This project implements a full e-commerce backend with asynchronous task processing and caching.

## 🚀 Features

- **Product Management**: List, retrieve, create, and update products with support for filtering, searching, and ordering.
- **Order Processing**: Complex order creation with atomic transactions and multi-item support.
- **Asynchronous Tasks**: Integrated with Celery and Redis to handle order confirmation emails in the background.
- **Caching**: Redis-backed caching for high-performance product and order list endpoints.
- **Authentication**: JWT-based authentication using `djangorestframework-simplejwt`.
- **Throttling**: Scoped rate limiting to prevent API abuse (`product` and `orders` scopes).
- **API Documentation**: OpenApi 3.0 schema generation using `drf-spectacular`.
- **Performance Monitoring**: Integrated with `django-silk` for request and database profiling.

## 🛠 Tech Stack

- **Framework**: Django 6.0+, Django Rest Framework (DRF)
- **Database**: SQLite (Default)
- **Cache/Broker**: Redis
- **Task Queue**: Celery
- **Auth**: SimpleJWT
- **Filtering**: Django Filter

## 📦 Installation & Setup

### Prerequisites
- Python 3.14+
- Redis server (running on `localhost:6379`)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Running Celery Worker
In a separate terminal:
```bash
cd backend
source venv/bin/activate
celery -A api worker --loglevel=info
```

## 🛣 API Endpoints

### Products
- `GET /products/` - List all products (Public)
- `POST /products/` - Create a product (Admin only)
- `GET /products/info/` - Summary statistics of products (Public)
- `GET /products/<id>/` - Get product details (Public)
- `PUT/PATCH/DELETE /products/<id>/` - Update or delete product (Admin only)

### Orders
- `GET /orders/` - List orders (Authenticated)
- `POST /orders/` - Create a new order (Authenticated)
- `GET /orders/<id>/` - Retrieve specific order (Authenticated)
- `PUT/PATCH /orders/<id>/` - Update order (Authenticated)
- `DELETE /orders/<id>/` - Cancel/Delete order (Authenticated)

### Users
- `GET /users/` - List users (Admin/Authenticated)

## ⚙️ Configuration
The project is configured to use:
- **JWT Access Token Lifetime**: 60 minutes
- **JWT Refresh Token Lifetime**: 1 day
- **Redis DB**: Index 1 for both caching and Celery broker.
- **Email**: Console backend (outputs emails to the terminal).

## 🧪 Testing
Run the test suite using:
```bash
cd backend
python manage.py test
```

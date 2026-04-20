# Coderr Backend API

A Django REST Framework backend for a freelancer platform where business users can offer services and customers can place orders and leave reviews.

---

## Tech Stack

- Python 3.10
- Django 5.2
- Django REST Framework
- SQLite (development)
- Token Authentication

---

## Features

- User registration and login with token authentication
- Two user types: `customer` and `business`
- Business users can create, update and delete offers with three detail packages (basic, standard, premium)
- Customers can place orders based on offer details
- Customers can leave reviews for business users
- Aggregated platform statistics via base-info endpoint

---

## Project Structure

```
coderr/
├── core/                   # Project settings and main URLs
│   ├── settings.py
│   ├── urls.py
│   └── views.py            # base-info endpoint
├── users_app/              # User registration, login and profiles
│   └── api/
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── permissions.py
├── offers_app/             # Offers and offer details
│   └── api/
├── orders_app/             # Orders
│   └── api/
├── reviews_app/            # Reviews
│   └── api/
└── manage.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd coderr
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```
SECRET_KEY='your-secret-key-here'
```

Generate a new secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login and receive token |

### Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile/{pk}/` | Get user profile |
| PATCH | `/api/profile/{pk}/` | Update user profile |
| GET | `/api/profiles/business/` | List all business profiles |
| GET | `/api/profiles/customer/` | List all customer profiles |

### Offers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/offers/` | List all offers |
| POST | `/api/offers/` | Create a new offer (business only) |
| GET | `/api/offers/{id}/` | Get offer details |
| PATCH | `/api/offers/{id}/` | Update an offer (owner only) |
| DELETE | `/api/offers/{id}/` | Delete an offer (owner only) |
| GET | `/api/offerdetails/{id}/` | Get offer detail |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List all orders |
| POST | `/api/orders/` | Create a new order (customer only) |
| PATCH | `/api/orders/{id}/` | Update order status (business only) |
| DELETE | `/api/orders/{id}/` | Delete an order (admin only) |
| GET | `/api/order-count/{business_user_id}/` | Get in-progress order count |
| GET | `/api/completed-order-count/{business_user_id}/` | Get completed order count |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviews/` | List all reviews |
| POST | `/api/reviews/` | Create a review (customer only) |
| PATCH | `/api/reviews/{id}/` | Update a review (owner only) |
| DELETE | `/api/reviews/{id}/` | Delete a review (owner only) |

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/base-info/` | Get platform statistics |

---

## Authentication

This API uses Token Authentication. Include the token in the request header:

```
Authorization: Token <your-token>
```

---

## Running Tests

```bash
python manage.py test
```

For test coverage:

```bash
coverage run manage.py test
coverage report
```

Current test coverage: **97%**

---

## Notes

- An offer must always contain exactly 3 details: `basic`, `standard` and `premium`
- A customer can only leave one review per business user
- Only business users can create offers
- Only customers can create orders
- Only the business user assigned to an order can update its status
- Order deletion is restricted to admin users

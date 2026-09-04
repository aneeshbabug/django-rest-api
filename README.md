# Django REST API

A RESTful API built with **Django** and **Django REST Framework** for user registration and item management.

The project implements **JWT authentication**, CRUD operations, and custom authorization using **administrator and item-owner permissions**.

---

## Features

- User registration
- JWT authentication
- Access and refresh tokens
- JWT refresh-token blacklisting for logout
- Authenticated API access
- Item creation and retrieval
- Item update and deletion
- Custom administrator permissions
- Custom item-owner permissions
- Admin + owner authorization for modifying and deleting items
- Password hashing using Django's authentication system
- Environment variable support for sensitive configuration

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| Simple JWT | JWT authentication |
| SQLite | Database |
| python-dotenv | Environment variable management |

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication.

### Authentication Flow

```text
Register
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Use Access Token for protected endpoints
   ↓
Access Token expires
   ↓
Use Refresh Token
   ↓
Receive New Access Token
```

Users can also log out by **blacklisting their refresh token**.

### Using the Access Token

Include the access token in the `Authorization` header when accessing protected endpoints:

```http
Authorization: Bearer <access-token>
```

---

## Authorization

The project uses custom Django REST Framework permissions to control access to item modification and deletion.

For `PUT`, `PATCH`, and `DELETE`, the user must satisfy **all three conditions**:

```text
Authenticated
      +
   Admin
      +
Item Owner
      ↓
Access Granted
```

### Permission Matrix

| User | Item Owner | Admin | PUT / PATCH / DELETE |
|---|:---:|:---:|:---:|
| Unauthenticated | — | — | ❌ |
| Normal user | Yes | No | ❌ |
| Normal user | No | No | ❌ |
| Admin | Yes | Yes | ✅ |
| Admin | No | Yes | ❌ |

This ensures that being an administrator alone is **not enough** to modify or delete another user's item.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register a new user | Not required |
| `POST` | `/api/auth/token/` | Obtain JWT access and refresh tokens | Not required |
| `POST` | `/api/auth/token/refresh/` | Refresh an access token | Not required |
| `POST` | `/api/auth/logout/` | Blacklist refresh token | Required |

### Items

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/api/items/` | Retrieve all items | Required |
| `POST` | `/api/items/` | Create an item | Required |
| `GET` | `/api/items/<id>/` | Retrieve a specific item | Required |
| `PUT` | `/api/items/<id>/` | Fully update an item | Admin + Owner |
| `PATCH` | `/api/items/<id>/` | Partially update an item | Admin + Owner |
| `DELETE` | `/api/items/<id>/` | Delete an item | Admin + Owner |

---

# API Usage Examples

## 1. Register a User

### Request

```http
POST /api/auth/register/
Content-Type: application/json
```

```json
{
    "username": "john",
    "password": "password123"
}
```

### Successful Response

```json
{
    "message": "User added Successfully"
}
```

Newly registered users are created as **non-admin users**.

---

## 2. Login

### Request

```http
POST /api/auth/token/
Content-Type: application/json
```

```json
{
    "username": "john",
    "password": "password123"
}
```

### Response

```json
{
    "refresh": "your-refresh-token",
    "access": "your-access-token"
}
```

The returned access token is used to authenticate requests to protected endpoints.

```http
Authorization: Bearer <access-token>
```

---

## 3. Create an Item

### Request

```http
POST /api/items/
Authorization: Bearer <access-token>
Content-Type: application/json
```

```json
{
    "name": "Laptop",
    "price": 75000,
    "description": "Development laptop"
}
```

The item's owner is automatically assigned to the **authenticated user**.

The client cannot choose or change the owner through the API.

---

## 4. Retrieve Items

### Request

```http
GET /api/items/
Authorization: Bearer <access-token>
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Laptop",
        "price": 75000,
        "description": "Development laptop"
    }
]
```

---

## 5. Update an Item

### PUT — Full Update

```http
PUT /api/items/1/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Requires:

```text
Authenticated + Admin + Owner
```

`PUT` replaces the complete item data.

### PATCH — Partial Update

```http
PATCH /api/items/1/
Authorization: Bearer <access-token>
Content-Type: application/json
```

Requires:

```text
Authenticated + Admin + Owner
```

`PATCH` allows partial updates to an item.

---

## 6. Delete an Item

### Request

```http
DELETE /api/items/1/
Authorization: Bearer <access-token>
```

Requires:

```text
Authenticated + Admin + Owner
```

---

# Project Structure

```text
django-rest-api/
│
├── backend/
|   |  
|   ├── manage.py
|   |
|   ├── api/
|   │   ├── migrations/
|   │   ├── admin.py
|   │   ├── apps.py
|   │   ├── models.py
|   │   ├── permissions.py
|   │   ├── serializer.py
|   │   ├── tests.py
|   │   ├── urls.py
|   │   └── views.py
|   │
|   └── backend/
|       ├── settings.py
|       ├── urls.py
|       ├── asgi.py
|       └── wsgi.py
|
├── .gitignore
├── requirements.txt
└── .env
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/aneeshbabug/django-rest-api.git
cd django-rest-api
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the same directory as `manage.py`.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

> **Important:** Never commit your `.env` file to GitHub.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

## 5. Run Database Migrations

```bash
python manage.py migrate
```

## 6. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

# Environment Variables

The project uses environment variables to keep sensitive configuration outside the source code.

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Django debug mode | `True` |

---

# Security

The project follows several basic security practices:

- Django's built-in password hashing is used when creating users.
- The Django `SECRET_KEY` is stored outside the source code.
- `.env` is excluded from Git.
- SQLite database files are excluded from Git.
- Users cannot assign themselves administrator privileges during registration.
- Item ownership is automatically assigned to the authenticated user.
- Item ownership cannot be changed through the serializer.
- JWT authentication protects API endpoints.
- Modification and deletion require both administrator and ownership permissions.

---

# Future Improvements

Possible future improvements include:

- [ ] Automated API tests
- [ ] API documentation with Swagger / OpenAPI
- [ ] Pagination
- [ ] Filtering and searching
- [ ] Rate limiting
- [ ] PostgreSQL database
- [ ] Production deployment
- [ ] Improved error responses
- [ ] Docker support
- [ ] CI/CD with GitHub Actions

---

# What I Learned

Through this project, I practiced:

- Building REST APIs with Django REST Framework
- Creating custom user models
- Working with serializers
- Implementing JWT authentication
- Creating custom DRF permissions
- Implementing ownership-based authorization
- Handling CRUD operations
- Working with environment variables
- Using Git and GitHub for version control

---

# Author

**Aneeshbabu G**

GitHub: [github.com/aneeshbabug](https://github.com/aneeshbabug)

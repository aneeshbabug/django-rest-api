Django REST API

A RESTful API built with Django and Django REST Framework for user registration and item management.
The project implements JWT authentication, CRUD operations, and custom authorization using admin and owner permissions.

Features:
User registration
JWT authentication
Access and refresh tokens
JWT token blacklisting for logout
Authenticated API access
Item creation and retrieval
Item update and deletion
Custom admin permission
Custom owner permission
Admin + owner authorization for modifying and deleting items
Password hashing using Django's authentication system
Environment variable support for sensitive configuration

Tech Stack:
Python
Django
Django REST Framework
Simple JWT
SQLite
python-dotenv

Authentication:
The API uses JWT (JSON Web Token) authentication.

Authentication Flow:
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
Receive new Access Token

Users can also log out by blacklisting their refresh token.


Authorization:
The project uses custom permissions to control access to item modification and deletion.

For PUT, PATCH, and DELETE, the user must satisfy all three conditions:

Authenticated
      +
Admin
      +
Owner of the Item
      ↓
Access Granted

Permission Examples
User	                ItemOwner	Admin	PUT/PATCH/DELETE
Unauthenticated	          -	      -	        ❌
Normal user	             Yes	    No	      ❌
Normal user	              No	    No	      ❌
Admin	                   Yes	   Yes	      ✅
Admin	                    No	   Yes	      ❌

This ensures that being an administrator alone is not enough to modify or delete another user's item.

API Endpoints:

Authentication -
Method	Endpoint	Description	Authentication
POST	/api/auth/register/	Register a new user	Not required
POST	/api/auth/token/	Obtain JWT access and refresh tokens	Not required
POST	/api/auth/token/refresh/	Refresh an access token	Not required
POST	/api/auth/logout/	Blacklist refresh token	Required

Items - 
Method	Endpoint	Description	Authentication
GET	/api/items/	Retrieve all items	Required
POST	/api/items/	Create an item	Required
GET	/api/items/<id>/	Retrieve a specific item	Required
PUT	/api/items/<id>/	Fully update an item	Admin + Owner
PATCH	/api/items/<id>/	Partially update an item	Admin + Owner
DELETE	/api/items/<id>/	Delete an item	Admin + Owner


Example Requests
Register a User
POST /api/auth/register/


Request:

{
    "username": "john",
    "password": "password123"
}


Successful response:

{
    "message": "User added Successfully"
}


New users are created as non-admin users.

Login
POST /api/auth/token/


Request:

{
    "username": "john",
    "password": "password123"
}


Response:

{
    "refresh": "your-refresh-token",
    "access": "your-access-token"
}


Use the access token when accessing protected endpoints:

Authorization: Bearer <access-token>

Create an Item
POST /api/items/
Authorization: Bearer <access-token>


Request:

{
    "name": "Laptop",
    "price": 75000,
    "description": "Development laptop"
}


The item's owner is automatically assigned to the authenticated user.

The client cannot choose or change the owner through the API.

Retrieve Items
GET /api/items/
Authorization: Bearer <access-token>


Example response:

[
    {
        "id": 1,
        "name": "Laptop",
        "price": 75000,
        "description": "Development laptop"
    }
]

Update an Item
PUT
PUT /api/items/1/
Authorization: Bearer <access-token>


Requires:
Authenticated + Admin + Owner


PUT replaces the complete item data.

PATCH
PATCH /api/items/1/
Authorization: Bearer <access-token>


Requires:
Authenticated + Admin + Owner


PATCH allows partial updates.

Delete an Item
DELETE /api/items/1/
Authorization: Bearer <access-token>


Requires:
Authenticated + Admin + Owner

Project Structure:
backend/
├── manage.py
│
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .gitignore
└── requirements.txt

Installation:
1. Clone the repository
git clone https://github.com/aneeshbabug/django-rest-api.git
cd django-rest-api

2. Create a virtual environment
python -m venv venv

3. Activate the virtual environment
Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Configure environment variables

Create a .env file in the same directory as manage.py.

Example:

SECRET_KEY=your-secret-key
DEBUG=True


Do not commit the .env file to GitHub.

6. Run migrations
python manage.py migrate

7. Start the development server
python manage.py runserver


The API will be available at:

http://127.0.0.1:8000/

Environment Variables:

The project uses environment variables for sensitive configuration.

Variable	      Description	        Example
SECRET_KEY	Django secret key  	your-secret-key
DEBUG	      Django debug mode	       True


Security:
The project follows several basic security practices:

Django password hashing is used when creating users.
The Django SECRET_KEY is stored outside the source code.
.env is excluded from Git.
SQLite database files are excluded from Git.
Users cannot assign themselves administrator privileges during registration.
Item ownership is assigned using the authenticated user.
Item ownership cannot be changed through the serializer.
JWT authentication protects API endpoints.
Modification and deletion require both administrator and ownership permissions.


Future Improvements:
Possible future improvements include:

Automated API tests
API documentation with Swagger/OpenAPI
Pagination
Filtering and searching
Rate limiting
PostgreSQL database
Production deployment
Improved error responses
Docker support
CI/CD with GitHub Actions
What I Learned

Through this project, I practiced:

Building REST APIs with Django REST Framework
Creating custom user models
Working with serializers
Implementing JWT authentication
Creating custom DRF permissions
Implementing ownership-based authorization
Handling CRUD operations
Working with environment variables
Using Git and GitHub for version control

Author
Aneeshbabu G

GitHub: https://github.com/aneeshbabug

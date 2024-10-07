
# E-commerce Product API

An API for managing products and categories in an e-commerce system. Built with Django and Django REST framework, this API allows for user authentication, product management, and category-based product search.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Features
- User management (CRUD operations)
- Product management (CRUD operations)
- Category management with dynamic search functionality
- Token-based authentication for user access control

## Technologies Used
- Python
- Django
- Django REST Framework
- SQLite (Database)
- Deployed on PythonAnywhere

## Installation
1. Clone the repository:
    \`\`\`bash
    git clone https://github.com/yourusername/ecommerce-product-api.git
    \`\`\`

2. Navigate to the project directory:
    \`\`\`bash
    cd ecommerce-product-api
    \`\`\`

3. Create and activate a virtual environment:
    \`\`\`bash
    python3 -m venv env
    source env/bin/activate
    \`\`\`

4. Install the required dependencies:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

5. Apply database migrations:
    \`\`\`bash
    python manage.py migrate
    \`\`\`

6. Run the development server:
    \`\`\`bash
    python manage.py runserver
    \`\`\`

## API Endpoints

### User Management
- \`POST /api/users/\`: Create a new user.
- \`GET /api/users/\`: Retrieve all users.
- \`PUT /api/users/<id>/\`: Update a specific user.
- \`DELETE /api/users/<id>/\`: Delete a user.

### Product Management
- \`POST /api/products/\`: Create a new product.
- \`GET /api/products/\`: Retrieve all products.
- \`PUT /api/products/<id>/\`: Update a specific product.
- \`DELETE /api/products/<id>/\`: Delete a product.

### Category Management
- \`GET /api/categories/\`: Retrieve all categories.
- \`GET /api/categories/<id>/\`: Retrieve products by category.

## Authentication
The API uses token-based authentication for secure access. Users need to authenticate to perform any product or category-related actions.

- Obtain a token:
    \`\`\`bash
    POST /api-token-auth/
    \`\`\`

- Include the token in the header for authorized requests:
    \`\`\`bash
    Authorization: Token <your_token>
    \`\`\`

## Future Enhancements
- Product reviews and ratings
- Stock management
- Discount and promotion features
- Support for multiple product images

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss potential changes or improvements.

# DIO Blog API

This project was developed as part of an academic course/study program.

This project is a RESTful API for a simple blog application, built with FastAPI, Python's modern, fast (high-performance) web framework for building APIs. It provides functionalities for user authentication, creating, reading, updating, and deleting blog posts.

## Features

-   User authentication (login, JWT token generation).
-   CRUD operations for blog posts (Create, Read, Update, Delete).
-   Filtering posts by published status.
-   Database integration using `databases` library (SQLAlchemy core).
-   Dependency management with Poetry.
-   Comprehensive integration tests with Pytest.

## Technologies Used

-   **FastAPI**: Web framework for building the API.
-   **Python**: Programming language.
-   **Poetry**: Dependency management and packaging.
-   **Uvicorn**: ASGI server for running the FastAPI application.
-   **`databases`**: Asynchronous database access library (SQLAlchemy Core compatible).
-   **Pytest**: Testing framework.
-   **Pydantic**: Data validation and settings management.
-   **Passlib**: For password hashing.
-   **PyJWT**: For JSON Web Token implementation.

## Setup Instructions

### Prerequisites

-   Python 3.9+
-   Poetry (installation instructions: `pip install poetry`)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/dio-blog.git
    cd dio-blog
    ```
    *(Note: Replace `https://github.com/your-username/dio-blog.git` with the actual repository URL if it's different.)*

2.  **Install dependencies using Poetry:**

    ```bash
    poetry install
    ```

3.  **Set up environment variables:**
    Copy the `.env.example` file to `.env` and fill in the necessary values.

    ```bash
    cp .env.example .env
    ```

    Example `.env` content:
    ```
    DATABASE_URL="sqlite:///./blog.db"
    SECRET_KEY="your-super-secret-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    -   `DATABASE_URL`: Connection string for your database. For local development, SQLite is often sufficient.
    -   `SECRET_KEY`: A strong, random string used for JWT encoding.
    -   `ALGORITHM`: The hashing algorithm for JWT (e.g., HS256).
    -   `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes.

## Running the Application

To start the FastAPI development server:

```bash
poetry run uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

The project includes integration tests using Pytest.

To run all tests:

```bash
poetry run pytest
```

To run a specific test file (e.g., after making a fix):

```bash
poetry run pytest tests/integration/controllers/post/test_read_all.py
```

## API Endpoints

### Authentication

-   `POST /auth/login`: Authenticate user and get JWT token.
    -   Request Body: `{"username": "your_username", "password": "your_password"}`
    -   Response: `{"access_token": "...", "token_type": "bearer"}`

### Posts

-   `POST /posts/`: Create a new blog post. (Requires authentication)
    -   Request Body: `{"title": "string", "content": "string", "published": "on" | "off"}`
-   `GET /posts/`: Retrieve a list of blog posts. (Requires authentication)
    -   Query Parameters:
        -   `limit`: (int) Maximum number of posts to return.
        -   `skip`: (int, default 0) Number of posts to skip.
        -   `published`: (str, optional) Filter by "on" or "off" status.
-   `GET /posts/{id}`: Retrieve a single blog post by ID. (Requires authentication)
-   `PATCH /posts/{id}`: Update an existing blog post by ID. (Requires authentication)
    -   Request Body: `{"title": "string", "content": "string", "published": "on" | "off"}` (fields are optional)
-   `DELETE /posts/{id}`: Delete a blog post by ID. (Requires authentication)

## Project Structure

```
.
├── .env.example
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── src/
│   ├── config.py             # Application settings and environment variables
│   ├── database.py           # Database connection and metadata
│   ├── exceptions.py         # Custom exceptions
│   ├── main.py               # Main FastAPI application entry point
│   ├── security.py           # Authentication and authorization logic (JWT)
│   ├── controllers/          # API endpoint definitions (FastAPI routers)
│   │   ├── auth.py
│   │   └── post.py
│   ├── models/               # Database table definitions (SQLAlchemy Core)
│   │   └── post.py
│   ├── schemas/              # Pydantic models for request/response validation
│   │   ├── auth.py
│   │   └── post.py
│   ├── services/             # Business logic and database interactions
│   │   └── post.py
│   └── views/                # Pydantic models for API responses (output schemas)
│       └── post.py
└── tests/
    ├── integration/          # Integration tests for API endpoints
    │   ├── controllers/
    │   │   ├── auth/
    │   │   └── post/
    └── conftest.py           # Pytest fixtures and configurations
```

This `README.md` provides a comprehensive overview of the `dio-blog` project.

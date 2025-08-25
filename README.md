# Task Management API

A FastAPI-based task management system with PostgreSQL, Docker, and pytest test suite.

This project allows you to manage tasks with CRUD operations. It can run locally or via Docker.

---

## 🚀 Features
- Create, Read, Update, Delete tasks
- PostgreSQL database
- Async SQLAlchemy integration
- Dockerized environment for easy setup
- Pytest test suite
- Swagger UI and ReDoc API documentation


---

## ⚙️ Setup Instructions

### 🔹 Run Locally
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload

# Run with Docker
docker-compose up --build

# Stop Containers
docker-compose down

# Running Tests
pytest

# Inside Docker
docker-compose run --rm web pytest

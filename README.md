# Digital Library Management System

## Table of Contents

- [Code Reference](#code-reference)  
- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Architecture & Design Patterns](#architecture--design-patterns)  
- [Project Structure](#project-structure)  
- [Database Setup](#database-setup)  
- [Installation & Usage](#installation--usage)  
- [API Endpoints](#api-endpoints)  
- [Testing](#testing)  
- [Workflow](#workflow)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Code Reference

- Repository: `https://github.com/username/library-management`  
- SQL scripts:  
  - `db/01_create_tables.sql`  
  - `db/02_create_indexes.sql`  

---

## Overview

Modern RESTful API in Python to manage digital library.  
Supports user, author, book, and loan management with business rules.

---

## Features

- User management: list, create, retrieve, update, delete  
- Author catalog: full CRUD  
- Book catalog: list, create, retrieve, update, delete; availability checks  
- Loan lifecycle: borrow, return (fine calculation), list active/overdue, user history  
- Business rules:  
  - 14‑day loan period  
  - $2.00/day fine  
  - Max 3 active loans per user  
- Extras: pagination, Redis cache, rate limiting, structured logging, JWT auth, Swagger UI  

---

## Tech Stack

| Layer           | Technology / Library         |
|----------------:|------------------------------|
| Language         | Python 3.11+                 |
| Framework        | FastAPI                      |
| Validation       | Pydantic                     |
| ORM              | SQLAlchemy                   |
| Database         | MySQL (InnoDB, utf8mb4)      |
| Cache            | Redis                        |
| API Docs         | FastAPI OpenAPI / Swagger UI |
| Testing          | Pytest                       |
| Logging          | structlog                    |
| Containerization | Docker + Docker Compose      |
| CI/CD            | GitHub Actions               |

---

## Architecture & Design Patterns

- Layered architecture: API, Service, Repository  
- Patterns: Repository, Dependency Injection, Factory  
- Principles: SOLID, DRY, YAGNI  

---

## Project Structure

Below is the folder/file layout. Inner code fences use tildes to avoid conflicts:

~~~text
library-management/
├── db/
│   ├── 01_create_tables.sql
│   └── 02_create_indexes.sql
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── auth.py
│   │   │   └── authors.py
│   │   │   └── books.py
│   │   │   └── loans.py
│   │   │   └── router.py
│   │   │   └── users.py
│   ├── core/
│   │   ├── .env
│   │   ├── logging.py
│   │   ├── security.py
│   │   ├── settings.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   ├── session.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── models/
│   │   ├── author_model.py
│   │   ├── book_model.py
│   │   └── loan_model.py
│   │   ├── user_model.py
│   ├── schemas/
│   │   ├── author_schema.py
│   │   ├── book_schema.py
│   │   └── loan_schema.py
│   │   ├── user_schema.py
│   ├── services/
│   │   ├── author_service.py
│   │   ├── book_service.py
│   │   └── loan_service.py
│   │   ├── user_service.py
│   ├── utils/
│   │   └── export.py
├── tests/
│   ├── test_user.py
│   ├── test_book.py
│   └── test_loan.py
├── main.py
├── requirements.txt
└── README.md
~~~

---

## Database Setup

~~~sql
CREATE DATABASE IF NOT EXISTS library_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- then run:
-- mysql -u root -p library_db < db/01_create_tables.sql
-- mysql -u root -p library_db < db/02_create_indexes.sql
~~~

---

## Installation & Usage

~~~bash
git clone https://github.com/username/library-management.git
cd library-management
cp .env.example .env
# edit .env with credentials
pip install -r requirements.txt
docker-compose up -d
uvicorn app.main:app --reload
~~~

Access Swagger UI at `http://localhost:8000/docs`

---

## API Endpoints

- **Users**: `/users` (GET, POST), `/users/{id}` (GET, PUT, DELETE)  
- **Authors**: `/authors` (CRUD)  
- **Books**: `/books` (GET, POST), `/books/{id}` (GET, PATCH, DELETE)  
- **Loans**: `/loans` (POST), `/loans/{id}/return` (POST), `/loans` (GET), `/users/{user_id}/loans` (GET)  

---

## Testing

~~~bash
pytest --cov=app
~~~

---

## Workflow

1. Fork repository  
2. Create feature branch  
3. Commit changes  
4. Push branch  
5. Open Pull Request  

---

## Contributing

- Follow PEP8, use Black & isort  
- Document new endpoints in Swagger  
- Write tests for new features  

---

## License

Licensed under MIT License  

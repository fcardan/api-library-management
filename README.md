# Digital Library Management System

[![🔥 Follow my GitHub](https://img.shields.io/badge/👉🏼-GitHub-white)](https://www.github.com/fcardan)
[![🔥 Follow my Linkedin](https://img.shields.io/badge/👉🏼-Linkedin-blue)](https://www.linkedin.com/in/fcardan)
[![⭐ pt-br](https://img.shields.io/badge/👉🏼-PtBr-green)](https://github.com/fcardan/api-library-management/blob/main/README-ptbr.md)
[![⭐ Star](https://img.shields.io/github/stars/fcardan/api-library-management)](https://github.com/fcardan/api-library-management)


## 🔹Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Database Setup](#database-setup)  
- [Installation & Usage](#installation--usage)  
- [API Endpoints](#api-endpoints)  

---

## Overview

api-library-management is a Python RESTful API built to manage a library system’s operations—from books to borrowing—designed with clean architecture, secure access, and scalability in mind.

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
- Extras: pagination, rate limiting, structured logging, JWT auth, Swagger UI  

---

## Tech Stack

| Layer           | Technology / Library         |
|----------------:|------------------------------|
| Language         | Python 3.11+                 |
| Framework        | FastAPI                      |
| Validation       | Pydantic                     |
| ORM              | SQLAlchemy                   |
| Database         | MySQL                        |
| API Docs         | FastAPI OpenAPI / Swagger UI |
| Testing          | Pytest                       |
| Logging          | structlog                    |

---

## Project Structure

Below is the folder/file layout:

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
└── README-ptbr.md
└── LICENSE.md
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
git clone https://github.com/fcardan/api-library-management.git
cd api-library-management
# edit .env with credentials
pip install -r requirements.txt
uvicorn main:app --reload
~~~

Access Swagger UI at `http://localhost:8000/docs`

---

## API Endpoints (INSOMNIA)

#### Authentication
- **Login**: `🟢 POST /auth/token`  
  Authenticate using username/password to obtain bearer token

#### Users
- **Create User**: `🟢 POST /users`  
- **List Users**: `🟣 GET /users`  
- **Get User by ID**: `🟣 GET /users/{user_id}`  
- **List User Loans**: `🟣 GET /users/{user_id}/loans`  
- **Full Update User**: `🟠 PUT /users/{user_id}`  
- **Partial Update User**: `🟡 PATCH /users/{user_id}`  
- **Delete User**: `🔴 DELETE /users/{user_id}`  

#### Authors
- **Create Author**: `🟢 POST /authors`  
- **List Authors**: `🟣 GET /authors`  
- **Get Author by ID**: `🟣 GET /authors/{author_id}`  
- **List Author's Books**: `🟣 GET /authors/{author_id}/books`  
- **Full Update Author**: `🟠 PUT /authors/{author_id}`  
- **Partial Update Author**: `🟡 PATCH /authors/{author_id}`  
- **Delete Author**: `🔴 DELETE /authors/{author_id}`  

#### Books
- **Create Book**: `🟢 POST /books`  
- **List Books**: `🟣 GET /books`  
- **Get Book by ID**: `🟣 GET /books/{book_id}`  
- **List Books by Availability**: `🟣 GET /books/available?status={boolean}`  
- **Full Update Book**: `🟠 PUT /books/{book_id}`  
- **Partial Update Book**: `🟡 PATCH /books/{book_id}`  
- **Delete Book**: `🔴 DELETE /books/{book_id}`  


#### Loans
- **Create Loan**: `🟢 POST /loans`  
- **List All Loans**: `🟣 GET /loans`  
- **Get Loan by ID**: `🟣 GET /loans/{loan_id}`  
- **List Active Loans**: `🟣 GET /loans/active/{user_id}`  
- **List Overdue Loans**: `🟣 GET /loans/overdue/{user_id}`  
- **List Loan History**: `🟣 GET /loans/history/{user_id}`  
- **Full Update Loan**: `🟠 PUT /loans/{loan_id}`  
- **Partial Update Loan**: `🟡 PATCH /loans/{loan_id}`  
- **Delete Loan**: `🔴 DELETE /loans/{loan_id}`  

---

### Request Examples

#### Authentication Request
```http
POST /auth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=youremailuserhere&password=yourpasswordhere
```

#### Book Creation
```http
{
  "title": "Sample Book",
  "author_id": "003055e6-372f-475d-a6ce-46e7d0def925",
  "published_date": "2023-01-15",
  "total_copies": 5,
  "available_copies": 5
}
```

#### Loan Creation
```http
{
  "user_id": "040446ef-7338-4351-955b-c94406332c9b",
  "book_id": "322b0e8b-cb0e-460d-bb5e-0987a3ba6eb3",
  "loan_date": "2025-07-15"
}
```

#### Partial Loan Update
```http
{
  "return_date": "2025-07-30"
}
```

### Environment Variables
```http
base_url: http://127.0.0.1:8000/api/v1
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
user_id: 040446ef-7338-4351-955b-c94406332c9b
book_id: 71c10dad-9ea7-45a1-92a9-1dffeeb9e614
author_id: 003055e6-372f-475d-a6ce-46e7d0def925
loan_id: 841b0c6f-2e6e-4ce3-97a9-336402f2d6c4

```

### Technical Specifications

#### 1. Authentication
- **Type**: Bearer Token (JWT)
- **Requirement**: Required for all endpoints except `/auth/token`
- **Header Format**:  
  `Authorization: Bearer <your_token>`

#### 2. Request Formats
| Endpoint Type       | Content-Type                     | Body Format        |
|---------------------|----------------------------------|-------------------|
| Most endpoints      | `application/json`               | JSON              |
| Authentication      | `application/x-www-form-urlencoded` | Form URL encoded |

#### 3. HTTP Methods
| Method  | Typical Usage                     | Example Endpoints              |
|---------|-----------------------------------|--------------------------------|
| 🟢 POST    | Create new resources              | `/users`, `/books`, `/loans`   |
| 🟣 GET     | Retrieve resources                | `/users/{id}`, `/books/available` |
| 🟠 PUT     | Full resource update              | `/users/{id}`, `/loans/{id}`   |
| 🟡 PATCH   | Partial resource update           | `/books/{id}`, `/authors/{id}` |
| 🔴 DELETE  | Remove resources                  | `/authors/{id}`, `/loans/{id}` |

#### 4. Query Parameters
| Parameter | Endpoint                  | Values       | Description                     |
|-----------|---------------------------|--------------|---------------------------------|
| `status`  | `GET /books/available`    | `true/false` | Filter books by availability    |

#### 5. Path Parameters
| Parameter   | Resource Type | Example Endpoint                     |
|-------------|---------------|--------------------------------------|
| `{user_id}` | User          | `GET /users/{user_id}/loans`         |
| `{book_id}` | Book          | `PATCH /books/{book_id}`             |
| `{author_id}`| Author        | `GET /authors/{author_id}/books`     |
| `{loan_id}` | Loan          | `PUT /loans/{loan_id}`               |

#### 6. Response Formats
- **Success**: JSON payload with resource data
- **Errors**: Standard HTTP status codes (4xx/5xx) with JSON error details
- **Validation Errors**: `422 Unprocessable Entity` with field-specific messages

#### 7. Base URL Structure

`{{base_url}}/api/v1/<endpoint_path>`

### Insomnia Collection Import Guide (v11.2.0):

#### Step 1: Download Raw Collection File
```bash
1. Open the GitHub link:  
   [Insomnia Collection](https://github.com/fcardan/api-library-management/blob/main/Insomnia_library-api.yaml)
2. Click the **Raw** button (top-right corner)
3. Press `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac) to save
4. Ensure filename is `Insomnia_library-api.yaml` (not .txt)
```

#### Step 2: Import into Insomnia
```bash
1. Launch Insomnia v11.2.0+
2. In your active workspace:   
   • Select Import/Export → Import Data   
```

#### Step 3: Configure Import Settings
```bash
In the import window:
1. Select "File" tab
2. Click "Select File" → choose downloaded .yaml
3. Click "Scan"
```

---

## Thanks for checking it out ❤️
### Did you like the project?

- ➡️ **Follow**: [@fcardan](https://github.com/fcardan)

- *️⃣ **Star**: Give it a star to support future updates!  

- 🔀 **Fork**: Fork it to customize for your needs!

---

## License
This repository is licensed. This means you are free to share and adapt this content for any purpose, even commercially, as long as you provide appropriate credit to the original author. For more details, please refer to the [LICENSE.md](https://github.com/fcardan/api-library-management/blob/main/LICENSE.md) file.

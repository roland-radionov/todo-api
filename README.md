# todo-api

Simple todo api that enable to create user, login, and create, update, delete tasks.

## Stack

- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **SQLite**
- **JWT**
- **Poetry**
- **Alembic**

## Getting started
  
### 1. Clone repository

``` shell
git clone https://github.com/roland-radionov/todo-api.git
cd todo-api
```

### 2. Create virtual env

``` shell
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

``` shell
pip install .
```

or with **Poetry**

``` shell
poetry install
```

### 4. Configure .env

Create ```.env``` file:
``` shell
DB_URL="sqlite+aiosqlite:///todo.db"
DEBUG=False
PUBLIC_KEY_PATH="etc/certs/public_key.pem"
PRIVATE_KEY_PATH="etc/certs/private_key.pem"
ALGORITHM="RS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### 5. Migration

``` bash
alembic upgrade head
```

### 6. Launch

``` bash
python main.py
or 
uvicorn main:app --reload
```

Documentation is available on address: ```http://127.0.0.1:8000/docs```

## API Endpoints

### Authentication

| Method |       Endpoint        |          Description         |
| :----: | :-------------------: | :--------------------------: |
| POST   | /api/v1/auth/register | User registration            |
| POST   |  /api/v1/auth/login   | Login, obtaining a JWT token |

### Tasks

| Method |        Endpoint         |                        Description                        |
| :----: | :---------------------: | :-------------------------------------------------------: |
| GET    | /api/v1/tasks/          | Receive all tasks with pagination, filtration and sorting |
| POST   | /api/v1/tasks/          | Create task                                               |
| PUT    | /api/v1/tasks/{task_id} | Update task by id                                         |
| DELETE | /api/v1/tasks/{task_id} | Delete tasks by id                                        |

### Filtration parameters

|  Parameter | Type |                        Description                       |
| :--------: | :--: | :------------------------------------------------------: |
| page       | int  | Page number (default: 1, min: 1)                         |
| limit      | int  | Number of tasks per page (default: 10, min: 1, max: 100) |
| sort_by    | str  | Sorting field ("created_at", "updated_at")               |
| sort_order | str  | Sorting order ("asc", "desc")                            |
| search     | str  | Search by title                                          |

## Requests example

### Registration

``` bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "qwerty"}'
```

### Login

``` bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=qwerty"
```

### Receiving tasks

``` bash
curl -X GET http://127.0.0.1:8000/api/v1/tasks?page=1&limit=10 \
  -H "Authorization: Bearer <your-token>"
```

### Create task

``` bash
curl -X POST http://127.0.0.1:8000/api/v1/tasks \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Read docs"}'
```

## Error Responses

| Status | Description                                      |
| ------ | ------------------------------------------------ |
| 401    | Unauthorized (invalid or missing token)          |
| 403    | Forbidden (trying to modify someone else's task) |
| 404    | Resource not found                               |
| 422    | Validation error                                 |

## Project structure

``` text
project/
├── api/
│   └── v1/
│       ├── auth/          # JWT authentication
│       │   ├── __init__.py
│       │   ├── schemas.py
│       │   ├── views.py
│       │   └── utils_jwt.py
│       ├── tasks/         # Task CRUD
│       │   ├── __init__.py
│       │   ├── crud.py
│       │   ├── schemas.py
│       │   └── views.py
│       ├── users/         # User management
│       │   ├── __init__.py
│       │   ├── crud.py
│       │   ├── schemas.py
│       │   └── views.py
│       └── __init__.py
├── core/
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   └── user.py
│   ├── __init__.py
│   ├── config.py          # Application settings
│   └── database.py        # Database connection
├── alembic/               # Database migrations
│   └── versions/
├── .env                   # Environment variables
├── .gitignore
├── alembic.ini
├── LICENSE
├── main.py                # Application entry point
├── pyproject.toml         # Project config (Poetry)
└── README.md
```

## Credits

This project is based on the [Todo List API](https://roadmap.sh/projects/todo-list-api) project from [roadmap.sh](https://roadmap.sh).

## Author

[Roland Radionov](https://github.com/roland-radionov)

## License

MIT
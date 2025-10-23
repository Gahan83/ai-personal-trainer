# AI Personal Trainer - Backend

FastAPI-based backend for the AI Personal Trainer application.

## Features

- **RESTful API** with automatic OpenAPI documentation
- **Authentication & Authorization** with JWT tokens
- **Database Integration** with SQLAlchemy ORM
- **Background Tasks** with Celery
- **Caching** with Redis
- **Data Validation** with Pydantic models

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile

### Workouts
- `GET /api/v1/workouts` - List workouts
- `POST /api/v1/workouts` - Create workout
- `GET /api/v1/workouts/{id}` - Get specific workout

### Exercises
- `GET /api/v1/exercises` - List exercises
- `GET /api/v1/exercises/categories` - List exercise categories

## Development

### Running the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

### Running Tests

```bash
pytest
```

## Environment Variables

Copy `env.example` to `.env` and configure:

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `REDIS_URL` - Redis connection string
- `ALLOWED_HOSTS` - CORS allowed origins

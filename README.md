# AI Personal Trainer

An intelligent fitness application that provides personalized workout plans and guidance using AI technology.

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **Redis** - In-memory data structure store
- **Celery** - Distributed task queue

### Frontend
- **React 18** - JavaScript library for building user interfaces
- **React Router** - Declarative routing for React
- **Styled Components** - CSS-in-JS styling solution
- **React Query** - Data fetching and caching library
- **React Hook Form** - Performant, flexible forms
- **Axios** - HTTP client for API requests
- **Lucide React** - Beautiful & consistent icon toolkit

## Project Structure

```
ai-personal-trainer/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   │   └── endpoints/  # Individual endpoint modules
│   │   ├── core/           # Core functionality (config, security)
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic services
│   │   └── utils/         # Utility functions
│   ├── tests/              # Test files
│   ├── docs/               # Documentation
│   ├── requirements.txt    # Python dependencies
│   └── env.example         # Environment variables template
├── frontend/               # React frontend
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── styles/         # Styling and themes
│   │   └── utils/          # Utility functions
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## Features

- **User Authentication** - Secure login and registration
- **Personalized Workouts** - AI-generated workout plans
- **Progress Tracking** - Monitor fitness journey
- **Exercise Library** - Comprehensive database of exercises
- **Dashboard** - Overview of fitness metrics
- **Profile Management** - User profile and preferences

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Redis (optional, for background tasks)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment variables:
   ```bash
   cp env.example .env
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Backend Development

- Use `pytest` for running tests
- Use `alembic` for database migrations
- Follow PEP 8 style guidelines
- Use type hints for better code documentation

### Frontend Development

- Use functional components with hooks
- Follow React best practices
- Use styled-components for styling
- Implement responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

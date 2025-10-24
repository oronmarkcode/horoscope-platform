# Horoscope Platform

This is a monorepo containing both the backend and frontend applications for the Horoscope project.

## Project Structure

```
horoscope-platform/
├── backend/                 # FastAPI backend application
│   ├── horoscope_backend/   # Main application package
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   ├── pyproject.toml      # Python dependencies
│   └── Dockerfile          # Backend Docker configuration
├── frontend/               # Frontend application (placeholder)
│   ├── package.json        # Node.js dependencies
│   └── README.md          # Frontend documentation
├── docker-compose.yml      # Unified Docker setup
└── README.md              # This file
```

## Quick Start

### Using Docker Compose (Recommended)

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Access the applications:**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000 (when implemented)
   - Database: localhost:5432

3. **Stop all services:**
   ```bash
   docker-compose down
   ```

### Development Setup

#### Backend Development

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   ```bash
   cp ../env.example .env
   ```

4. **Run database migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

5. **Start the development server:**
   ```bash
   poetry run uvicorn horoscope_backend.main:app --reload
   ```

#### Frontend Development

The frontend is currently a placeholder. To implement it:

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Choose your framework and initialize:**
   ```bash
   # For React
   npx create-react-app . --template typescript

   # For Vue
   npm create vue@latest .

   # For Angular
   ng new horoscope-platform-frontend
   ```

## Services

- **Backend**: FastAPI application running on port 8000
- **Frontend**: Node.js application running on port 3000 (placeholder)
- **Database**: PostgreSQL running on port 5432

## Environment Variables

Copy `env.example` to `.env` in the backend directory and configure:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Enable debug mode

## Database Migrations

Run migrations from the backend directory:

```bash
cd backend
poetry run alembic upgrade head
```

## Testing

Run tests from the backend directory:

```bash
cd backend
poetry run pytest
```

## Contributing

1. Make changes in the appropriate directory (`backend/` or `frontend/`)
2. Test your changes
3. Submit a pull request

## License

MIT License
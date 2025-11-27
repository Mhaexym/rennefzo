# Rennefzo Backend API

A FastAPI backend for the Rennefzo Flutter application.

## Features

- FastAPI framework with async/await support
- CORS middleware configured for Flutter app
- Structured project layout following best practices
- Pydantic models for request/response validation
- Error handling with custom exceptions
- Health check endpoints
- Example CRUD endpoints for items

## Project Structure

```
rennefzo_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/      # API route handlers
│   │       ├── schemas/         # Pydantic models
│   │       └── api.py          # Router aggregation
│   └── core/
│       ├── config.py           # Settings and configuration
│       └── exceptions.py       # Custom exceptions
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the development server**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /api/v1/health/` - Health check
- `GET /api/v1/health/ping` - Simple ping

### Items (Example CRUD)
- `GET /api/v1/items/` - List all items (with pagination)
- `GET /api/v1/items/{item_id}` - Get item by ID
- `POST /api/v1/items/` - Create new item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Configuration

The application uses environment variables for configuration. See `.env.example` for available options.

Key settings:
- `BACKEND_CORS_ORIGINS`: List of allowed origins for CORS
- `SECRET_KEY`: Secret key for JWT tokens (change in production)
- `DATABASE_URL`: Database connection string

## Development

### Adding New Endpoints

1. Create a new router in `app/api/v1/endpoints/`
2. Define schemas in `app/api/v1/schemas/`
3. Add the router to `app/api/v1/api.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Use async/await for I/O operations

## Production Deployment

Before deploying:
1. Change `SECRET_KEY` to a secure random value
2. Update `BACKEND_CORS_ORIGINS` with your Flutter app URLs
3. Set up a proper database (replace in-memory storage)
4. Configure proper logging
5. Set up HTTPS
6. Use a production ASGI server (e.g., Gunicorn with Uvicorn workers)

## License

MIT


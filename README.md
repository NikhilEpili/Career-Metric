# Career Metric - AI-Based Candidate Assessment System

An AI-powered employability scoring platform that evaluates student employability with 85% accuracy using weighted scoring algorithms across academic, technical, and soft skills.

## Features

- ✅ **Weighted Scoring Algorithm**: Evaluates candidates across multiple dimensions
- ✅ **Personalized Feedback**: 100% personalized feedback and career suggestions
- ✅ **Profile Integration**: Resume parsing, LinkedIn & GitHub profile analysis, CP ratings
- ✅ **Real-time Dashboard**: Interactive score visualization with Chart.js
- ✅ **Authentication**: JWT-based secure authentication
- ✅ **RESTful API**: FastAPI backend with OpenAPI documentation

## Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL, SQLAlchemy, Pandas, Scikit-learn, BeautifulSoup
- **Frontend**: React, TypeScript, Vite, Chart.js
- **Infrastructure**: Docker, Docker Compose
- **Authentication**: JWT (python-jose)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Career-Metric
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

   Or start in background:
   ```bash
   docker-compose up -d --build
   ```

3. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/docs
   - **Database**: localhost:5432
     - User: `career_metric`
     - Password: `career_metric`
     - Database: `career_metric`

### First Time Setup

1. **Start services:**
   ```bash
   docker-compose up --build
   ```

2. **Wait for services to be ready:**
   - Backend will run migrations automatically
   - Superuser will be created automatically
   - Default superuser: `admin@example.com` / `ChangeMe123!`

3. **Verify health:**
   ```bash
   curl http://localhost:8000/api/v1/health/
   ```

4. **Open frontend:**
   - Navigate to http://localhost:3000
   - You should see the Career Metric interface
   - Health indicator should show "Live" status

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

## Local Development

### Backend Setup
```bash
cd backend
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head
python -c "from app.core.init_db import main; main()"
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests
```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_scoring.py -v

# Run with verbose output
pytest -v
```

### Frontend Tests
```bash
# Run all tests
cd frontend
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Type check
npx tsc --noEmit

# Lint
npm run lint
```

### Full Stack Testing
```bash
# Start services
docker-compose up --build

# Test API
curl http://localhost:8000/api/v1/health/

# Test Frontend
# Open http://localhost:3000
```

### Test Checklist

**Backend API Tests:**
- [ ] Health endpoint: `curl http://localhost:8000/api/v1/health/`
- [ ] Register user: `POST /api/v1/auth/register`
- [ ] Login: `POST /api/v1/auth/login`
- [ ] Create profile: `POST /api/v1/profiles/`
- [ ] Evaluate assessment: `POST /api/v1/assessments/{id}/evaluate`

**Frontend Manual Tests:**
- [ ] Health indicator shows status
- [ ] Registration form works
- [ ] Login works
- [ ] Intake form accepts inputs
- [ ] Score dashboard displays
- [ ] Charts render correctly

## Testing the Application

### 1. Register a New User
- Click "Create an account" on the frontend
- Or use the API:
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@example.com",
      "password": "Test123!",
      "full_name": "Test User"
    }'
  ```

### 2. Login
- Use the login form on the frontend
- Or use the API:
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@example.com&password=Test123!"
  ```

### 3. Create a Profile
- After logging in, a profile will be created automatically
- Or create one via API with your token

### 4. Evaluate Assessment
- Fill out the intake form on the frontend
- Submit to get your employability score
- View personalized feedback and recommendations

## Project Structure

```
Career-Metric/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test suite
│   └── requirements.txt  # Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities & API client
│   │   └── styles/       # CSS
│   └── package.json
├── docker-compose.yml    # Docker orchestration
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user

### Profiles
- `GET /api/v1/profiles/` - List user profiles
- `POST /api/v1/profiles/` - Create profile
- `PUT /api/v1/profiles/{id}` - Update profile
- `DELETE /api/v1/profiles/{id}` - Delete profile

### Assessments
- `POST /api/v1/assessments/{profile_id}/evaluate` - Evaluate candidate

### Health
- `GET /api/v1/health/` - Health check

See full API documentation at http://localhost:8000/api/docs

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
POSTGRES_SERVER=db
POSTGRES_USER=career_metric
POSTGRES_PASSWORD=career_metric
POSTGRES_DB=career_metric
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=ChangeMe123!
```

### Frontend
Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Scoring Algorithm

The employability score is calculated using weighted components:

- **Academic** (25%): Academic performance and qualifications
- **Technical** (35%): Technical skills and programming ability
- **Soft Skills** (20%): Communication and teamwork
- **Experience** (10%): Industry experience
- **Portfolio** (10%): GitHub, LinkedIn, Resume, CP ratings

## Troubleshooting

### Services Won't Start
```bash
# Check if ports are already in use (Windows)
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Database Connection Issues
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Backend Errors
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up frontend
```

### Backend Tests Fail
- Check Python version: `python --version` (need 3.11+)
- Install deps: `pip install -r requirements-dev.txt`
- Check database connection

### Frontend Tests Fail
- Clear cache: `rm -rf node_modules && npm install`
- Check Node version: `node --version` (need 18+)

### Docker Issues
- Rebuild: `docker-compose build --no-cache`
- Check logs: `docker-compose logs backend`

## Production Build

To build for production:

```bash
# Build all services
docker-compose build

# Or build specific service
docker-compose build backend
docker-compose build frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions, please open an issue on GitHub.

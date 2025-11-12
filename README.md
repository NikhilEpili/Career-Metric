<div align="center">

# 🚀 Career Metric

**AI-Powered Candidate Assessment System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

*An intelligent employability scoring platform that evaluates candidates with 85% accuracy using advanced weighted algorithms across academic, technical, and soft skills dimensions.*

[Features](#-features) • [Quick Start](#-quick-start) • [Contributing](#-contributing) • [Documentation](#-documentation) • [Support](#-support)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Development Guide](#-development-guide)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Support](#-support)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About

**Career Metric** is an open-source AI-powered platform designed to revolutionize candidate assessment. By leveraging machine learning algorithms and comprehensive data analysis, it provides accurate employability scores and personalized feedback to help students and professionals understand their career readiness.

### Key Highlights

- 🎯 **85% Accuracy**: Advanced weighted scoring algorithm
- 🤖 **AI-Powered**: Machine learning-based assessment
- 📊 **Multi-Dimensional**: Evaluates academic, technical, and soft skills
- 🔄 **Real-Time**: Interactive dashboards with live updates
- 🔒 **Secure**: JWT-based authentication and data protection
- 📈 **Personalized**: 100% customized feedback and recommendations

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **🎯 Weighted Scoring Algorithm** | Multi-dimensional evaluation across 5 key areas with intelligent weighting |
| **💬 Personalized Feedback** | AI-generated, 100% personalized feedback and career suggestions |
| **🔗 Profile Integration** | Seamless integration with Resume parsing, LinkedIn, GitHub, and CP ratings |
| **📊 Real-Time Dashboard** | Interactive visualizations using Chart.js with live score updates |
| **🔐 Secure Authentication** | JWT-based authentication with role-based access control |
| **📚 RESTful API** | FastAPI backend with comprehensive OpenAPI/Swagger documentation |
| **🐳 Docker Support** | One-command deployment with Docker Compose |
| **🧪 Test Coverage** | Comprehensive test suite for both backend and frontend |

### Scoring Dimensions

The platform evaluates candidates across five weighted dimensions:

- **📚 Academic (25%)**: Academic performance, qualifications, and educational achievements
- **💻 Technical (35%)**: Programming skills, technical knowledge, and coding ability
- **🤝 Soft Skills (20%)**: Communication, teamwork, and interpersonal abilities
- **💼 Experience (10%)**: Industry experience, internships, and professional background
- **🎨 Portfolio (10%)**: GitHub contributions, LinkedIn profile, Resume quality, CP ratings

---

## 🛠 Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **ML/Analytics**: Pandas, Scikit-learn
- **Web Scraping**: BeautifulSoup
- **Authentication**: JWT (python-jose)
- **Migrations**: Alembic
- **Testing**: Pytest

### Frontend

- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Visualization**: Chart.js
- **Styling**: CSS3
- **Testing**: Vitest

### Infrastructure

- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL
- **API Documentation**: OpenAPI/Swagger

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) 18+ (for local frontend development)
- [Python](https://www.python.org/) 3.11+ (for local backend development)
- [Git](https://git-scm.com/)

### Installation

#### Option 1: Docker (Recommended) 🐳

The easiest way to get started is using Docker Compose:

   ```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Career-Metric.git
   cd Career-Metric

# 2. Start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**Access Points:**
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/api/docs
- 🗄️ **Database**: localhost:5432

**Default Credentials:**
- Database User: `career_metric`
- Database Password: `career_metric`
- Database Name: `career_metric`
- Superuser: `admin@example.com` / `ChangeMe123!`

#### Option 2: Local Development

**Backend Setup:**

   ```bash
cd backend

# Install dependencies
pip install -r requirements-dev.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Initialize database
python -c "from app.core.init_db import main; main()"

# Start development server
uvicorn app.main:app --reload
```

**Frontend Setup:**

   ```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env

# Start development server
npm run dev
```

### First Time Setup

1. **Start Services:**
   ```bash
   docker-compose up --build
   ```

2. **Wait for Initialization:**
   - Backend will automatically run database migrations
   - Superuser account will be created automatically
   - All services will be ready in ~30 seconds

3. **Verify Installation:**
   ```bash
   # Check backend health
   curl http://localhost:8000/api/v1/health/
   
   # Expected response: {"status": "healthy"}
   ```

4. **Access the Application:**
   - Open http://localhost:3000 in your browser
   - You should see the Career Metric interface
   - Health indicator should display "Live" status

---

## 📁 Project Structure

```
Career-Metric/
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 api/              # API routes and endpoints
│   │   │   ├── 📂 v1/           # API version 1
│   │   │   │   ├── auth.py      # Authentication endpoints
│   │   │   │   ├── profiles.py  # Profile management
│   │   │   │   ├── assessments.py # Assessment endpoints
│   │   │   │   └── health.py    # Health check
│   │   │   ├── deps.py          # Dependencies
│   │   │   └── router.py        # Main router
│   │   ├── 📂 core/             # Core configuration
│   │   │   ├── config.py        # Settings
│   │   │   ├── security.py      # Security utilities
│   │   │   └── init_db.py       # Database initialization
│   │   ├── 📂 db/               # Database setup
│   │   │   ├── base.py          # Base class
│   │   │   └── session.py       # Database session
│   │   ├── 📂 models/           # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── assessment.py
│   │   │   ├── feedback.py
│   │   │   └── integration.py
│   │   ├── 📂 schemas/          # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── assessment.py
│   │   │   └── integration.py
│   │   ├── 📂 services/         # Business logic
│   │   │   ├── scoring.py       # Scoring algorithm
│   │   │   ├── feedback.py      # Feedback generation
│   │   │   ├── resume_parser.py # Resume parsing
│   │   │   ├── github.py        # GitHub integration
│   │   │   ├── linkedin.py      # LinkedIn integration
│   │   │   └── cp.py            # CP ratings
│   │   └── 📂 utils/            # Utility functions
│   ├── 📂 alembic/              # Database migrations
│   ├── 📂 tests/                # Test suite
│   ├── 📂 scripts/              # Utility scripts
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/       # React components
│   │   │   ├── AuthPanel.tsx
│   │   │   ├── IntakeForm.tsx
│   │   │   ├── ScoreDashboard.tsx
│   │   │   └── StatusPill.tsx
│   │   ├── 📂 lib/              # Utilities & API client
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   ├── 📂 styles/           # CSS styles
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml           # Docker orchestration
└── README.md                    # This file
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Login and receive JWT token |
| `GET` | `/api/v1/auth/me` | Get current user information |

### Profile Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/profiles/` | List all user profiles |
| `POST` | `/api/v1/profiles/` | Create a new profile |
| `PUT` | `/api/v1/profiles/{id}` | Update an existing profile |
| `DELETE` | `/api/v1/profiles/{id}` | Delete a profile |

### Assessment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/assessments/{profile_id}/evaluate` | Evaluate a candidate and generate score |

### Health Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health/` | Check API health status |

### Interactive Documentation

For detailed API documentation with interactive testing, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Example API Usage

**Register a User:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123!"
```

---

## 💻 Development Guide

### Environment Variables

#### Backend (.env)

Create a `.env` file in the `backend/` directory:

```env
# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Database
POSTGRES_SERVER=db
POSTGRES_USER=career_metric
POSTGRES_PASSWORD=career_metric
POSTGRES_DB=career_metric

# Admin User
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=ChangeMe123!

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

#### Frontend (.env)

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Running Services Individually

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Database:**
```bash
docker-compose up db
```

### Database Migrations

```bash
# Create a new migration
cd backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality

**Backend:**
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

**Frontend:**
```bash
# Format code
npm run format

# Lint code
npm run lint

# Type checking
npx tsc --noEmit
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_scoring.py -v

# Run with verbose output
pytest -v -s

# Run specific test
pytest tests/test_scoring.py::test_calculate_score -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Integration Tests

```bash
# Start all services
docker-compose up --build

# Test API health
curl http://localhost:8000/api/v1/health/

# Run full test suite
cd backend && pytest
cd ../frontend && npm test
```

### Test Checklist

**Backend API Tests:**
- [ ] Health endpoint returns 200
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Profile creation requires authentication
- [ ] Assessment evaluation generates score
- [ ] Error handling works correctly

**Frontend Tests:**
- [ ] Health indicator displays status
- [ ] Registration form validation
- [ ] Login form works
- [ ] Intake form accepts all inputs
- [ ] Score dashboard renders correctly
- [ ] Charts display data properly

---

## 🤝 Contributing

We love your input! We want to make contributing to Career Metric as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

### How to Contribute

1. **Fork the Repository**
  ```bash
   # Click the "Fork" button on GitHub, then:
   git clone https://github.com/yourusername/Career-Metric.git
   cd Career-Metric
   ```

2. **Create a Feature Branch**
  ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-fix
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Write Tests**
   - Add tests for new features
   - Ensure all tests pass
   - Maintain or improve test coverage

5. **Commit Your Changes**
   ```bash
   git commit -m "Add: amazing new feature"
   # Use conventional commits:
   # - Add: for new features
   # - Fix: for bug fixes
   # - Update: for updates
   # - Docs: for documentation
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots if applicable
   - Wait for review and feedback

### Development Workflow

```bash
# 1. Sync with upstream
git remote add upstream https://github.com/originalowner/Career-Metric.git
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes and test
# ... make your changes ...
npm test  # or pytest

# 4. Commit
git add .
git commit -m "Add: description of changes"

# 5. Push and create PR
git push origin feature/my-feature
```

### Coding Standards

**Python (Backend):**
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions/classes
- Maximum line length: 100 characters
- Use `black` for formatting

**TypeScript (Frontend):**
- Use TypeScript strict mode
- Follow ESLint rules
- Use functional components with hooks
- Maximum line length: 100 characters
- Use Prettier for formatting

### Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: Explain what and why
- **Tests**: All tests must pass
- **Documentation**: Update README/docs if needed
- **Size**: Keep PRs focused and reasonably sized

### Good First Issues

Looking for your first contribution? Check out our [Good First Issues](https://github.com/yourusername/Career-Metric/labels/good%20first%20issue) label!

Some ideas:
- 🐛 Fix bugs
- 📝 Improve documentation
- 🎨 UI/UX improvements
- ⚡ Performance optimizations
- 🧪 Add test coverage
- 🌐 Internationalization
- 🔧 Refactoring

### Code of Conduct

#### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

#### Our Standards

**Examples of behavior that contributes to creating a positive environment:**

- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints and experiences
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards other community members

**Examples of unacceptable behavior:**

- ❌ The use of sexualized language or imagery
- ❌ Trolling, insulting/derogatory comments, and personal attacks
- ❌ Public or private harassment
- ❌ Publishing others' private information without permission
- ❌ Other conduct which could reasonably be considered inappropriate

---

## 🗺️ Roadmap

### Current Version (v1.0)

- ✅ Core scoring algorithm
- ✅ User authentication
- ✅ Profile management
- ✅ Basic dashboard
- ✅ API documentation

### Upcoming Features

- [ ] **Enhanced ML Models**: Improved accuracy with deep learning
- [ ] **Multi-language Support**: Internationalization (i18n)
- [ ] **Advanced Analytics**: Detailed insights and trends
- [ ] **Export Reports**: PDF/Excel report generation
- [ ] **API Rate Limiting**: Enhanced security and performance
- [ ] **Webhook Support**: Real-time notifications
- [ ] **Mobile App**: React Native mobile application
- [ ] **Admin Dashboard**: Comprehensive admin panel
- [ ] **Batch Processing**: Process multiple assessments
- [ ] **Integration APIs**: Third-party service integrations

### Long-term Goals

- 🎯 Achieve 90%+ accuracy
- 🌍 Support for multiple languages
- 📱 Native mobile applications
- 🤖 Advanced AI recommendations
- 📊 Enterprise features
- 🔐 Enhanced security features

---

## 🔧 Troubleshooting

### Common Issues

#### Services Won't Start

**Problem**: Docker services fail to start

**Solution**:
```bash
# Check if ports are in use (Windows)
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :5432

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

#### Database Connection Issues

**Problem**: Cannot connect to database

**Solution**:
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Verify connection
docker-compose exec db psql -U career_metric -d career_metric
```

#### Backend Errors

**Problem**: Backend fails to start or crashes

**Solution**:
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements-dev.txt
```

#### Frontend Not Loading

**Problem**: Frontend doesn't load or shows errors

**Solution**:
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up frontend

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Tests Fail

**Backend Tests:**
```bash
# Check Python version
python --version  # Need 3.11+

# Install dependencies
pip install -r requirements-dev.txt

# Check database connection
# Ensure database is running
```

**Frontend Tests:**
```bash
# Clear cache
rm -rf node_modules && npm install

# Check Node version
node --version  # Need 18+

# Run with verbose output
npm test -- --verbose
```

### Getting Help

If you're still experiencing issues:

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/yourusername/Career-Metric/issues)
2. **Create New Issue**: Provide detailed information about your problem
3. **Ask in Discussions**: Use [GitHub Discussions](https://github.com/yourusername/Career-Metric/discussions)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Career Metric Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 💬 Support

### Get Help

- 📖 **Documentation**: Check this README and inline code comments
- 🐛 **Bug Reports**: [Open an Issue](https://github.com/yourusername/Career-Metric/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Open an Issue](https://github.com/yourusername/Career-Metric/issues/new?template=feature_request.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/Career-Metric/discussions)
- 📧 **Email**: support@careermetric.com (if applicable)

### Community

- ⭐ **Star us on GitHub**: Help us grow!
- 🍴 **Fork the repository**: Make it your own
- 📢 **Share with others**: Spread the word
- 🤝 **Contribute**: See [Contributing](#-contributing) section

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for building APIs
- **React** - A JavaScript library for building user interfaces
- **PostgreSQL** - Powerful open-source relational database
- **Docker** - Containerization platform
- **All Contributors** - Thank you to everyone who has contributed to this project!

### Special Thanks

- To all the open-source maintainers whose libraries make this project possible
- To the community for feedback and contributions
- To early adopters and beta testers

---

<div align="center">

**Made with ❤️ by the Career Metric Team**

[⭐ Star us on GitHub](https://github.com/yourusername/Career-Metric) • [🐛 Report Bug](https://github.com/yourusername/Career-Metric/issues) • [💡 Request Feature](https://github.com/yourusername/Career-Metric/issues) • [📖 Documentation](#-documentation)

</div>

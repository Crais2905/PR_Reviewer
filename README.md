# 🤖 AI PR Reviewer

AI-powered backend service that automatically reviews GitHub Pull Requests using **Google Gemini**.

The user only provides a **GitHub Pull Request URL**. The system asynchronously fetches the PR diff via the **GitHub API**, analyzes the changes with **Gemini**, and stores a **structured review report** containing a summary, risk assessment, and categorized findings.

---

## ✨ Features

* 🔐 JWT authentication (access + refresh tokens)
* 🔗 GitHub Pull Request integration
* 🤖 AI-powered code review using **Google Gemini**
* ⚙️ Asynchronous processing with **Celery + Redis**
* 📊 Structured AI findings (security, performance, maintainability, etc.)
* 🚦 Review status tracking (`pending → processing → completed / failed`)
* 🧪 Fully tested with **Pytest**
* 🗄️ Async PostgreSQL integration with **SQLAlchemy 2.0**
* 🔄 Database migrations with **Alembic**

---

## 🧠 What the AI Returns

Each review contains:

* **Summary** — short explanation of the PR
* **Risk level** — `low`, `medium`, or `high`
* **Overall comment** — general assessment
* **Findings** — structured list of detected issues

Example:

```json
{
  "summary": "Introduces Redis caching for product retrieval.",
  "risk": "medium",
  "overall_comment": "Implementation is generally good, but cache invalidation should be reviewed.",
  "finding_problems": [
    {
      "title": "Incomplete cache invalidation",
      "category": "performance",
      "severity": "medium",
      "description": "The cache is not invalidated when products are deleted.",
      "recommendation": "Invalidate cache entries after delete operations."
    }
  ]
}
```

---

## 🛠️ Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Framework        | FastAPI                 |
| Database         | PostgreSQL              |
| ORM              | SQLAlchemy 2.0 (async)  |
| Migrations       | Alembic                 |
| Background Jobs  | Celery                  |
| Broker / Backend | Redis                   |
| AI               | Google Gemini           |
| External API     | GitHub REST API         |
| Validation       | Pydantic                |
| Testing          | Pytest + pytest-asyncio |
| HTTP Client      | HTTPX                   |

---

## 🔄 Review Workflow

```text
1. User submits a GitHub Pull Request URL
           │
           ▼
2. API creates a Review with status = pending
           │
           ▼
3. Celery starts background processing
           │
           ▼
4. GitHub API downloads the PR diff
           │
           ▼
5. Gemini analyzes the code changes
           │
           ▼
6. AI returns summary, risk, and findings
           │
           ▼
7. Review status becomes completed
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-pr-reviewer.git
cd ai-pr-reviewer
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start Redis

Make sure Redis is running locally:

```bash
redis-server
```

### 7. Start Celery worker

```bash
celery -A app.celery_app.celery worker --loglevel=info
```

### 8. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

API will be available at:

* **API:** http://localhost:8000
* **Swagger UI:** http://localhost:8000/docs

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_pr_reviewer

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7


GEMINI_API_KEY=your-gemini-api-key
GITHUB_TOKEN=your-github-personal-access-token
```

> Never commit your `.env` file.

---

## 📚 API Reference

### Authentication

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| `POST` | `/auth/register/` | Register a new user      |
| `POST` | `/auth/login/`    | Login and receive tokens |
| `POST` | `/auth/logout/`   | Logout current session   |
| `GET`  | `/auth/profile/`  | Get current user profile |
| `POST` | `/auth/refresh/`  | Refresh access token     |

### Reviews

| Method | Endpoint               | Description                                 |
| ------ | ---------------------- | ------------------------------------------- |
| `POST` | `/reviews/`            | Create a new AI review from a GitHub PR URL |
| `GET`  | `/reviews/`            | Get all reviews for the current user        |
| `GET`  | `/reviews/{review_id}` | Get a specific review with AI results       |

---

## 🧪 Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_review.py -v
```

Tests use mocked GitHub and Gemini responses to avoid external API calls during CI and local development.

---

## 🗄️ Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback the last migration:

```bash
alembic downgrade -1
```

---

## 📄 License

MIT License

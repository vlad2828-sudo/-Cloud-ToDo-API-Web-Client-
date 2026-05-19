# Cloud ToDo API + Web Client MVP

Production-oriented MVP for a cloud ToDo service:

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Alembic, layered architecture.
- **Frontend:** React + Vite + TypeScript.
- **Local runtime:** Docker Compose with PostgreSQL, API and Web UI.
- **Cloud target:** AWS App Runner or ECS Fargate fallback, Amazon RDS PostgreSQL, Secrets Manager, S3 + CloudFront, CloudWatch, ECR.
- **CI/CD:** GitHub Actions for lint, tests, Docker build and ECR push.

> Note: `X-API-Key` in a browser frontend is acceptable only for an educational MVP. For production, use Cognito/JWT or keep write operations behind a backend-controlled session.

---

## 1. Quick start: local Docker launch

Requirements:

- Docker
- Docker Compose

Run:

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Web UI: <http://localhost:3000>
- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- Health: <http://localhost:8000/health>

Default local API key:

```text
X-API-Key: dev-api-key-change-me
```

---

## 2. Local backend without Docker

Requirements:

- Python 3.12+
- PostgreSQL or SQLite for quick tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

cp ../.env.example .env
export DATABASE_URL="sqlite:///./todo_local.db"
export API_KEY="dev-api-key-change-me"

alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 3. Local frontend without Docker

Requirements:

- Node.js 20+

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open: <http://localhost:5173>

---

## 4. API contract

### Task

```json
{
  "id": "uuid",
  "title": "string, required, 3-120",
  "description": "string, optional, max 500",
  "status": "NEW | IN_PROGRESS | DONE",
  "priority": "LOW | MEDIUM | HIGH",
  "dueDate": "2026-05-01",
  "createdAt": "2026-04-26T10:00:00Z",
  "updatedAt": "2026-04-26T10:00:00Z"
}
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/tasks` | Create task |
| `GET` | `/api/tasks` | List tasks with `status`, `priority`, `limit`, `offset` |
| `GET` | `/api/tasks/{id}` | Get task by ID |
| `PUT` | `/api/tasks/{id}` | Full update |
| `PATCH` | `/api/tasks/{id}` | Partial update: `status` and/or `priority` |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `GET` | `/health` | Health check |

### Error format

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "details": [
    {
      "field": "title",
      "message": "String should have at least 3 characters"
    }
  ]
}
```

---

## 5. Tests and quality gates

```bash
cd backend
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest
```

The backend contains:

- unit tests for service layer;
- integration tests for API endpoints;
- validation and error tests.

---

## 6. AWS deployment outline

### Backend

1. Create ECR repository.
2. Create RDS PostgreSQL database in private subnets.
3. Store secrets in AWS Secrets Manager:
   - `DATABASE_URL`
   - `API_KEY`
4. Deploy backend container to App Runner if available for your AWS account.
5. If App Runner is unavailable, deploy to ECS Fargate + ALB.
6. Enable CloudWatch Logs.
7. Configure CORS with your CloudFront domain.

### Frontend

1. Build frontend:

```bash
cd frontend
VITE_API_BASE_URL=https://your-api-domain.example.com npm run build
```

2. Upload `frontend/dist` to a private S3 bucket.
3. Serve via CloudFront.
4. Invalidate CloudFront cache after each deployment.

---

## 7. GitHub Actions secrets

Required for backend ECR push:

```text
AWS_GITHUB_ROLE_ARN
AWS_REGION
ECR_REPOSITORY
```

Optional for frontend deploy:

```text
FRONTEND_S3_BUCKET
CLOUDFRONT_DISTRIBUTION_ID
VITE_API_BASE_URL
VITE_API_KEY
```

---

## 8. Repository layout

```text
cloud-todo-mvp/
  backend/
    app/
    migrations/
    tests/
    Dockerfile
    requirements.txt
    requirements-dev.txt
    pyproject.toml
  frontend/
    src/
    Dockerfile
    nginx.conf
    package.json
  infra/
    aws/
      README.md
  .github/
    workflows/
      backend-ci-cd.yml
      frontend-ci-cd.yml
  docker-compose.yml
  .env.example
```

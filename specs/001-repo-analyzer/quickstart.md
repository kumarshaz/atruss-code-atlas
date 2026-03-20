# Quickstart: Repository Analyzer

## Prerequisites
- Python 3.12+
- PostgreSQL (running locally or via Docker)
- Redis
- GitHub PAT (optional, but recommended for avoiding rate limits)

## Local Setup

1. **Clone and Install**
```bash
git clone <repo-url> atruss-code-atlas
cd atruss-code-atlas
python -m venv .venv
# On Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Configuration**
Create a `.env` file based on `.env.example`:
```ini
GITHUB_TOKEN=your_pat_here
DATABASE_URL=postgresql://user:password@localhost:5432/repoanalyzer
REDIS_URL=redis://localhost:6379/0
```

3. **Database Migrations**
```bash
alembic upgrade head
```

4. **Run Analysis**
```bash
python -m repo_analyzer discover --org your-org
```

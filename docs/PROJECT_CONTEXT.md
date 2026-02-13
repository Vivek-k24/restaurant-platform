# Restaurant Platform – Project Context

## Architecture
- Frontend Tablet: React Native (Android)
- Backend: FastAPI (Python 3.11)
- Database: PostgreSQL
- Local Infra: Docker Compose
- Testing: pytest
- Logging: structlog

## Goal of MVP
Deliver a working vertical slice:
1. Backend /health endpoint
2. PostgreSQL running locally
3. Tablet app can call backend and display status

## Development Rules
- All changes via feature branches
- Small PRs only
- Must pass:
  - pytest
  - ruff lint
- Do not refactor unrelated code
- Keep structure clean and minimal

## Current State
Walking skeleton is being built.

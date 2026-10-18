# HelioDesk — Customer Support AI Agent Platform

A Django customer-support dashboard with PostgreSQL support, ticket tools, optional LLM endpoint, audit events, demo data, and Docker Compose.

## Features
- Ticket inbox with search/filtering and priority/status indicators
- Django ORM models for tickets and ticket events
- Explicit tool registry: read ticket, search tickets, draft reply, resolve ticket
- Optional OpenAI-compatible chat completions endpoint and deterministic fallback
- Reply drafts can be edited and saved, but are never automatically sent
- Django admin, health endpoint, synthetic sample tickets, responsive dashboard

## Run locally (SQLite)
Python 3.11+:
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Open http://127.0.0.1:8000.

## Run with PostgreSQL
Install Docker Compose and run:
```bash
docker compose up --build
```
Open http://localhost:8000.

## Optional LLM
Set LLM_API_URL, LLM_API_KEY, and LLM_MODEL in `.env`. The endpoint should accept OpenAI-compatible chat-completions requests. If unset, local fallback works without network calls. Model output is treated as text and cannot invoke arbitrary tools.

## API
- GET `/api/health/`
- GET `/api/tickets/`
- POST `/api/agent/run/` JSON: `{"message":"Summarize ticket","ticket_id":1}`
- POST `/api/tickets/<id>/reply/` JSON: `{"draft":"..."}`
- Django admin: `/admin/`

## Before production
Add authentication and authorization to APIs, secure secrets, set DEBUG=0, configure HTTPS/secure cookies, validate all tool permissions, add rate limits, robust structured tool calling, monitoring, backups, privacy controls, and a security review. This starter is not safe to expose publicly as-is.

## Metrics disclaimer
The resume figures (8,500 monthly users, 94% uptime, 87% test coverage, 41% fewer escalations, 22 tools/9 services) are not proven by this starter. Verify metrics using actual deployment telemetry and test reports before claiming them as measured results.

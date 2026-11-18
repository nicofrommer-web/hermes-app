# HERMES Command Center — API and persistent dashboard

This is the separate HERMES B2B workspace. It is not connected to NEXORA or any Shopify project.

## What is now connected

- The dashboard is served by the same FastAPI application as the API (same origin).
- Admin login uses a signed, HTTP-only session cookie; the browser never receives the service API token.
- Dashboard workspace snapshots (leads, tasks, approvals, agent settings, workflow settings and audit entries) are saved in the configured database.
- Workspace rows are scoped to the server-configured `HERMES_TENANT_ID`.
- The browser redirects to the login page when its session expires.
- Mutating browser requests with a cross-origin Origin header are rejected.

## Run locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

Set the environment values from `backend/.env.example` in your shell (or use your deployment provider's secret manager). For local HTTP only, set `HERMES_COOKIE_SECURE=false`. Then run:

```bash
uvicorn backend.app:app --reload
```

Open `http://127.0.0.1:8000`. Sign in with `HERMES_ADMIN_USER` and `HERMES_ADMIN_PASSWORD`. The first start creates clearly labeled synthetic demo records in the database. The public demo page is available at `/website/`; its analysis endpoint is deliberately separate from tenant data and does not create leads, tasks, or approvals.

## Deploy as one container

Build from the repository root (not from the backend subfolder):

```bash
docker build -f backend/Dockerfile -t hermes-command-center .
docker run -p 8000:8000 --env-file backend/.env hermes-command-center
```

Use a managed PostgreSQL database and HTTPS in hosted environments. Configure all secrets server-side:
- `HERMES_TENANT_ID`: unique internal tenant key.
- `HERMES_SESSION_SECRET`: long random secret (at least 32 random bytes).
- `HERMES_ADMIN_USER` and `HERMES_ADMIN_PASSWORD`: unique admin credentials.
- `HERMES_COOKIE_SECURE=true` in production.
- `DATABASE_URL`: managed PostgreSQL connection string using the psycopg driver.

Do not commit a real `.env` file. Do not put credentials or tokens into the HTML, JavaScript, GitHub repository, or browser storage.

## API

- `POST /api/login`, `GET /api/session`, `POST /api/logout`
- `GET/PUT /api/workspace` — full workspace snapshot, maximum 1 MB
- `GET/POST /api/leads`
- `GET/POST /api/tasks`
- `GET/POST /api/approvals`
- `POST /api/approvals/{id}/decision` — pending-only decision
- `GET /api/audit`
- `GET /health`

## Current limitations — read before real use

This is a single-admin MVP, not yet a multi-user SaaS. It does not yet provide per-user RBAC, password reset, MFA, rate limiting, automated database migrations, backup scheduling, monitoring, or a formal security review. Workspace snapshots are tenant-scoped, but the single configured admin is not a full customer account system. Use only synthetic/demo data until these controls are implemented and reviewed.

Agent roles and workflow switches remain configuration only. No model calls, email sending, CRM integrations, autonomous actions, or external business operations are enabled. An approval records a decision; it does not execute the approved action. The workspace currently persists a complete JSON snapshot, while the normalized leads/tasks/approvals/audit tables remain available for future migration to granular persistence.

# HERMES API foundation

FastAPI service for the separate HERMES B2B Command Center. It is not connected to NEXORA or any Shopify store.

## Local run

1. Create a virtual environment and install `requirements.txt`.
2. Set `HERMES_API_TOKEN` to a long random secret and `HERMES_TENANT_ID` to a unique tenant identifier.
3. Set `DATABASE_URL=sqlite:///./hermes-dev.db` for local-only development, or a managed PostgreSQL URL.
4. Run `uvicorn app:app --reload` from this folder.
5. Open `/docs` for the API contract and `/health` for a health check.

## Endpoints

- `GET/POST /api/leads`
- `GET/POST /api/tasks`
- `GET/POST /api/approvals`
- `POST /api/approvals/{id}/decision` (pending-only, idempotency guarded by state)
- `GET /api/audit`

All `/api/*` routes require `Authorization: Bearer <HERMES_API_TOKEN>`. Every query is scoped to the single `HERMES_TENANT_ID` configured for this deployment. Do not expose the token in browser code. The browser dashboard must call a trusted server-side adapter; it must never contain the API token.

## Important status

This is a first backend foundation, not a production-ready multi-customer SaaS. Authentication is a single service token, not user login; tenant identity is configured server-side; no email/CRM integrations or AI execution are enabled. Use managed PostgreSQL, secret storage, HTTPS, backups, rate limiting, monitoring, migrations, user-level RBAC, and security review before real customer data or external use. Approval decisions are recorded only; they do not execute the approved action.

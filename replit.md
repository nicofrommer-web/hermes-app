# HERMES on Replit

## Run command

The repository-root `.replit` file installs the existing Python requirements and starts the existing FastAPI application:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

The dashboard is served by FastAPI from `command-center/`. The API health endpoint is `/health`.

## Required Replit Secrets

Before the first run, configure these in the Replit Secrets tool. Never commit them to Git:

- `HERMES_TENANT_ID`: a private test tenant identifier
- `HERMES_SESSION_SECRET`: a long random secret (at least 32 random bytes)
- `HERMES_ADMIN_USER`: a private test admin username
- `HERMES_ADMIN_PASSWORD`: a unique strong test password

For a private local/test Replit workspace, the default database is SQLite at `./hermes-dev.db`. Do not add a public production database or real customer data during initial testing. The application currently requires the four secrets above and intentionally does not invent default credentials.

For a hosted HTTPS deployment, set `HERMES_COOKIE_SECURE=true`. For local HTTP-only development, `HERMES_COOKIE_SECURE=false` may be used only in a private test environment.

## First-run verification

1. Start the Repl.
2. Confirm `GET /health` returns JSON with status `ok`.
3. Open the app preview and confirm the login page appears.
4. Sign in using the test credentials stored in Replit Secrets.
5. Use synthetic data only.

## Current limitations

This is an MVP. Do not treat it as production-ready or enter customer information. Authentication is single-admin; MFA, rate limiting, password recovery, automated migrations, scheduled backups, monitoring and a security review remain outstanding. Workflow/agent controls are configuration only; approval decisions are recorded but do not trigger external actions. Optional AI analysis is not enabled by this run configuration.

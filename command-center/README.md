# HERMES Command Center

Isolated B2B operations dashboard for HERMES. This project is separate from NEXORA and all Shopify ventures.

## Dashboard capabilities
- Lead CRM with create/edit/search/filter and CSV export
- Customer view and research intake
- Six configurable agent-role cards
- Workflow templates and toggles
- Task management
- Human approval queue
- Analytics and audit log
- Login/logout page
- Server-side workspace persistence through the FastAPI API

## Run and deploy
The dashboard is served by the backend application from the same origin. Follow [the backend setup guide](../backend/README.md). Build the Docker image from the repository root using `docker build -f backend/Dockerfile -t hermes-command-center .`.

## Current limits
The app is a single-admin MVP. It persists the workspace in the configured database and protects the browser session with a signed HTTP-only cookie. Use a managed PostgreSQL database and HTTPS for hosting. Configure secrets only in the server environment.

The first-run records are synthetic examples, not real prospects or customers. Agent cards and workflow toggles are configuration only; no model execution, email sending, CRM integrations, or autonomous external actions are active. Approval decisions are recorded but do not execute anything.

Before real customer data or multi-customer use, add and review user-level RBAC, MFA, password reset, rate limiting, database migrations, scheduled backups, monitoring, privacy/legal controls, and a security review.

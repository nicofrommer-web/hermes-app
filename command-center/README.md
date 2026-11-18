# HERMES Command Center

Isolated B2B command-center MVP for the HERMES business. This folder is separate from NEXORA and all Shopify projects.

## Current scope
- Lead CRM with create/edit/search/filter and CSV export
- Customer view
- Research intake and source-note fields
- Six agent-role controls
- Workflow templates and toggles
- Task management
- Human approval queue
- Analytics from local records
- Audit log and CSV backup

## Safety and current limitations
This is a browser-only prototype. It uses LocalStorage and synthetic seed records. It has no server database, authentication, multi-user access, AI model execution, or live business integrations. Do not enter real customer personal data or secrets. Agent switches and workflow toggles configure the demo UI only; they do not start autonomous agents. Approvals record a decision locally and do not send anything externally.

Production work still required: server-side API, database with tenant isolation, authentication/RBAC, secure secret storage, backups, monitoring, privacy/legal review, integration testing and deployment hardening.

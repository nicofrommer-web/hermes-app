# Production readiness checklist for HERMES

## Done
- [x] Fly.io config (`fly.toml`)
- [x] Postgres attachment instructions
- [x] Secrets management guide
- [x] Live dashboard metrics endpoint (`/api/dashboard/summary`)
- [x] Health check
- [x] Session-based auth + optional API token
- [x] Audit logging
- [x] Dockerfile

## Recommended next (optional)
- [ ] Rate limiting on `/api/login` (e.g. 5 attempts / minute)
- [ ] Sentry for error tracking
- [ ] Automated Postgres backups
- [ ] Custom domain + Cloudflare in front
- [ ] Multi-tenant support beyond single `HERMES_TENANT_ID`

## Deploy command reminder
```bash
fly deploy
```

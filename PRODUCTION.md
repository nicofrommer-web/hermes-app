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
- [x] Rate limiting dependency (`slowapi`) + example
- [x] Backup helper script (`scripts/backup.sh`)

## Recommended next (optional)
- [ ] Rate limiting fully activated in `app.py` (see RATE_LIMIT.md)
- [ ] Sentry for error tracking
- [ ] Automated scheduled backups
- [ ] Custom domain + Cloudflare in front
- [ ] Multi-tenant support beyond single `HERMES_TENANT_ID`

## Deploy command reminder
```bash
fly deploy
```

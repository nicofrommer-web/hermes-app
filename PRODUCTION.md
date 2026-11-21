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
- [x] Rate limiting activated on `/api/login` (5 attempts per minute per IP; covered by pytest)
- [ ] Sentry for error tracking
- [ ] Automated scheduled backups (the helper only requests a backup; scheduling and restore verification remain open)
- [ ] Custom domain + Cloudflare in front
- [ ] Multi-tenant support beyond single `HERMES_TENANT_ID`

## Deploy command reminder
```bash
fly deploy
```

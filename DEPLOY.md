# HERMES Production Deployment (Fly.io)

## 1. Voraussetzungen
- Fly.io CLI installiert (`flyctl`)
- Angemeldet: `fly auth login`

## 2. App erstellen & Postgres
```bash
cd /path/to/hermes-app
fly launch --name hermes-backend --region fra --no-deploy
fly postgres create --name hermes-db --region fra
fly postgres attach hermes-db --app hermes-backend
```

## 3. Secrets setzen
```bash
fly secrets set \
  HERMES_TENANT_ID="hermes-main" \
  HERMES_SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')" \
  HERMES_ADMIN_USER="admin" \
  HERMES_ADMIN_PASSWORD="DEIN-STARKES-PASSWORT" \
  HERMES_COOKIE_SECURE="true"
```

`DATABASE_URL` wird durch `fly postgres attach` automatisch gesetzt.

## 4. Deploy
```bash
fly deploy
```

## 5. Health-Check
```bash
curl https://hermes-backend.fly.dev/health
```

## 6. Frontend
Das Command Center wird aktuell vom Backend mit ausgeliefert (StaticFiles).
Für spätere Skalierung kann das `website/` und `command-center/` auf Cloudflare Workers ausgelagert werden.

## Wichtige Hinweise
- Niemals echte Passwörter in Git committen.
- Vor echtem Betrieb: Backup-Strategie für Postgres einrichten (`fly postgres backup` oder managed).
- Rate-Limiting und Monitoring (Sentry) als nächste Schritte empfohlen.

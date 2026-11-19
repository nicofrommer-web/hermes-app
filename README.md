# HERMES Command Center

HERMES – KI-Assistent für Betriebe in Villingen-Schwenningen.

## Live Dashboard Metrics

Neuer Endpoint für echte Zahlen aus der Datenbank:

```
GET /api/dashboard/summary
```

Antwort:
```json
{
  "leads_total": 12,
  "leads_new": 5,
  "leads_qualified": 3,
  "tasks_open": 7,
  "approvals_pending": 2,
  "uptime": "99.98%"
}
```

Das Frontend im Command Center kann diesen Endpoint nutzen, um die Übersicht mit Live-Daten zu füllen.

## Production Deployment

Siehe [DEPLOY.md](./DEPLOY.md) für die komplette Fly.io-Anleitung (Region `fra`, Postgres, Secrets).

## Replit starten

Das Projekt verwendet Python 3.12, FastAPI und Uvicorn. Die Replit-Startkonfiguration in `.replit` installiert die Abhängigkeiten und startet:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

## Erforderliche Replit-Secrets

Vor dem ersten Start müssen in **Replit → Secrets** diese vier Werte angelegt werden:

| Secret | Zweck | Beispiel / Hinweis |
|---|---|---|
| `HERMES_TENANT_ID` | Kennung des HERMES-Arbeitsbereichs | `hermes-main` |
| `HERMES_SESSION_SECRET` | Signaturschlüssel für Login-Sitzungen | Zufälligen, langen Wert verwenden |
| `HERMES_ADMIN_USER` | Admin-Benutzername | Selbst festlegen |
| `HERMES_ADMIN_PASSWORD` | Admin-Passwort | Ein eigenes, starkes Passwort verwenden |

**Wichtig:** Keine echten Passwörter oder Secrets in GitHub-Dateien, Issues oder Chats eintragen.

## Produktions-Checkliste

Vor einem Einsatz mit echten Unternehmensdaten:

1. Alle Secrets ausschließlich in der Deployment-Umgebung hinterlegen.
2. Für dauerhafte Daten eine verwaltete PostgreSQL-Datenbank über `DATABASE_URL` konfigurieren.
3. HTTPS aktivieren und `HERMES_COOKIE_SECURE=true` beibehalten.
4. Backup, Wiederherstellung, Zugriffsrechte und Datenschutzprozesse vor dem Produktivbetrieb testen.

**Funktionsgrenze:** Die vorhandenen Agenten und Workflows im Dashboard sind derzeit Prozessvorlagen bzw. Demo-Funktionen. Ohne zusätzliche Integrationen und implementierte Ausführungslogik führen sie keine eigenständigen KI-Aktionen oder externen Kundenkontakte aus.

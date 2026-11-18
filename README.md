# HERMES Command Center

HERMES – KI-Assistent für Betriebe in Villingen-Schwenningen.

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

Einen zufälligen Sitzungsschlüssel kannst du lokal mit folgendem Befehl erzeugen:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Optionale Umgebungsvariablen:

- `DATABASE_URL`: Datenbankverbindung. Ohne Angabe verwendet die App eine lokale SQLite-Datei `hermes-dev.db`.
- `HERMES_API_TOKEN`: Optionaler Bearer-Token für API-Zugriffe.
- `HERMES_COOKIE_SECURE`: Standard ist `true`; für HTTPS so belassen.

## Gesundheitsprüfung

Nach erfolgreichem Start die Replit-Webview öffnen und `/docs` aufrufen. Die FastAPI-Dokumentation sollte erscheinen. Wenn der Prozess beim Start abbricht, zuerst prüfen, ob alle vier erforderlichen Secrets korrekt gesetzt sind.

## Datenhinweis

Die Anwendung legt Tabellen beim Start automatisch an. Für dauerhafte Produktionsdaten sollte eine verwaltete PostgreSQL-Datenbank über `DATABASE_URL` verwendet werden. SQLite in einer flüchtigen Entwicklungsumgebung ist nicht als verlässliche Produktionsspeicherung gedacht.

## GitHub Actions / automatische Prüfung

Bei jedem Push auf `main` und bei Pull Requests nach `main` führt GitHub Actions die Backend-Smoke-Tests mit Python 3.12 aus. Die dort verwendeten Zugangsdaten sind ausschließlich temporäre CI-Testwerte und dürfen nicht für einen echten Betrieb verwendet werden.

Den Status findest du im Repository unter **Actions → HERMES backend tests**. Ein grüner Lauf ist Voraussetzung für die technische Freigabe des jeweiligen Commits.

## Produktions-Checkliste

Vor einem Einsatz mit echten Unternehmensdaten:

1. Alle vier erforderlichen Secrets ausschließlich in der Deployment-Umgebung hinterlegen.
2. Für dauerhafte Daten eine verwaltete PostgreSQL-Datenbank über `DATABASE_URL` konfigurieren.
3. HTTPS aktivieren und `HERMES_COOKIE_SECURE=true` beibehalten.
4. Ein individuelles, starkes Admin-Passwort und einen zufälligen `HERMES_SESSION_SECRET` verwenden.
5. Nach dem Deployment `/health` prüfen. Die Antwort muss HTTP 200 sowie `"database": "ok"` enthalten.
6. Backup, Wiederherstellung, Zugriffsrechte und Datenschutzprozesse vor dem Produktivbetrieb testen.

**Funktionsgrenze:** Die vorhandenen Agenten und Workflows im Dashboard sind derzeit Prozessvorlagen bzw. Demo-Funktionen. Ohne zusätzliche Integrationen und implementierte Ausführungslogik führen sie keine eigenständigen KI-Aktionen oder externen Kundenkontakte aus.

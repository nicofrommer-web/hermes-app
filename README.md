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

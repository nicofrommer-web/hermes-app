# Dashboard Live-Metriken

Die Übersicht im Command Center (`command-center/index.html`) wurde so angepasst, dass sie den Endpoint `/api/dashboard/summary` aufruft.

## Verhalten
- Beim Laden der Übersicht wird `/api/dashboard/summary` abgefragt.
- Die Zahlen (Leads gesamt, Offene Aufgaben, Freigaben ausstehend) kommen aus der echten Datenbank.
- Bei Verbindungsfehler fällt das System auf die lokalen Workspace-Daten zurück.
- Der Demo-Hinweis wurde durch einen "Live-Daten"-Hinweis ersetzt.

## Nächster Schritt
Nach dem Deploy auf Fly.io die Übersicht öffnen – die Metriken sollten live aus der DB kommen.

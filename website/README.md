# HERMES public website

Standalone, responsive German-language product and demo page.

## Preview locally

Open `index.html` in a browser. No build step or third-party dependency is required.

## Demo behavior

- The interactive request preview uses simple browser-side keyword rules.
- No request text is sent to a server or stored.
- The page explicitly asks visitors not to enter real customer or confidential business data.
- It is a product concept/demo page, not a production AI service or customer intake channel.

## Publishing

This folder can be deployed as a static site by a hosting provider using `website/` as the output/root directory. Configure a custom domain only after ownership, legal pages, contact details, and the hosting configuration have been reviewed.

Before public commercial launch, add verified company/contact details, privacy and legal notices appropriate to the operator, accessibility checks, analytics only with appropriate consent, and a security/legal review. Do not collect customer data until the backend and privacy controls are ready.

## Backend connection

When served by the HERMES FastAPI app, the page is available at `/website/` and posts demo text to `POST /api/demo/analyze`. The endpoint is public, stateless, limited to 3,000 characters per request and uses a simple in-memory per-IP request limit. It returns a rule-based preview only; it does not call an AI model, write to the database, create approvals, or send messages. Do not enter personal, customer, or confidential data.

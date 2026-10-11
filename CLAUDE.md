# Instructions for AI coding agents

- Never hardcode a secret, API key, token, or connection string in code. Never paste a literal value as a "temporary" placeholder either, even one meant to be replaced later.
- This project's available Key Vault secrets are listed at the start of every conversation (a system note naming each key and a one-line description). Fetch a value with:
  ```python
  from app.core.key_vault import get_secret
  value = get_secret("<key-name>")
  ```
  Use the exact key name given in that note.
- If the secret you need isn't in that list, stop and tell the user to add it via the Studio's "Secrets" panel. Suggest a kebab-case key name (e.g. `stripe-api-key`) and a short description, rather than inventing a value or writing a TODO with a fake one.
- The app still runs fine on `.env` defaults (SQLite, a generated `SECRET_KEY`) when no Key Vault is configured at all. That's the normal local/offline path and nothing about it changes.
- `database_url` and `secret_key` in `app/core/config.py` are reserved for THIS app's own built-in database and signing key only — they're already wired vault-first in `get_settings()`, and that's as far as their scope goes. Do not repoint `database_url` at a different data source just because it's also "a database" — it stays pointed at this app's own store.
- Any other external system a request needs — a different database, a third-party API, another service — gets its own new secret key, named for what it actually is (e.g. `ms-db-connection-string`, `stripe-api-key`), fetched directly at its point of use via `get_secret(name)`. Never add it to `Settings` and never route it through `database_url`/`secret_key`. Do this automatically, the first time it comes up, without being asked: write the code against the new key name you chose, and tell the user to add that exact key (plus a short description) via the Studio's "Secrets" panel — don't wait for them to notice you reused the wrong field.

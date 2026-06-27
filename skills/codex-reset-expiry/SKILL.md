---
name: codex-reset-expiry
description: Query Codex Desktop rate-limit reset credit expiration dates from the local signed-in Codex auth session. Use when the user asks when Codex reset credits expire, how long available resets remain valid, to check reset expiry dates, or to inspect reset credit grants without modifying the Codex Desktop app.
---

# Codex Reset Expiry

## Purpose

Query the same reset-credit backend that Codex Desktop uses:

`https://chatgpt.com/backend-api/wham/rate-limit-reset-credits`

Use this skill to answer account-specific questions such as "when do my Codex resets expire?" or "check the expiry dates for my available reset credits."

## Workflow

1. Run the bundled script:

```bash
python <skill-dir>/scripts/query_reset_credits.py
```

2. Report only the available count and reset credit dates. Do not print, copy, save, or summarize tokens.

3. If the script cannot authenticate, ask the user to sign in to Codex Desktop or Codex CLI and try again. Do not ask the user to paste an access token.

4. If the endpoint fails or changes, state that the internal endpoint did not return usable reset-credit data and fall back to visible UI information only.

## Safety Rules

- Never print `access_token`, `refresh_token`, `id_token`, authorization headers, or the full auth file.
- Never persist response data unless the user explicitly asks for a saved report.
- Do not patch or modify the original WindowsApps Codex installation for a simple expiry query.
- Treat this as an unofficial local convenience workflow. The endpoint and response shape may change.

## Script Notes

`scripts/query_reset_credits.py` reads `~/.codex/auth.json`, uses the access token and account id in memory, calls the reset-credit endpoint, and prints a sanitized summary. Use `--json` only when a structured sanitized response is useful.

---
name: codex-reset-expiry
description: "Query available Codex Desktop rate-limit reset credit expiration dates from the local signed-in Codex auth session. Use when the user asks when Codex reset credits expire, how long reset credits remain valid, to check reset expiry dates, to inspect reset credit grants, or asks in Chinese: 查 Codex reset 到期日, 查询重置次数有效期, 重置次数什么时候过期. This skill is read-only and must not modify Codex Desktop."
---

# Codex Reset Expiry

Co-created by `ebxk` and Codex.

## Quick Start

Run the bundled script:

```bash
python <skill-dir>/scripts/query_reset_credits.py
```

Use `--lang en`, `--lang zh`, or `--lang both` when the user wants a specific output language. Use `--json` only when structured sanitized output is useful.

## What To Report

- Available reset credit count.
- Each available reset credit's expiration time.
- Grant time only when it helps explain the result.
- A short caveat that the endpoint is internal and may change.

## Safety Rules

- Never print `access_token`, `refresh_token`, `id_token`, authorization headers, or raw auth file contents.
- Never ask the user to paste a token.
- Never patch, overwrite, or modify Codex Desktop for this query.
- If authentication fails, ask the user to sign in to Codex Desktop or Codex CLI and retry.
- If the endpoint fails or changes, say the live reset-credit endpoint did not return usable data.

## Notes

The script reads the local Codex auth session from `CODEX_HOME/auth.json` or `~/.codex/auth.json`, uses credentials only in memory, calls `https://chatgpt.com/backend-api/wham/rate-limit-reset-credits`, and prints a sanitized summary.

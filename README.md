# codex-reset-expiry-skill

A small Codex skill that checks the expiration dates for available Codex rate-limit reset credits.

The skill calls the same reset-credit endpoint used by Codex Desktop:

```text
https://chatgpt.com/backend-api/wham/rate-limit-reset-credits
```

It reads the local Codex auth session from `~/.codex/auth.json`, uses the access token only in memory, and prints a sanitized summary with available reset counts and expiration dates.

## Install

Copy the skill folder into your Codex skills directory:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\codex-reset-expiry" "$env:USERPROFILE\.codex\skills\codex-reset-expiry"
```

Restart Codex or start a new Codex session, then ask:

```text
Use $codex-reset-expiry to check when my Codex reset credits expire.
```

You can also run the script directly:

```powershell
python .\skills\codex-reset-expiry\scripts\query_reset_credits.py
```

## Safety

- Do not paste or share tokens.
- The script does not print `access_token`, `refresh_token`, `id_token`, or authorization headers.
- The script does not modify Codex Desktop or WindowsApps files.
- This uses an internal endpoint that may change.

## License

MIT

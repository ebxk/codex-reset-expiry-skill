# codex-reset-expiry-skill

English | 中文

A small Codex skill that checks the expiration dates for available Codex rate-limit reset credits.

Co-created by `ebxk` and Codex.

The skill calls the same reset-credit endpoint used by Codex Desktop:

```text
https://chatgpt.com/backend-api/wham/rate-limit-reset-credits
```

It reads the local Codex auth session from `CODEX_HOME/auth.json` or `~/.codex/auth.json`, uses the access token only in memory, and prints a sanitized summary with available reset counts and expiration dates.

## Scope

This project is intentionally small:

- live reset credit count
- available reset credit expiration dates
- no Codex Desktop patching
- no local session snapshot parsing
- no token printing or persistence

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

The script prints bilingual output by default. Use `--lang en`, `--lang zh`, or `--lang both` to choose the display language.

## Safety

- Do not paste or share tokens.
- The script does not print `access_token`, `refresh_token`, `id_token`, or authorization headers.
- The script does not modify Codex Desktop or WindowsApps files.
- This uses an internal endpoint that may change.

---

## 中文

一个轻量的 Codex skill，用来查询可用 Codex rate-limit reset credit 的到期时间。

由 `ebxk` 和 Codex 共同创作。

它调用 Codex Desktop 使用的同一个 reset-credit 接口：

```text
https://chatgpt.com/backend-api/wham/rate-limit-reset-credits
```

它会读取本机 Codex 登录态 `CODEX_HOME/auth.json` 或 `~/.codex/auth.json`，只在内存中使用 access token，并只输出脱敏后的可用次数和到期时间。

## 范围

这个项目故意保持很小：

- 查询 live reset credit 数量
- 查询可用 reset credit 的到期时间
- 不 patch Codex Desktop
- 不解析本地 session snapshot
- 不打印或保存 token

## 安装

把 skill 文件夹复制到你的 Codex skills 目录：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\codex-reset-expiry" "$env:USERPROFILE\.codex\skills\codex-reset-expiry"
```

重启 Codex 或新开一个 Codex 会话，然后这样问：

```text
用 $codex-reset-expiry 查我的 Codex reset 到期日。
```

也可以直接运行脚本：

```powershell
python .\skills\codex-reset-expiry\scripts\query_reset_credits.py
```

脚本默认输出中英双语。可以用 `--lang en`、`--lang zh` 或 `--lang both` 选择显示语言。

## 安全说明

- 不要粘贴或分享 token。
- 脚本不会打印 `access_token`、`refresh_token`、`id_token` 或 authorization headers。
- 脚本不会修改 Codex Desktop 或 WindowsApps 文件。
- 这个项目使用内部接口，未来可能会变化。

## License

MIT

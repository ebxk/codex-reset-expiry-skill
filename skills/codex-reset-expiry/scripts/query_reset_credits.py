#!/usr/bin/env python3
"""Query Codex reset-credit expiration dates without printing tokens."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


ENDPOINT = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query Codex rate-limit reset credit expiration dates."
    )
    parser.add_argument(
        "--auth",
        default=str(Path.home() / ".codex" / "auth.json"),
        help="Path to Codex auth.json. Defaults to ~/.codex/auth.json.",
    )
    parser.add_argument(
        "--endpoint",
        default=ENDPOINT,
        help="Reset-credit endpoint. Defaults to the Codex Desktop endpoint.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print sanitized JSON instead of a human-readable summary.",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh", "both"),
        default="both",
        help="Human-readable output language. Defaults to both.",
    )
    return parser.parse_args()


def load_credentials(auth_path: Path) -> tuple[str, str | None]:
    if not auth_path.exists():
        raise RuntimeError(f"Codex auth file was not found: {auth_path}")

    try:
        auth = json.loads(auth_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Codex auth file is not valid JSON: {auth_path}") from exc

    tokens = auth.get("tokens")
    if not isinstance(tokens, dict):
        raise RuntimeError("Codex auth file does not contain a tokens object.")

    access_token = tokens.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("Codex auth file does not contain an access token.")

    account_id = tokens.get("account_id")
    if account_id is not None and not isinstance(account_id, str):
        account_id = None

    return access_token, account_id


def fetch_reset_credits(endpoint: str, access_token: str, account_id: str | None) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "OpenAI-Beta": "codex-1",
        "originator": "Codex Desktop",
        "User-Agent": "codex-reset-expiry-skill/1.0",
    }
    if account_id:
        headers["ChatGPT-Account-ID"] = account_id

    request = urllib.request.Request(endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Reset-credit endpoint returned HTTP {exc.code}. Sign in again or try later."
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach reset-credit endpoint: {exc.reason}") from exc

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Reset-credit endpoint did not return JSON.") from exc

    if not isinstance(data, dict):
        raise RuntimeError("Reset-credit endpoint returned an unexpected response.")
    return data


def parse_iso(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def local_time_text(value: object) -> str | None:
    parsed = parse_iso(value)
    if parsed is None:
        return None
    local = parsed.astimezone()
    offset = local.strftime("%z")
    if len(offset) == 5:
        offset = f"{offset[:3]}:{offset[3:]}"
    return f"{local.strftime('%Y-%m-%d %H:%M')} UTC{offset}"


def sanitized_summary(data: dict) -> dict:
    credits = data.get("credits")
    if not isinstance(credits, list):
        credits = []

    sanitized_credits = []
    for credit in credits:
        if not isinstance(credit, dict):
            continue
        status = credit.get("status")
        expires_at = credit.get("expires_at")
        granted_at = credit.get("granted_at")
        row = {
            "status": status,
            "granted_at": granted_at,
            "granted_local": local_time_text(granted_at),
            "expires_at": expires_at,
            "expires_local": local_time_text(expires_at),
        }
        sanitized_credits.append(row)

    available = [row for row in sanitized_credits if row.get("status") == "available"]
    available.sort(key=lambda row: row.get("expires_at") or "")

    return {
        "available_count": data.get("available_count"),
        "available_credits": available,
        "all_credit_count": len(sanitized_credits),
    }


def print_human_en(summary: dict) -> None:
    print("Codex reset credits")
    print(f"Available count: {summary.get('available_count')}")

    available = summary.get("available_credits") or []
    if not available:
        print("No available reset credits with expiration dates were returned.")
        return

    for index, credit in enumerate(available, start=1):
        expires = credit.get("expires_local") or credit.get("expires_at") or "unknown"
        granted = credit.get("granted_local") or credit.get("granted_at") or "unknown"
        print(f"{index}. Expires: {expires} (granted: {granted})")


def print_human_zh(summary: dict) -> None:
    print("Codex reset 到期时间")
    print(f"可用次数: {summary.get('available_count')}")

    available = summary.get("available_credits") or []
    if not available:
        print("接口没有返回带到期时间的可用 reset credit。")
        return

    for index, credit in enumerate(available, start=1):
        expires = credit.get("expires_local") or credit.get("expires_at") or "未知"
        granted = credit.get("granted_local") or credit.get("granted_at") or "未知"
        print(f"{index}. 到期: {expires} (获得: {granted})")


def print_human(summary: dict, lang: str) -> None:
    if lang in ("en", "both"):
        print_human_en(summary)
    if lang == "both":
        print()
    if lang in ("zh", "both"):
        print_human_zh(summary)


def main() -> int:
    args = parse_args()
    try:
        access_token, account_id = load_credentials(Path(args.auth).expanduser())
        data = fetch_reset_credits(args.endpoint, access_token, account_id)
        summary = sanitized_summary(data)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_human(summary, args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

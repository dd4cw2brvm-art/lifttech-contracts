"""Daily customer totals: Supabase in production, JSON file locally."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Tuple

RIYADH_TZ = timezone(timedelta(hours=3), name="Asia/Riyadh")

ARABIC_WEEKDAYS = (
    "الاثنين",
    "الثلاثاء",
    "الأربعاء",
    "الخميس",
    "الجمعة",
    "السبت",
    "الأحد",
)

ARABIC_MONTHS = (
    "",
    "يناير",
    "فبراير",
    "مارس",
    "أبريل",
    "مايو",
    "يونيو",
    "يوليو",
    "أغسطس",
    "سبتمبر",
    "أكتوبر",
    "نوفمبر",
    "ديسمبر",
)

DEFAULT_STORE_PATH = Path(__file__).resolve().parent / "output" / "daily_customer_counts.json"


def riyadh_now() -> datetime:
    return datetime.now(RIYADH_TZ)


def format_arabic_date(value: datetime) -> str:
    local = value.astimezone(RIYADH_TZ)
    return (
        f"{ARABIC_WEEKDAYS[local.weekday()]}، "
        f"{local.day} {ARABIC_MONTHS[local.month]} {local.year}"
    )


def parse_updated_at(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(RIYADH_TZ)
    except (TypeError, ValueError):
        return None


def format_arabic_time(value: Any) -> str:
    parsed = value if isinstance(value, datetime) else parse_updated_at(value)
    if parsed is None:
        return "—"
    parsed = parsed.astimezone(RIYADH_TZ)
    period = "ص" if parsed.hour < 12 else "م"
    hour = parsed.hour % 12 or 12
    return f"{hour}:{parsed.minute:02d} {period}"


def get_operator_name() -> str:
    return os.getenv("DAILY_CONTACTS_OPERATOR", "المدير التنفيذي").strip()


@lru_cache(maxsize=1)
def _supabase_client() -> Any:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    if not url or not key:
        return None
    from supabase import create_client

    return create_client(url, key)


def _load_store(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_store(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _get_from_supabase(record_date: str) -> Tuple[Optional[dict], Optional[str]]:
    client = _supabase_client()
    if client is None:
        return None, None
    try:
        response = (
            client.table("daily_contact_counts")
            .select(
                "record_date,maintenance_count,installation_count,"
                "updated_at,entered_by"
            )
            .eq("record_date", record_date)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return (rows[0] if rows else None), None
    except Exception as exc:
        return None, str(exc)


def _save_to_supabase(payload: dict) -> Tuple[Optional[dict], Optional[str]]:
    client = _supabase_client()
    if client is None:
        return None, None
    try:
        response = (
            client.table("daily_contact_counts")
            .upsert(payload, on_conflict="record_date")
            .execute()
        )
        rows = response.data or []
        return (rows[0] if rows else payload), None
    except Exception as exc:
        return None, str(exc)


def get_daily_contact_record(
    record_date: str,
    store_path: Path = DEFAULT_STORE_PATH,
) -> Tuple[Optional[dict], Optional[str]]:
    record, error = _get_from_supabase(record_date)
    if error or record is not None or _supabase_client() is not None:
        return record, error

    record = _load_store(store_path).get(record_date)
    return (record, None) if record else (None, None)


def save_daily_contact_record(
    *,
    record_date: str,
    maintenance_count: int,
    installation_count: int,
    entered_by: str,
    updated_at: datetime,
    store_path: Path = DEFAULT_STORE_PATH,
) -> Tuple[Optional[dict], Optional[str]]:
    maintenance_count = int(maintenance_count)
    installation_count = int(installation_count)
    if maintenance_count < 0 or installation_count < 0:
        return None, "يجب ألا تكون الأرقام سالبة."
    if not entered_by.strip():
        return None, "تعذّر تحديد اسم المستخدم."

    payload = {
        "record_date": record_date,
        "maintenance_count": maintenance_count,
        "installation_count": installation_count,
        "updated_at": updated_at.astimezone(RIYADH_TZ).isoformat(),
        "entered_by": entered_by.strip(),
    }

    saved, error = _save_to_supabase(payload)
    if error:
        return None, error
    if saved is not None:
        return saved, None

    store = _load_store(store_path)
    store[record_date] = payload
    try:
        _write_store(store_path, store)
    except OSError as exc:
        return None, str(exc)
    return payload, None

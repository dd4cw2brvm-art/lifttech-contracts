# -*- coding: utf-8 -*-
"""Security helpers for Hotfix V18.1 — pure functions (testable, no Streamlit)."""

from __future__ import annotations

from datetime import date, timedelta

ROLE_DENY = "deny"
AUTH_SESSION_EPOCH = "v18.1-hotfix"
LEGACY_QUERY_AUTH_KEYS = ("u", "r", "n", "cc", "tk", "pg")
PWD_MIN_LENGTH = 10
CLIENT_PORTAL_ENABLED = False

VALID_STAFF_ROLES = frozenset({"admin", "manager", "tech", "client"})
PWD_FORBIDDEN = frozenset(
    {"12345", "123456", "password", "lifttech", "admin", "00000", "111111"}
)


def normalize_role(role: str | None, valid_roles: set[str] | None = None) -> str:
    allowed = valid_roles or VALID_STAFF_ROLES
    if not role or role not in allowed:
        return ROLE_DENY
    return role


def is_client_login_blocked(role: str) -> bool:
    return not CLIENT_PORTAL_ENABLED and role == "client"


def is_forbidden_password(pwd: str, username: str = "") -> bool:
    if not pwd:
        return True
    if len(pwd) < PWD_MIN_LENGTH:
        return True
    if pwd.lower() in PWD_FORBIDDEN:
        return True
    if username and pwd.lower() == username.lower():
        return True
    return False


def has_legacy_auth_query_params(params: dict) -> bool:
    return any(params.get(k) for k in LEGACY_QUERY_AUTH_KEYS)


def strip_legacy_auth_query_params(params: dict) -> dict:
    return {k: v for k, v in params.items() if k not in LEGACY_QUERY_AUTH_KEYS}


def scope_records_by_contract_ids(
    records: list,
    allowed_ids: set[str],
    contract_id_field: str = "contract_id",
) -> list:
    if not allowed_ids:
        return []
    return [
        r
        for r in records
        if str(r.get(contract_id_field, "")) in allowed_ids
    ]


def client_contract_ids(contracts: list, contract_no: str) -> set[str]:
    if not contract_no:
        return set()
    return {
        str(c.get("id"))
        for c in contracts
        if str(c.get("contract_no", "")) == contract_no
    }


def validate_work_order(
    title: str,
    contract_id,
    technician: str,
    scheduled_date,
    status: str,
) -> list[str]:
    errors: list[str] = []
    if not (title or "").strip():
        errors.append("عنوان أمر العمل مطلوب")
    if not contract_id:
        errors.append("يجب اختيار عقد مرتبط")
    if not technician or technician == "-- غير مكلف --":
        errors.append("يجب تعيين فني مسؤول")
    if scheduled_date is None:
        errors.append("تاريخ الجدولة مطلوب")
    else:
        sched = scheduled_date
        if isinstance(sched, str):
            try:
                sched = date.fromisoformat(sched[:10])
            except ValueError:
                errors.append("تاريخ الجدولة غير صالح")
                sched = None
        if sched is not None and sched < date.today() - timedelta(days=1):
            errors.append("تاريخ الجدولة لا يمكن أن يكون في الماضي البعيد")
    if status not in {"pending", "assigned"}:
        errors.append("حالة أمر العمل الابتدائية غير صالحة")
    return errors


def check_duplicate_work_order(
    rows: list[dict],
    contract_id,
    title: str,
    technician: str,
    scheduled_date,
) -> bool:
    if not contract_id or not technician:
        return False
    sched = str(scheduled_date)
    title_n = (title or "").strip().lower()
    for row in rows:
        if str(row.get("contract_id")) != str(contract_id):
            continue
        if (row.get("technician") or "") != technician:
            continue
        if str(row.get("scheduled_date", ""))[:10] != sched[:10]:
            continue
        if row.get("status") in ("cancelled", "completed"):
            continue
        if (row.get("title") or "").strip().lower() == title_n:
            return True
    return False


def get_ultramsg_credentials(secrets: dict) -> tuple[str | None, str | None]:
    instance = (secrets or {}).get("ULTRAMSG_INSTANCE")
    token = (secrets or {}).get("ULTRAMSG_TOKEN")
    if not instance or not token:
        return None, None
    return str(instance).strip(), str(token).strip()

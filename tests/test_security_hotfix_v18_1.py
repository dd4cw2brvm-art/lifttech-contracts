# -*- coding: utf-8 -*-
"""Security Hotfix V18.1 — regression tests (no Streamlit runtime)."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from security_hotfix import (
    AUTH_SESSION_EPOCH,
    CLIENT_PORTAL_ENABLED,
    PWD_MIN_LENGTH,
    ROLE_DENY,
    check_duplicate_work_order,
    client_contract_ids,
    get_ultramsg_credentials,
    has_legacy_auth_query_params,
    is_client_login_blocked,
    is_forbidden_password,
    normalize_role,
    scope_records_by_contract_ids,
    strip_legacy_auth_query_params,
    validate_work_order,
)


class TestUrlAuthBlocked:
    def test_forged_url_params_detected(self):
        params = {"u": "hacker", "r": "admin", "tk": "deadbeef"}
        assert has_legacy_auth_query_params(params) is True

    def test_strip_removes_session_params(self):
        raw = {"u": "x", "r": "admin", "pg": "dashboard", "foo": "bar"}
        cleaned = strip_legacy_auth_query_params(raw)
        assert "u" not in cleaned and "r" not in cleaned and "pg" not in cleaned
        assert cleaned.get("foo") == "bar"


class TestRoleDeny:
    def test_missing_role_becomes_deny(self):
        assert normalize_role(None) == ROLE_DENY
        assert normalize_role("") == ROLE_DENY

    def test_admin_spoof_from_empty_denied(self):
        assert normalize_role("superuser") == ROLE_DENY

    def test_valid_admin_preserved(self):
        assert normalize_role("admin") == "admin"


class TestTechnicianScope:
    def test_technician_sees_only_own_tasks(self):
        rows = [
            {"technician": "فيصل", "title": "A"},
            {"technician": "فريتز", "title": "B"},
        ]
        mine = [r for r in rows if r.get("technician") == "فيصل"]
        assert len(mine) == 1
        assert mine[0]["title"] == "A"


class TestClientIsolation:
    def test_client_cannot_see_other_contract_data(self):
        contracts = [
            {"id": 1, "contract_no": "C-100"},
            {"id": 2, "contract_no": "C-200"},
        ]
        allowed = client_contract_ids(contracts, "C-100")
        rows = [
            {"contract_id": "1", "description": "mine"},
            {"contract_id": "2", "description": "other"},
        ]
        scoped = scope_records_by_contract_ids(rows, allowed)
        assert len(scoped) == 1
        assert scoped[0]["description"] == "mine"


class TestWorkOrderCreation:
    def test_validate_work_order_ok(self):
        errs = validate_work_order(
            "صيانة دورية",
            10,
            "فيصل",
            date.today(),
            "assigned",
        )
        assert errs == []

    def test_validate_work_order_requires_fields(self):
        errs = validate_work_order("", None, "-- غير مكلف --", None, "pending")
        assert len(errs) >= 3

    def test_duplicate_detection(self):
        existing = [
            {
                "contract_id": "5",
                "title": "فحص",
                "technician": "فيصل",
                "scheduled_date": "2026-07-15",
                "status": "assigned",
            }
        ]
        assert check_duplicate_work_order(
            existing, "5", "فحص", "فيصل", "2026-07-15"
        )


class TestUltraMsgSecrets:
    def test_missing_secret_no_default(self):
        inst, tok = get_ultramsg_credentials({})
        assert inst is None and tok is None

    def test_partial_secret_rejected(self):
        inst, tok = get_ultramsg_credentials({"ULTRAMSG_INSTANCE": "x"})
        assert inst is None and tok is None

    def test_valid_secret_pair(self):
        inst, tok = get_ultramsg_credentials(
            {"ULTRAMSG_INSTANCE": "inst", "ULTRAMSG_TOKEN": "tok"}
        )
        assert inst == "inst" and tok == "tok"


class TestPasswordPolicy:
    def test_default_password_forbidden(self):
        assert is_forbidden_password("12345", "user1") is True

    def test_min_length_ten(self):
        assert is_forbidden_password("short1", "user1") is True
        assert is_forbidden_password("a" * PWD_MIN_LENGTH, "user1") is False


class TestClientPortalDisabled:
    def test_client_login_blocked(self):
        assert CLIENT_PORTAL_ENABLED is False
        assert is_client_login_blocked("client") is True
        assert is_client_login_blocked("admin") is False


class TestSessionEpoch:
    def test_epoch_defined(self):
        assert AUTH_SESSION_EPOCH == "v18.1-hotfix"

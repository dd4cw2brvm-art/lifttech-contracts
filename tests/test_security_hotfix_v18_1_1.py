# -*- coding: utf-8 -*-
"""Security Hotfix V18.1.1 — password policy and technician isolation tests."""

from __future__ import annotations

from security_hotfix import (
    PWD_MIN_LENGTH,
    account_requires_admin_reset,
    is_forbidden_password,
    scope_contracts_for_technician,
    scope_records_for_technician,
    technician_contract_ids,
    validate_new_password,
)


class TestPasswordPolicyAllPaths:
    def test_validate_rejects_default_password(self):
        assert validate_new_password("12345", "faisal")

    def test_validate_rejects_short_password(self):
        errs = validate_new_password("abc", "faisal")
        assert any(str(PWD_MIN_LENGTH) in e for e in errs)

    def test_validate_rejects_username_as_password(self):
        errs = validate_new_password("faisal", "faisal")
        assert errs

    def test_validate_accepts_strong_password(self):
        assert validate_new_password("SecurePass99", "faisal") == []

    def test_set_db_password_gate_blocks_weak(self):
        assert is_forbidden_password("12345", "faisal") is True
        assert is_forbidden_password("SecurePass99", "faisal") is False

    def test_account_requires_admin_reset_for_stored_default(self):
        assert account_requires_admin_reset("12345", "faisal") is True
        assert account_requires_admin_reset("SecurePass99", "faisal") is False


class TestBlockedDefaultAccounts:
    def test_weak_stored_password_blocks_login_path(self):
        stored = "password"
        assert account_requires_admin_reset(stored, "junaid") is True

    def test_admin_reset_must_use_policy(self):
        admin_reset = "123456"
        assert validate_new_password(admin_reset, "junaid")


class TestTechnicianDashboardCalendarIsolation:
    def test_technician_sees_only_own_work_orders(self):
        rows = [
            {"technician": "فيصل", "contract_id": "1", "title": "A"},
            {"technician": "فريتز", "contract_id": "2", "title": "B"},
        ]
        scoped = scope_records_for_technician(rows, "فيصل")
        assert len(scoped) == 1
        assert scoped[0]["contract_id"] == "1"

    def test_technician_contract_ids_from_tasks_only(self):
        wo = [{"technician": "فيصل", "contract_id": 10}]
        fr = [{"technician": "فريتز", "contract_id": 20}]
        ml = [{"technician": "فيصل", "contract_id": 11}]
        ids = technician_contract_ids(wo, fr, ml, "فيصل")
        assert ids == {"10", "11"}

    def test_technician_dashboard_contracts_scoped(self):
        contracts = [
            {"id": 10, "contract_no": "C-10"},
            {"id": 20, "contract_no": "C-20"},
        ]
        scoped = scope_contracts_for_technician(contracts, {"10"})
        assert len(scoped) == 1
        assert scoped[0]["contract_no"] == "C-10"

    def test_calendar_events_isolated_per_technician(self):
        maintenance = [
            {"technician": "فيصل", "log_date": "2026-07-10", "contract_id": 1},
            {"technician": "فريتز", "log_date": "2026-07-10", "contract_id": 2},
        ]
        scoped = scope_records_for_technician(maintenance, "فيصل")
        assert len(scoped) == 1


class TestSessionNotCreatedOnFailedPasswordSave:
    def test_weak_password_fails_before_persist(self):
        """محاكاة: set_db_password يرفض قبل الكتابة إذا كانت السياسة تفشل."""
        new_pwd = "12345"
        can_save = not is_forbidden_password(new_pwd, "faisal")
        assert can_save is False

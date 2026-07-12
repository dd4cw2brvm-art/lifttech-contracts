from datetime import datetime, timezone
from pathlib import Path
import json

from daily_contacts_store import (
    RIYADH_TZ,
    format_arabic_date,
    format_arabic_date_from_iso,
    format_arabic_time,
    get_daily_contact_record,
    save_daily_contact_record,
)


def test_format_arabic_date_from_iso():
    assert format_arabic_date_from_iso("2026-07-11") == "السبت، 11 يوليو 2026"


def test_formats_riyadh_date_and_time_in_arabic():
    value = datetime(2026, 7, 11, 15, 30, tzinfo=timezone.utc)

    assert format_arabic_date(value) == "السبت، 11 يوليو 2026"
    assert format_arabic_time(value) == "6:30 م"


def test_save_and_update_single_record_per_date(tmp_path: Path):
    store_path = tmp_path / "daily_customer_counts.json"
    updated_at = datetime(2026, 7, 11, 18, 30, tzinfo=RIYADH_TZ)

    saved, error = save_daily_contact_record(
        record_date="2026-07-11",
        maintenance_count=12,
        installation_count=7,
        entered_by="أحمد",
        updated_at=updated_at,
        store_path=store_path,
    )
    assert error is None
    assert saved["maintenance_count"] == 12

    updated, error = save_daily_contact_record(
        record_date="2026-07-11",
        maintenance_count=15,
        installation_count=7,
        entered_by="أحمد",
        updated_at=updated_at,
        store_path=store_path,
    )
    assert error is None
    assert updated["maintenance_count"] == 15

    record, _ = get_daily_contact_record("2026-07-11", store_path=store_path)
    assert record["maintenance_count"] == 15
    assert len(json.loads(store_path.read_text(encoding="utf-8"))) == 1


def test_save_rejects_negative_values(tmp_path: Path):
    saved, error = save_daily_contact_record(
        record_date="2026-07-11",
        maintenance_count=-1,
        installation_count=0,
        entered_by="أحمد",
        updated_at=datetime.now(RIYADH_TZ),
        store_path=tmp_path / "daily_customer_counts.json",
    )

    assert saved is None
    assert error == "يجب ألا تكون الأرقام سالبة."

"""
لوحة مستقلة: العملاء المتواصلون اليوم.

تشغيل:
  streamlit run customers_today_dashboard.py
"""

from __future__ import annotations

import html
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from daily_contacts_store import (
    format_arabic_date,
    format_arabic_time,
    get_daily_contact_record,
    get_operator_name,
    riyadh_now,
    save_daily_contact_record,
)

load_dotenv()


def resolve_operator_name() -> str:
    try:
        value = st.secrets.get("DAILY_CONTACTS_OPERATOR")
        if value:
            return str(value).strip()
    except Exception:
        pass
    return get_operator_name()


def resolve_supabase_env() -> None:
    try:
        if "SUPABASE_URL" in st.secrets and not os.getenv("SUPABASE_URL"):
            os.environ["SUPABASE_URL"] = str(st.secrets["SUPABASE_URL"])
        if "SUPABASE_KEY" in st.secrets and not os.getenv("SUPABASE_KEY"):
            os.environ["SUPABASE_KEY"] = str(st.secrets["SUPABASE_KEY"])
    except Exception:
        pass


resolve_supabase_env()

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "lifttech-logo.png"

st.set_page_config(
    page_title="لفتك — العملاء المتواصلون اليوم",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "📞",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"], [data-testid="stToolbar"],
[data-testid="stDeployButton"], [data-testid="collapsedControl"] {
    display: none !important;
}
html, body, [data-testid="stApp"] {
    background: #FFFFFF !important;
    direction: rtl;
    font-family: "Segoe UI", Tahoma, Arial, sans-serif;
}
[data-testid="stMainBlockContainer"], .main .block-container {
    max-width: 560px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
}
.brand-logo {
    text-align: center;
    margin: 0 auto 18px;
    max-width: 220px;
}
.brand-logo img {
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}
.daily-contacts-heading {
    text-align: center;
    margin: 8px auto 22px;
    color: #111111;
    font-size: clamp(1.35rem, 4vw, 1.85rem);
    font-weight: 900;
}
.daily-card-title {
    color: #111111;
    font-size: 1rem;
    font-weight: 800;
    text-align: right;
    margin-bottom: 14px;
}
.daily-saved-number {
    min-height: 92px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CB0A04;
    background: #FFFFFF;
    border: 1.5px solid #D1D5DB;
    border-radius: 12px;
    font-size: clamp(2.8rem, 10vw, 4rem);
    font-weight: 900;
    font-variant-numeric: tabular-nums;
}
.daily-date, .daily-status {
    text-align: center;
    color: #111111;
    font-weight: 700;
    margin: 14px 0;
}
.daily-status {
    color: #4B5563;
    font-size: .84rem;
    margin-top: 12px;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1.5px solid #111111 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(0,0,0,.06) !important;
}
[data-testid="stNumberInput"] input {
    min-height: 92px !important;
    color: #CB0A04 !important;
    background: #FFFFFF !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 12px !important;
    font-size: clamp(2.8rem, 10vw, 4rem) !important;
    font-weight: 900 !important;
    text-align: center !important;
    font-variant-numeric: tabular-nums !important;
}
[data-testid="stNumberInput"] button { display: none !important; }
.stButton > button,
.stFormSubmitButton > button {
    width: 100% !important;
    min-height: 48px !important;
    background: #CB0A04 !important;
    color: #FFFFFF !important;
    border: 1px solid #CB0A04 !important;
    border-radius: 10px !important;
    box-shadow: 0 3px 9px rgba(203,10,4,.22) !important;
    font-size: .95rem !important;
    font-weight: 800 !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #A80803 !important;
    border-color: #A80803 !important;
}
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        padding-left: 14px !important;
        padding-right: 14px !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }
    [data-testid="column"] {
        min-width: 100% !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

if LOGO_PATH.exists():
    logo_col_left, logo_col_center, logo_col_right = st.columns([1, 1.2, 1])
    with logo_col_center:
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    '<h1 class="daily-contacts-heading">العملاء المتواصلون اليوم</h1>',
    unsafe_allow_html=True,
)


def render_cards(is_editing: bool, maintenance: int, installation: int, record_date: str):
    maintenance_col, installation_col = st.columns(2, gap="medium")
    with maintenance_col:
        with st.container(border=True):
            st.markdown(
                '<div class="daily-card-title">🛠️ عملاء الصيانة</div>',
                unsafe_allow_html=True,
            )
            if is_editing:
                maintenance = st.number_input(
                    "إجمالي عملاء الصيانة",
                    min_value=0,
                    value=maintenance,
                    step=1,
                    format="%d",
                    key=f"daily_maintenance_{record_date}",
                    label_visibility="collapsed",
                )
            else:
                st.markdown(
                    f'<div class="daily-saved-number">{maintenance}</div>',
                    unsafe_allow_html=True,
                )
    with installation_col:
        with st.container(border=True):
            st.markdown(
                '<div class="daily-card-title">🛗 عملاء التركيبات</div>',
                unsafe_allow_html=True,
            )
            if is_editing:
                installation = st.number_input(
                    "إجمالي عملاء التركيبات",
                    min_value=0,
                    value=installation,
                    step=1,
                    format="%d",
                    key=f"daily_installation_{record_date}",
                    label_visibility="collapsed",
                )
            else:
                st.markdown(
                    f'<div class="daily-saved-number">{installation}</div>',
                    unsafe_allow_html=True,
                )
    return int(maintenance), int(installation)


now = riyadh_now()
record_date = now.date().isoformat()
record, load_error = get_daily_contact_record(record_date)

if load_error:
    if "daily_contact_counts" in load_error or "PGRST205" in load_error:
        st.error("تعذّر فتح سجل أرقام اليوم. نفّذ daily_contact_counts.sql في Supabase.")
    else:
        st.error("تعذّر تحميل أرقام اليوم.")
    st.stop()

edit_key = f"daily_contacts_editing_{record_date}"
if edit_key not in st.session_state:
    st.session_state[edit_key] = record is None
editing = bool(st.session_state[edit_key])

maintenance_value = int((record or {}).get("maintenance_count") or 0)
installation_value = int((record or {}).get("installation_count") or 0)

if editing:
    with st.form(f"daily_contacts_form_{record_date}", clear_on_submit=False):
        maintenance_value, installation_value = render_cards(
            True, maintenance_value, installation_value, record_date
        )
        st.markdown(
            f'<div class="daily-date">{format_arabic_date(now)}</div>',
            unsafe_allow_html=True,
        )
        button_label = "حفظ التعديلات" if record else "حفظ أرقام اليوم"
        submitted = st.form_submit_button(button_label, use_container_width=True)

    if submitted:
        saved, save_error = save_daily_contact_record(
            record_date=record_date,
            maintenance_count=maintenance_value,
            installation_count=installation_value,
            entered_by=resolve_operator_name(),
            updated_at=riyadh_now(),
        )
        if save_error:
            st.error("تعذّر حفظ أرقام اليوم. حاول مرة أخرى.")
        else:
            record = saved
            st.session_state[edit_key] = False
            st.rerun()
else:
    render_cards(False, maintenance_value, installation_value, record_date)
    st.markdown(
        f'<div class="daily-date">{format_arabic_date(now)}</div>',
        unsafe_allow_html=True,
    )
    if st.button("تعديل أرقام اليوم", use_container_width=True):
        st.session_state[edit_key] = True
        st.rerun()

if record:
    updated_time = format_arabic_time(record.get("updated_at"))
    entered_by = html.escape(str(record.get("entered_by") or "—"))
    status = f"آخر تحديث: {updated_time} — المُدخل: {entered_by}"
else:
    status = "لم يتم حفظ أرقام اليوم بعد"

st.markdown(
    f'<div class="daily-status">{status}</div>',
    unsafe_allow_html=True,
)

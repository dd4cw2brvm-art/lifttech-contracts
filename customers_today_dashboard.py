"""
تقرير يومي: إجمالي الاتصالات الفعلية لحملات Google Ads — لفتك للمصاعد.

تشغيل:
  streamlit run customers_today_dashboard.py
"""

from __future__ import annotations

import html
import importlib.util
import os
import sys
from datetime import timedelta
from pathlib import Path

import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _load_store_module():
    store_path = Path(__file__).resolve().parent / "daily_contacts_store.py"
    if not store_path.exists():
        raise ImportError(f"Missing store module: {store_path}")

    module_name = "daily_contacts_store"
    spec = importlib.util.spec_from_file_location(module_name, store_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load store module from {store_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_store = _load_store_module()
format_arabic_date_from_iso = _store.format_arabic_date_from_iso
format_arabic_time = _store.format_arabic_time
get_daily_contact_record = _store.get_daily_contact_record
get_operator_name = _store.get_operator_name
riyadh_now = _store.riyadh_now
save_daily_contact_record = _store.save_daily_contact_record

LOGO_PATH = Path(__file__).resolve().parent / "assets" / "lifttech-logo.png"

st.set_page_config(
    page_title="لفتك — تقرير الاتصالات اليومية | Google Ads",
    page_icon="📞",
    layout="centered",
    initial_sidebar_state="collapsed",
)


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

st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stSidebar"], [data-testid="stToolbar"],
[data-testid="stDeployButton"], [data-testid="collapsedControl"] {
    display: none !important;
}
html, body, [data-testid="stApp"] {
    background: #F4F5F7 !important;
    direction: rtl;
    font-family: "Cairo", "Segoe UI", Tahoma, Arial, sans-serif;
}
[data-testid="stMainBlockContainer"], .main .block-container {
    max-width: 720px !important;
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}
.report-shell {
    background: #FFFFFF;
    border: 1px solid #D9DDE3;
    border-top: 4px solid #CB0A04;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(17,17,17,.06);
    overflow: hidden;
}
.report-header {
    padding: 22px 22px 16px;
    border-bottom: 1px solid #ECEFF3;
    background: linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%);
}
.report-badge {
    display: inline-block;
    background: #111111;
    color: #FFFFFF;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .4px;
    padding: 5px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}
.report-title {
    margin: 0;
    color: #111111;
    font-size: clamp(1.2rem, 3.5vw, 1.55rem);
    font-weight: 900;
    line-height: 1.45;
}
.report-subtitle {
    margin: 8px 0 0;
    color: #5B6470;
    font-size: .88rem;
    font-weight: 600;
    line-height: 1.7;
}
.report-toolbar {
    margin-top: 16px;
    padding: 12px 14px;
    background: #F8F9FB;
    border: 1px solid #E7EBF0;
    border-radius: 12px;
}
.report-body {
    padding: 18px 22px 22px;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
}
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #D9DDE3;
    border-radius: 14px;
    padding: 16px 14px 14px;
    min-height: 170px;
}
.kpi-label {
    color: #111111;
    font-size: .92rem;
    font-weight: 800;
    margin-bottom: 4px;
}
.kpi-caption {
    color: #6B7280;
    font-size: .72rem;
    font-weight: 600;
    margin-bottom: 14px;
}
.kpi-value {
    min-height: 88px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CB0A04;
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 12px;
    font-size: clamp(2.5rem, 8vw, 3.4rem);
    font-weight: 900;
    font-variant-numeric: tabular-nums;
}
.total-bar {
    margin-top: 14px;
    padding: 12px 16px;
    border-radius: 12px;
    background: #111111;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    font-weight: 800;
}
.total-bar span {
    font-size: .84rem;
    opacity: .88;
}
.total-bar strong {
    font-size: 1.35rem;
    color: #FFFFFF;
    font-variant-numeric: tabular-nums;
}
.report-date {
    text-align: center;
    color: #111111;
    font-weight: 800;
    margin: 16px 0 10px;
    font-size: .95rem;
}
.report-status {
    text-align: center;
    color: #5B6470;
    font-size: .8rem;
    font-weight: 700;
    margin-top: 10px;
}
.report-footnote {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px dashed #D9DDE3;
    color: #7A828C;
    font-size: .72rem;
    line-height: 1.8;
    text-align: center;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
[data-testid="stNumberInput"] input {
    min-height: 88px !important;
    color: #CB0A04 !important;
    background: #FFFFFF !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    font-size: clamp(2.5rem, 8vw, 3.4rem) !important;
    font-weight: 900 !important;
    text-align: center !important;
    font-variant-numeric: tabular-nums !important;
}
[data-testid="stNumberInput"] button { display: none !important; }
[data-testid="stDateInput"] label {
    font-weight: 800 !important;
    color: #111111 !important;
    font-size: .82rem !important;
}
[data-testid="stDateInput"] input {
    font-weight: 700 !important;
}
.stButton > button,
.stFormSubmitButton > button {
    width: 100% !important;
    min-height: 48px !important;
    background: #CB0A04 !important;
    color: #FFFFFF !important;
    border: 1px solid #CB0A04 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(203,10,4,.18) !important;
    font-size: .92rem !important;
    font-weight: 800 !important;
}
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #111111 !important;
    border: 1px solid #D1D5DB !important;
    box-shadow: none !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #A80803 !important;
    border-color: #A80803 !important;
}
@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"],
    .main .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    .report-header, .report-body {
        padding-left: 14px !important;
        padding-right: 14px !important;
    }
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

today = riyadh_now().date()
yesterday = today - timedelta(days=1)

if "daily_contacts_selected_date" not in st.session_state:
    st.session_state["daily_contacts_selected_date"] = today

if st.session_state.pop("goto_yesterday", False):
    st.session_state["daily_contacts_selected_date"] = yesterday

st.markdown('<div class="report-shell"><div class="report-header">', unsafe_allow_html=True)

if LOGO_PATH.exists():
    logo_col_left, logo_col_center, logo_col_right = st.columns([1, 1.1, 1])
    with logo_col_center:
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    """
<div class="report-badge">Google Ads Performance Report</div>
<h1 class="report-title">تقرير الاتصالات اليومية — حملات مصاعد لفتك</h1>
<p class="report-subtitle">
إجمالي العملاء الفعليين الذين تواصلوا عبر الحملات، موزّعين على
<strong>الصيانة</strong> و<strong>التركيبات</strong> — بتوقيت الرياض.
</p>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="report-toolbar">', unsafe_allow_html=True)
date_col, yesterday_col, today_col = st.columns([2.2, 1, 1], gap="small")
with yesterday_col:
    st.markdown("<div style='height:1.55rem'></div>", unsafe_allow_html=True)
    if st.button("أمس", use_container_width=True):
        st.session_state["goto_yesterday"] = True
        st.rerun()
with today_col:
    st.markdown("<div style='height:1.55rem'></div>", unsafe_allow_html=True)
    if st.button("اليوم", use_container_width=True):
        st.session_state["daily_contacts_selected_date"] = today
        st.rerun()
with date_col:
    selected_date = st.date_input(
        "تاريخ التقرير",
        max_value=today,
        format="DD/MM/YYYY",
        key="daily_contacts_selected_date",
    )
st.markdown("</div></div><div class='report-body'>", unsafe_allow_html=True)

record_date = selected_date.isoformat()
is_today = selected_date == today
display_date = format_arabic_date_from_iso(record_date)
view_mode = "عرض تقرير سابق" if not is_today else "تقرير اليوم الحالي"

st.markdown(
    f'<div class="report-date">{html.escape(display_date)} — {html.escape(view_mode)}</div>',
    unsafe_allow_html=True,
)


def render_cards(is_editing: bool, maintenance: int, installation: int, record_date: str):
    maintenance_col, installation_col = st.columns(2, gap="medium")
    with maintenance_col:
        st.markdown(
            """
            <div class="kpi-card">
              <div class="kpi-label">🛠️ عملاء الصيانة</div>
              <div class="kpi-caption">إجمالي الاتصالات الفعلية — حملة الصيانة</div>
            """,
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
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="kpi-value">{maintenance}</div></div>',
                unsafe_allow_html=True,
            )
    with installation_col:
        st.markdown(
            """
            <div class="kpi-card">
              <div class="kpi-label">🛗 عملاء التركيبات</div>
              <div class="kpi-caption">إجمالي الاتصالات الفعلية — حملة التركيبات</div>
            """,
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
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="kpi-value">{installation}</div></div>',
                unsafe_allow_html=True,
            )
    return int(maintenance), int(installation)


record, load_error = get_daily_contact_record(record_date)

if load_error:
    st.markdown("</div></div>", unsafe_allow_html=True)
    if "daily_contact_counts" in load_error or "PGRST205" in load_error:
        st.error("تعذّر فتح سجل التقرير. نفّذ daily_contact_counts.sql في Supabase.")
    else:
        st.error("تعذّر تحميل بيانات التقرير.")
    st.stop()

edit_key = f"daily_contacts_editing_{record_date}"
if edit_key not in st.session_state:
    st.session_state[edit_key] = record is None
editing = bool(st.session_state[edit_key])

maintenance_value = int((record or {}).get("maintenance_count") or 0)
installation_value = int((record or {}).get("installation_count") or 0)
total_value = maintenance_value + installation_value

if editing:
    with st.form(f"daily_contacts_form_{record_date}", clear_on_submit=False):
        maintenance_value, installation_value = render_cards(
            True, maintenance_value, installation_value, record_date
        )
        total_value = maintenance_value + installation_value
        st.markdown(
            f"""
            <div class="total-bar">
              <span>إجمالي الاتصالات الفعلية لليوم</span>
              <strong>{total_value}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
        button_label = "اعتماد التعديلات" if record else "اعتماد التقرير اليومي"
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
            st.error("تعذّر اعتماد التقرير. حاول مرة أخرى.")
        else:
            record = saved
            st.session_state[edit_key] = False
            st.rerun()
else:
    render_cards(False, maintenance_value, installation_value, record_date)
    st.markdown(
        f"""
        <div class="total-bar">
          <span>إجمالي الاتصالات الفعلية لليوم</span>
          <strong>{total_value}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "تعديل التقرير" if is_today else "تعديل تقرير هذا اليوم",
        use_container_width=True,
    ):
        st.session_state[edit_key] = True
        st.rerun()

if record:
    updated_time = format_arabic_time(record.get("updated_at"))
    entered_by = html.escape(str(record.get("entered_by") or "—"))
    status = f"آخر اعتماد: {updated_time} — المُدخل: {entered_by}"
else:
    status = (
        "لم يتم اعتماد تقرير اليوم بعد"
        if is_today
        else "لا يوجد تقرير معتمد لهذا التاريخ"
    )

st.markdown(
    f"""
    <div class="report-status">{status}</div>
    <div class="report-footnote">
      تعريف العميل الفعلي: رقم جوال مختلف لديه طلب واضح، ويُحسب مرة واحدة يومياً.
      <br>
      هذا التقرير مخصص لمتابعة أداء حملات Google Ads — مصاعد لفتك.
    </div>
    </div></div>
    """,
    unsafe_allow_html=True,
)

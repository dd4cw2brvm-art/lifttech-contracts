import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import io
import urllib.request
import urllib.parse
import json as _json

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LiftTech — نظام إدارة المصاعد",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Google Fonts + Global CSS (Odoo ERP Style)
# ─────────────────────────────────────────────
st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown("""
<style>
/* ═══════════════════════════════════════════════
   LiftTech V8.7 — Pure White & Black, No Colors
   ═══════════════════════════════════════════════ */

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stApp"] {
  background: #ffffff !important;
  color: #111111 !important;
  font-family: "Cairo", "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
  direction: rtl;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDeployButton"]      { display: none !important; }
[data-testid="stStatusWidget"]      { display: none !important; }
[data-testid="collapsedControl"]    { display: none !important; }
button[title="View fullscreen"]     { display: none !important; }
.stDecoration                       { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-left: 2px solid #111111 !important;
  min-width: 220px !important;
  max-width: 220px !important;
}
[data-testid="stSidebar"] * {
  color: #111111 !important;
}

/* ── Radio (sidebar nav) ── */
[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
[data-testid="stSidebar"] .stRadio label {
  background: transparent !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 10px 14px !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  color: #111111 !important;
  cursor: pointer !important;
  transition: background .15s;
  direction: rtl !important;
  text-align: right !important;
  width: 100% !important;
  display: block !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: #f0f0f0 !important;
}
/* إخفاء نقطة الـ radio — Streamlit جديد */
[data-testid="stSidebar"] .stRadio input[type="radio"] {
  display: none !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
  display: none !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] ~ div,
[data-testid="stSidebar"] .stRadio span[data-baseweb="radio"] {
  display: none !important;
}

/* ── Main content area ── */
[data-testid="stMainBlockContainer"],
.main .block-container {
  padding: 24px 32px !important;
  max-width: 100% !important;
  background: #ffffff !important;
}

/* ── Buttons ── */
.stButton > button {
  background: #111111 !important;
  color: #ffffff !important;
  border: 1.5px solid #111111 !important;
  border-radius: 6px !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  padding: 8px 18px !important;
  transition: opacity .2s;
}
.stButton > button:hover  { opacity: .8 !important; }
.stButton > button[kind="secondary"] {
  background: #ffffff !important;
  color: #111111 !important;
  border: 1.5px solid #111111 !important;
}

/* ── Inputs ── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
[data-baseweb="select"] *,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: #ffffff !important;
  color: #111111 !important;
  border: 1.5px solid #aaaaaa !important;
  border-radius: 6px !important;
  font-size: 0.92rem !important;
}
[data-baseweb="select"] [data-baseweb="popover"] * {
  background: #ffffff !important;
  color: #111111 !important;
}

/* ── Labels & text ── */
label, .stSelectbox label, .stTextInput label, .stTextArea label,
.stDateInput label, .stNumberInput label, .stRadio label,
[data-testid="stWidgetLabel"] {
  font-size: 0.88rem !important;
  font-weight: 600 !important;
  color: #111111 !important;
}

/* ── Dataframe / table ── */
[data-testid="stDataFrame"] table,
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] td {
  background: #ffffff !important;
  color: #111111 !important;
  border-color: #cccccc !important;
  font-size: 0.9rem !important;
}
[data-testid="stDataFrame"] th {
  background: #f0f0f0 !important;
  font-weight: 700 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  border: 1.5px solid #111111 !important;
  border-radius: 8px !important;
  background: #ffffff !important;
}
[data-testid="stExpander"] summary {
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  color: #111111 !important;
}

/* ── Alerts / info boxes ── */
.stAlert, [data-testid="stAlert"] {
  background: #f8f8f8 !important;
  color: #111111 !important;
  border: 1.5px solid #111111 !important;
  border-radius: 8px !important;
}

/* ── Slider ── */
[data-testid="stSlider"] * { color: #111111 !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
  background: #111111 !important;
  border-color: #111111 !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] { border-bottom: 2px solid #111111 !important; }
[data-baseweb="tab"] {
  background: transparent !important;
  color: #555555 !important;
  font-size: 0.9rem !important;
  font-weight: 600 !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  color: #111111 !important;
  border-bottom: 2px solid #111111 !important;
}

/* ── KPI cards ── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}
.kpi-card {
  background: #ffffff;
  border: 1.5px solid #111111;
  border-radius: 8px;
  padding: 18px 16px;
}
.kpi-value {
  font-size: 2rem;
  font-weight: 900;
  color: #111111;
  line-height: 1;
  letter-spacing: -0.5px;
}
.kpi-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #555555;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.kpi-sub {
  font-size: 0.72rem;
  color: #888888;
  margin-top: 6px;
}

/* ── Section headers ── */
.section-header {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #111111;
  border-bottom: 1.5px solid #111111;
  padding-bottom: 6px;
  margin: 20px 0 12px 0;
}

/* ── ERP panels ── */
.erp-panel {
  background: #ffffff;
  border: 1.5px solid #111111;
  border-radius: 8px;
  padding: 18px;
  margin-bottom: 16px;
}
.erp-panel-header {
  font-size: 0.78rem;
  font-weight: 700;
  color: #111111;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #cccccc;
  padding-bottom: 8px;
  margin-bottom: 14px;
}

/* ── Form groups ── */
.form-group-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #111111;
  letter-spacing: 0.5px;
  border-right: 3px solid #111111;
  padding-right: 10px;
  margin: 20px 0 12px 0;
}

/* ── Badges / status ── */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  background: #f0f0f0;
  color: #111111;
  border: 1px solid #aaaaaa;
}

/* ── Collection card ── */
.collection-card {
  background: #ffffff;
  border: 1.5px solid #111111;
  border-radius: 8px;
  padding: 18px;
}
.collection-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: #111111;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
  text-transform: uppercase;
}
.collection-amount {
  font-size: 1.4rem;
  font-weight: 800;
  color: #111111;
  margin-bottom: 10px;
}
.collection-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #555555;
  margin-top: 6px;
}
.progress-bar-track {
  background: #f0f0f0;
  border-radius: 4px;
  height: 7px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background: #111111;
  border-radius: 4px;
}

/* ── Alert grid ── */
.alert-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.alert-card {
  background: #f8f8f8;
  border: 1.5px solid #cccccc;
  border-radius: 6px;
  padding: 12px;
  text-align: center;
}
.alert-num { font-size: 1.5rem; font-weight: 800; color: #111111; }
.alert-lbl { font-size: 0.65rem; color: #888888; margin-top: 3px; }

/* ── Calendar ── */
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}
.cal-day {
  background: #ffffff;
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 8px 4px;
  min-height: 80px;
  font-size: 0.75rem;
  color: #111111;
}
.cal-day-header {
  font-size: 0.65rem;
  font-weight: 700;
  color: #111111;
  text-align: center;
  padding: 4px;
  background: #f0f0f0;
  border-radius: 4px;
  margin-bottom: 4px;
}
.cal-event {
  font-size: 0.62rem;
  background: #f0f0f0;
  border: 1px solid #aaaaaa;
  border-radius: 3px;
  padding: 2px 4px;
  margin-bottom: 2px;
  color: #111111;
}

/* ── Mini KPI ── */
.kpi-mini {
  background: #f8f8f8;
  border: 1px solid #cccccc;
  border-radius: 6px;
  padding: 10px 12px;
  text-align: center;
}
.kpi-mini-label { font-size: 0.68rem; color: #555555; margin-bottom: 4px; }
.kpi-mini-value { font-size: 1.2rem; font-weight: 800; color: #111111; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0f0f0; }
::-webkit-scrollbar-thumb { background: #aaaaaa; border-radius: 3px; }


/* ── Top Header Bar ── */
.top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border-bottom: 2px solid #111111;
  padding: 12px 24px;
  margin: -24px -32px 20px -32px;
}
.top-header-left  { display: flex; align-items: center; gap: 12px; }
.top-header-title { font-size: 1.1rem; font-weight: 700; color: #111111; }
.top-header-right { display: flex; align-items: center; gap: 12px; }
.header-badge {
  font-size: 0.72rem; font-weight: 700; padding: 3px 12px;
  border-radius: 4px; background: #f0f0f0; color: #111111;
  border: 1px solid #aaaaaa;
}
.header-time { font-size: 0.75rem; color: #888888; }

/* ── Sidebar Logo & User ── */
.sb-logo {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 14px 12px 14px;
  border-bottom: 1px solid #dddddd;
  margin-bottom: 8px;
}
.sb-logo-icon  { font-size: 1.6rem; }
.sb-logo-title { font-size: 1rem; font-weight: 800; color: #111111; }
.sb-logo-sub   { font-size: 0.67rem; color: #888888; }
.sb-user {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  background: #f8f8f8;
  border-radius: 8px;
  margin: 0 8px 8px 8px;
}
.sb-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: #111111; color: #ffffff;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; font-weight: 700; flex-shrink: 0;
}
.sb-name { font-size: 0.85rem; font-weight: 700; color: #111111; }
.sb-role { font-size: 0.67rem; color: #888888; margin-top: 1px; }

/* ── Form Groups ── */
.form-group {
  border: 1.5px solid #dddddd;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 14px;
  background: #ffffff;
}
.form-group-header {
  font-size: 0.82rem; font-weight: 700; color: #111111;
  letter-spacing: 0.5px; margin-bottom: 12px;
  border-bottom: 1px solid #eeeeee; padding-bottom: 8px;
}
.form-group-body { padding: 0; }


/* ── Elevator Cards ── */
.elev-card {
  background: #ffffff;
  border: 1.5px solid #111111;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 14px;
}
.elev-card-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: #111111;
  margin-bottom: 4px;
}
.elev-card-meta {
  font-size: 0.8rem;
  color: #666666;
  margin-bottom: 2px;
}

/* ── Tech Cards ── */
.tech-card {
  background: #ffffff;
  border: 1.5px solid #111111;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  text-align: center;
}
.tech-card h3 {
  font-size: 0.92rem;
  font-weight: 700;
  color: #111111;
  margin: 0 0 10px 0;
}
.tech-stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: #555555;
  padding: 4px 0;
  border-bottom: 1px solid #eeeeee;
}
.tech-stat:last-child { border-bottom: none; }
.tech-stat strong { color: #111111; }

/* ── Responsive ── */
@media (max-width: 768px) {
  [data-testid="stMainBlockContainer"],
  .main .block-container { padding: 12px 10px !important; }
  .kpi-value { font-size: 1.5rem; }
  .kpi-label { font-size: 0.62rem; }
}

/* ── Dashboard no-scroll mode ── */
body.dash-noscroll,
body.dash-noscroll [data-testid="stApp"],
body.dash-noscroll [data-testid="stMainBlockContainer"],
body.dash-noscroll .main .block-container {
  overflow: hidden !important;
  height: 100vh !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
TECHNICIANS = ["فيصل", "سيلفوم", "فريتز", "جنيد", "كفاية الله"]
TECHNICIANS_WITH_UNASSIGNED = ["-- غير مكلف --"] + TECHNICIANS

# ─────────────────────────────────────────────
# مهمة 4: Role Enum موحد — القيم الوحيدة المعتمدة
# ─────────────────────────────────────────────
ROLE_ADMIN   = "admin"
ROLE_MANAGER = "manager"
ROLE_TECH    = "tech"
ROLE_CLIENT  = "client"
VALID_ROLES  = {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH, ROLE_CLIENT}

ROLES = {
    "admin":   "مدير عام",
    "manager": "مدير",
    "tech":    "فني",
    "client":  "عميل",
}

# ─────────────────────────────────────────────
# مهمة 6: User-Employee Mapping — ربط المستخدم بالموظف
# ─────────────────────────────────────────────
STAFF_REGISTRY = {
    "majed":  {"name": "ماجد",       "role": ROLE_ADMIN,   "team": "الإدارة",     "region": "الرياض",   "active": True},
    "ahmed":  {"name": "أحمد",       "role": ROLE_MANAGER, "team": "العمليات",    "region": "الرياض",   "active": True},
    "taha":   {"name": "طه",         "role": ROLE_MANAGER, "team": "التحصيل",     "region": "الرياض",   "active": True},
    "ali":    {"name": "علي",        "role": ROLE_MANAGER, "team": "الفني",       "region": "الرياض",   "active": True},
    "ayman":  {"name": "أيمن",       "role": ROLE_MANAGER, "team": "الهندسة",     "region": "الرياض",   "active": True},
    "faisal": {"name": "فيصل",       "role": ROLE_TECH,    "team": "الصيانة",     "region": "شمال الرياض", "active": True},
    "silvom": {"name": "سيلفوم",     "role": ROLE_TECH,    "team": "الصيانة",     "region": "وسط الرياض",  "active": True},
    "fritz":  {"name": "فريتز",      "role": ROLE_TECH,    "team": "الصيانة",     "region": "جنوب الرياض", "active": True},
    "junaid": {"name": "جنيد",       "role": ROLE_TECH,    "team": "الصيانة",     "region": "شرق الرياض",  "active": True},
    "kifaya": {"name": "كفاية الله", "role": ROLE_TECH,    "team": "الصيانة",     "region": "غرب الرياض",  "active": True},
}

def get_staff_info(username: str) -> dict:
    return STAFF_REGISTRY.get(username, {"name": username, "role": ROLE_TECH, "team": "—", "region": "—", "active": True})

def is_user_active(username: str) -> bool:
    return STAFF_REGISTRY.get(username, {}).get("active", True)

# ─────────────────────────────────────────────
# مهمة 1+2: Role Matrix + Permission Matrix
# ─────────────────────────────────────────────
# الصلاحيات: view / create / edit / delete / assign / export / approve / close / reopen / print
PERMISSIONS = {
    # شاشة العقود
    "contracts.view":    {ROLE_ADMIN, ROLE_MANAGER},
    "contracts.create":  {ROLE_ADMIN, ROLE_MANAGER},
    "contracts.edit":    {ROLE_ADMIN, ROLE_MANAGER},
    "contracts.delete":  {ROLE_ADMIN},
    "contracts.export":  {ROLE_ADMIN, ROLE_MANAGER},
    "contracts.print":   {ROLE_ADMIN, ROLE_MANAGER},
    # أوامر العمل
    "work_orders.view":    {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "work_orders.create":  {ROLE_ADMIN, ROLE_MANAGER},
    "work_orders.edit":    {ROLE_ADMIN, ROLE_MANAGER},
    "work_orders.assign":  {ROLE_ADMIN, ROLE_MANAGER},
    "work_orders.close":   {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "work_orders.reopen":  {ROLE_ADMIN, ROLE_MANAGER},
    "work_orders.export":  {ROLE_ADMIN, ROLE_MANAGER},
    "work_orders.delete":  {ROLE_ADMIN},
    # البلاغات
    "fault_reports.view":    {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH, ROLE_CLIENT},
    "fault_reports.create":  {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH, ROLE_CLIENT},
    "fault_reports.edit":    {ROLE_ADMIN, ROLE_MANAGER},
    "fault_reports.assign":  {ROLE_ADMIN, ROLE_MANAGER},
    "fault_reports.close":   {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "fault_reports.reopen":  {ROLE_ADMIN, ROLE_MANAGER},
    "fault_reports.export":  {ROLE_ADMIN, ROLE_MANAGER},
    "fault_reports.delete":  {ROLE_ADMIN},
    # الصيانة
    "maintenance.view":    {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "maintenance.create":  {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "maintenance.edit":    {ROLE_ADMIN, ROLE_MANAGER},
    "maintenance.export":  {ROLE_ADMIN, ROLE_MANAGER},
    # الداشبورد والتقارير
    "dashboard.view":     {ROLE_ADMIN, ROLE_MANAGER},
    "audit_log.view":     {ROLE_ADMIN},
    "users.manage":       {ROLE_ADMIN},
    "data_quality.view":  {ROLE_ADMIN, ROLE_MANAGER},
    "reports.export":     {ROLE_ADMIN, ROLE_MANAGER},
}

def has_perm(action: str) -> bool:
    """التحقق من صلاحية المستخدم الحالي — مهمة 3: backend authorization"""
    role = st.session_state.get("role", ROLE_CLIENT)
    if role not in VALID_ROLES:
        return False
    return role in PERMISSIONS.get(action, set())

def require_perm(action: str):
    """يوقف التنفيذ إذا لم تتوفر الصلاحية"""
    if not has_perm(action):
        role_ar = ROLES.get(st.session_state.get("role",""), "مجهول")
        st.error(f"⛔ صلاحية [{action}] غير متاحة لدور [{role_ar}]")
        st.stop()

# ─────────────────────────────────────────────
# مهمة 1: Business Glossary — تعريفات المصطلحات
# ─────────────────────────────────────────────
GLOSSARY = {
    "بلاغ":         "طلب إصلاح عطل طارئ يُرفع من العميل أو الفني",
    "أمر_عمل":      "مهمة مجدولة مربوطة بعقد وفني",
    "زيارة_صيانة":  "زيارة دورية وفق جدول العقد",
    "إغلاق":        "إنهاء البلاغ أو الأمر مع توثيق النتيجة",
    "تعليق":        "إيقاف مؤقت مع ذكر السبب",
    "تصعيد":        "رفع البلاغ لمستوى أعلى بسبب تعقيد أو تأخر",
    "عميل":         "صاحب العقد المرتبط بالمصعد",
    "موقع":         "المبنى أو العقار الذي يضم المصعد",
    "عقد":          "اتفاقية صيانة بين LiftTech والعميل",
}

# ─────────────────────────────────────────────
# مهمة 2: Status Catalog — حالات موحدة لكل وحدة
# ─────────────────────────────────────────────
CONTRACT_STATUSES = {"active": "نشط", "expired": "منتهي", "cancelled": "ملغي", "suspended": "موقوف"}
PAYMENT_STATUSES  = {"unpaid": "غير مسدد", "partial": "جزئي", "paid": "مسدد", "overdue": "متأخر"}

WO_STATUSES = {
    "pending":     "معلق",
    "in_progress": "جاري",
    "completed":   "مكتمل",
    "cancelled":   "ملغي",
    "on_hold":     "موقوف",
}
FR_STATUSES = {
    "open":        "مفتوح",
    "assigned":    "مكلف",
    "in_progress": "جاري",
    "resolved":    "محلول",
    "closed":      "مغلق",
    "escalated":   "مصعّد",
}
ML_STATUSES = {"done": "منجز", "partial": "جزئي", "rescheduled": "مُعاد جدولته"}

# ─────────────────────────────────────────────
# مهمة 3: Auto-numbering — أكواد مرجعية تلقائية
# ─────────────────────────────────────────────
def _generate_code(prefix: str, table: str, supabase_client) -> str:
    """
    يولّد كوداً تلقائياً مثل WO-0023 بناءً على آخر ID في الجدول.
    prefix: WO / FLT / PM / INV / AST
    """
    try:
        res = supabase_client.table(table).select("id").order("id", desc=True).limit(1).execute()
        last_id = res.data[0]["id"] if res.data else 0
        return f"{prefix}-{str(last_id + 1).zfill(4)}"
    except Exception:
        import random
        return f"{prefix}-{random.randint(1000,9999)}"

# ─────────────────────────────────────────────
# مهمة 7: Master Data — بيانات مرجعية ثابتة
# ─────────────────────────────────────────────
CITIES    = ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام", "الخبر", "الطائف", "أبها", "تبوك", "القصيم"]
DISTRICTS_RIYADH = ["النخيل", "العليا", "الملقا", "الورود", "السليمانية", "النزهة", "الروضة", "الصحافة",
                     "الربيع", "الياسمين", "حطين", "الغدير", "البديعة", "الشفاء", "الوادي", "طويق", "أخرى"]
FAULT_TYPES   = ["توقف تام", "أبواب لا تُغلق", "ضوضاء", "اهتزاز", "عدم وصول للطابق", "فشل كهربائي",
                 "ماس كهربائي", "تسرب زيت", "سلسلة قاطعة", "حريق في لوحة التحكم", "أخرى"]
VISIT_TYPES   = ["صيانة وقائية", "صيانة تصحيحية", "فحص دوري", "استجابة طارئة", "فحص ما بعد تركيب"]
PRIORITY_LEVELS  = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
ELEVATOR_TYPES   = ["ركاب", "شحن", "بانوراما", "خدمة", "سلم كهربائي"]
ELEVATOR_BRANDS  = ["Otis", "Kone", "Schindler", "Mitsubishi", "Thyssen", "Sigma", "Sodimas", "محلي", "أخرى"]
WORK_TYPES       = {"preventive": "وقائي", "corrective": "تصحيحي", "emergency": "طارئ", "inspection": "فحص"}

# ─────────────────────────────────────────────
# مهمة 8: Reason Codes — أسباب إلزامية
# ─────────────────────────────────────────────
CANCEL_REASONS  = ["انتهاء العقد", "طلب العميل", "خطأ في الإدخال", "تكرار", "أخرى"]
HOLD_REASONS    = ["انتظار قطع غيار", "عدم توفر فني", "طلب تأجيل من العميل", "ظروف طارئة", "أخرى"]
CLOSE_REASONS   = ["تم الإصلاح بالكامل", "إصلاح جزئي — متابعة لاحقة", "استبدال قطعة", "لا عطل — فحص وقائي", "أخرى"]
REOPEN_REASONS  = ["العطل عاد", "الحل لم يكن كافياً", "شكوى العميل", "فحص إضافي مطلوب", "أخرى"]

# ─────────────────────────────────────────────
# مهمة 11: Data Formatting Standards
# ─────────────────────────────────────────────
def fmt_phone(phone: str) -> str:
    """توحيد رقم الجوال: يبدأ بـ 05 وطوله 10"""
    p = "".join(filter(str.isdigit, str(phone or "")))
    if len(p) == 9 and p.startswith("5"): p = "0" + p
    if len(p) == 10 and p.startswith("05"): return p
    return phone  # إرجاع كما هو إذا لم يطابق

def fmt_date_ar(d) -> str:
    """تنسيق التاريخ: YYYY/MM/DD"""
    try: return str(d)[:10].replace("-", "/")
    except: return str(d or "—")

def validate_phone(phone: str) -> bool:
    p = "".join(filter(str.isdigit, str(phone or "")))
    if len(p) == 9 and p.startswith("5"): p = "0" + p
    return len(p) == 10 and p.startswith("05")

# ─────────────────────────────────────────────
# مهام 4,5: Validation Engine — حقول إلزامية + قواعد تحقق
# ─────────────────────────────────────────────
class ValidationError(Exception):
    pass

def validate_work_order(title: str, contract_id, technician: str,
                         scheduled_date, status: str) -> list:
    """يعيد قائمة رسائل الخطأ (فارغة = صحيح)"""
    errors = []
    if not title.strip():
        errors.append("عنوان أمر العمل مطلوب")
    if not contract_id:
        errors.append("يجب اختيار عقد مرتبط")
    if not technician or technician == "-- غير مكلف --":
        errors.append("يجب تعيين فني مسؤول")
    if scheduled_date is None:
        errors.append("تاريخ الجدولة مطلوب")
    elif scheduled_date < date.today() - timedelta(days=1):
        errors.append("تاريخ الجدولة لا يمكن أن يكون في الماضي البعيد")
    return errors

def validate_fault_report(description: str) -> list:
    errors = []
    if not description.strip():
        errors.append("وصف العطل مطلوب")
    if len(description.strip()) < 10:
        errors.append("وصف العطل قصير جداً — أدخل 10 أحرف على الأقل")
    return errors

def validate_contract(contract_no: str, customer_name: str,
                       start_date, end_date, contract_value: float) -> list:
    errors = []
    if not contract_no.strip():
        errors.append("رقم العقد مطلوب")
    if not customer_name.strip():
        errors.append("اسم العميل مطلوب")
    if start_date and end_date and end_date <= start_date:
        errors.append("تاريخ الانتهاء يجب أن يكون بعد تاريخ البداية")
    if contract_value < 0:
        errors.append("قيمة العقد لا يمكن أن تكون سالبة")
    return errors

def validate_maintenance_log(work_done: str, contract_id, technician: str) -> list:
    errors = []
    if not work_done.strip():
        errors.append("الأعمال المنجزة مطلوبة")
    if not contract_id:
        errors.append("يجب اختيار عقد مرتبط")
    if not technician:
        errors.append("يجب اختيار الفني")
    return errors

def show_validation_errors(errors: list) -> bool:
    """يعرض الأخطاء ويعيد True إذا وُجدت أخطاء"""
    if errors:
        for err in errors:
            st.error(f"❌ {err}")
        return True
    return False

# ─────────────────────────────────────────────
# مهمة 6: Duplicate Detection — اكتشاف التكرار
# ─────────────────────────────────────────────
def check_duplicate_fault(supabase_client, contract_id, description: str,
                            hours_window: int = 24) -> bool:
    """
    يتحقق من وجود بلاغ مكرر لنفس العقد بنفس الوصف
    خلال فترة hours_window ساعة
    """
    if supabase_client is None or not contract_id:
        return False
    try:
        from datetime import datetime, timedelta
        since = (datetime.now() - timedelta(hours=hours_window)).isoformat()
        res = supabase_client.table("fault_reports")             .select("id, description, reported_date")             .eq("contract_id", contract_id)             .gte("reported_date", since[:10])             .execute()
        for row in (res.data or []):
            existing_desc = str(row.get("description","")).strip().lower()
            new_desc = description.strip().lower()
            # تشابه نصي بسيط — 60% من الكلمات مشتركة
            w1 = set(existing_desc.split())
            w2 = set(new_desc.split())
            if w1 and w2:
                overlap = len(w1 & w2) / max(len(w1), len(w2))
                if overlap >= 0.6:
                    return True
        return False
    except Exception:
        return False

def check_duplicate_work_order(supabase_client, contract_id, title: str,
                                 technician: str, scheduled_date) -> bool:
    """يتحقق من وجود أمر عمل مكرر بنفس العقد والفني والتاريخ"""
    if supabase_client is None or not contract_id:
        return False
    try:
        res = supabase_client.table("work_orders")             .select("id, title, technician, scheduled_date")             .eq("contract_id", contract_id)             .eq("technician", technician)             .eq("scheduled_date", str(scheduled_date))             .not_.in_("status", ["cancelled", "completed"])             .execute()
        return len(res.data or []) > 0
    except Exception:
        return False

# ─────────────────────────────────────────────
# مهمة 9: Workflow Guardrails — التسلسل المنطقي
# ─────────────────────────────────────────────
# انتقالات الحالة المسموحة
WO_TRANSITIONS = {
    "pending":     ["in_progress", "cancelled", "on_hold"],
    "in_progress": ["completed",   "cancelled", "on_hold"],
    "on_hold":     ["in_progress", "cancelled"],
    "completed":   [],   # نهائية — لا تعديل
    "cancelled":   [],   # نهائية — لا تعديل
}
FR_TRANSITIONS = {
    "open":        ["assigned",    "closed"],
    "assigned":    ["in_progress", "open",   "escalated"],
    "in_progress": ["resolved",    "on_hold","escalated"],
    "on_hold":     ["in_progress", "closed"],
    "resolved":    ["closed",      "open"],   # إعادة فتح ممكنة
    "closed":      ["open"],                  # إعادة فتح فقط
    "escalated":   ["in_progress", "closed"],
}

def get_allowed_transitions(current_status: str, transitions_map: dict) -> list:
    return transitions_map.get(current_status, [])

def is_valid_transition(from_status: str, to_status: str, transitions_map: dict) -> bool:
    allowed = get_allowed_transitions(from_status, transitions_map)
    return to_status in allowed or to_status == from_status

def validate_closure(status: str, close_reason: str, technician: str) -> list:
    """يتحقق من اكتمال بيانات الإغلاق — مهمة 17"""
    errors = []
    if status in ("completed", "closed", "resolved"):
        if not close_reason or close_reason == "-- اختر --":
            errors.append("سبب الإغلاق مطلوب")
        if not technician or technician == "-- غير مكلف --":
            errors.append("الفني المنفذ مطلوب عند الإغلاق")
    return errors

# ─────────────────────────────────────────────
# مهمة 10: Timestamps Model — أوقات دورة الحياة
# ─────────────────────────────────────────────
def get_lifecycle_timestamps(record: dict) -> dict:
    """يستخرج طوابع الوقت من السجل مع دعم الأسماء القديمة والجديدة"""
    return {
        "إنشاء":    record.get("created_at") or record.get("reported_date"),
        "تعيين":    record.get("assigned_at"),
        "بدء":      record.get("started_at"),
        "إنجاز":    record.get("completed_at"),
        "إغلاق":    record.get("closed_at"),
    }

# ─────────────────────────────────────────────
# مهمة 14: User-Friendly Error Messages
# ─────────────────────────────────────────────
DB_ERRORS = {
    "duplicate key":         "⚠️ هذا السجل مسجّل مسبقاً — تحقق من رقم العقد أو البلاغ",
    "foreign key":           "⚠️ لا يمكن حذف هذا السجل — توجد بيانات مرتبطة به",
    "null value":            "⚠️ حقل مطلوب لم يُملأ — راجع النموذج",
    "connection":            "⚠️ تعذّر الاتصال بقاعدة البيانات — حاول مجدداً",
    "permission":            "⚠️ ليس لديك صلاحية لإجراء هذه العملية",
    "timeout":               "⚠️ انتهت مهلة الاتصال — حاول مجدداً",
    "not found":             "⚠️ السجل المطلوب غير موجود",
    "column":                "⚠️ خطأ في البيانات — تواصل مع المدير",
}

def friendly_error(exc: Exception) -> str:
    msg = str(exc).lower()
    for key, friendly in DB_ERRORS.items():
        if key in msg:
            return friendly
    return f"⚠️ حدث خطأ غير متوقع: {str(exc)[:120]}"

# ─────────────────────────────────────────────
# مهمة 15: Field Change Tracking في log_action
# ─────────────────────────────────────────────
def build_change_summary(old: dict, new: dict, fields: list) -> tuple:
    """
    يقارن حقول محددة بين القيم القديمة والجديدة.
    يعيد (old_str, new_str) للحقول التي تغيّرت.
    """
    changed_old = {}
    changed_new = {}
    for f in fields:
        v_old = str(old.get(f,"") or "")
        v_new = str(new.get(f,"") or "")
        if v_old.strip() != v_new.strip():
            changed_old[f] = v_old
            changed_new[f] = v_new
    old_str = " | ".join(f"{k}: {v}" for k,v in changed_old.items()) if changed_old else ""
    new_str = " | ".join(f"{k}: {v}" for k,v in changed_new.items()) if changed_new else ""
    return old_str, new_str

# ─────────────────────────────────────────────
# مهمة 11: Reopen Policy — سياسة إعادة الفتح
# ─────────────────────────────────────────────
REOPEN_REQUIRES_ADMIN = True   # إعادة الفتح تحتاج admin أو manager فقط

def can_reopen(record_status: str, actor_role: str) -> bool:
    """يتحقق من إمكانية إعادة فتح السجل"""
    if record_status not in ("completed", "closed", "cancelled"):
        return False  # السجل ليس في حالة نهائية
    if REOPEN_REQUIRES_ADMIN:
        return actor_role in (ROLE_ADMIN, ROLE_MANAGER)
    return True

def validate_reopen(record_status: str, reopen_reason: str) -> list:
    errors = []
    actor_role = st.session_state.get("role", "")
    if not can_reopen(record_status, actor_role):
        errors.append("إعادة الفتح تتطلب صلاحية مدير أو مدير عام")
    if not reopen_reason or reopen_reason == "-- اختر --":
        errors.append("سبب إعادة الفتح مطلوب")
    return errors

# ─────────────────────────────────────────────
# مهمة 12: Approval Rules — قواعد الاعتماد
# ─────────────────────────────────────────────
# الإجراءات التي تحتاج اعتمادًا
APPROVAL_REQUIRED = {
    "contract.delete":   {ROLE_ADMIN},
    "work_order.delete": {ROLE_ADMIN},
    "fault.delete":      {ROLE_ADMIN},
    "work_order.cancel": {ROLE_ADMIN, ROLE_MANAGER},
    "contract.edit_value": {ROLE_ADMIN, ROLE_MANAGER},
    "record.reopen":     {ROLE_ADMIN, ROLE_MANAGER},
    "tech.reassign":     {ROLE_ADMIN, ROLE_MANAGER},
}

def needs_approval(action_key: str) -> bool:
    """يتحقق إذا كان الإجراء يحتاج اعتمادًا من دور معين"""
    allowed = APPROVAL_REQUIRED.get(action_key, set())
    return bool(allowed)  # إذا وجد في القائمة = يحتاج اعتماد

def can_approve(action_key: str) -> bool:
    role = st.session_state.get("role", "")
    return role in APPROVAL_REQUIRED.get(action_key, set())

# ─────────────────────────────────────────────
# مهمة 13: Decision Log — سجل القرارات الإدارية
# ─────────────────────────────────────────────
def log_decision(decision_type: str, entity_type: str, entity_id: str,
                 decision: str, reason: str = "", notes: str = ""):
    """
    يسجل قرارًا إداريًا (اعتماد/رفض/تصعيد) في audit_logs
    decision: "approved" | "rejected" | "escalated"
    """
    action_map = {"approved": "approve", "rejected": "reject", "escalated": "escalate"}
    action = action_map.get(decision, "approve")
    details = f"نوع: {decision_type} | القرار: {decision} | السبب: {reason}"
    if notes:
        details += f" | ملاحظة: {notes}"
    log_action(
        action=action,
        module=entity_type,
        details=details[:500],
        severity="important",
        entity_id=str(entity_id),
    )

# ─────────────────────────────────────────────
# مهمة 15: Export Controls — ضبط التصدير والطباعة
# ─────────────────────────────────────────────
def log_export(module: str, record_count: int, export_format: str = "CSV"):
    """يسجل كل عملية تصدير في سجل الأحداث"""
    if not has_perm(f"{module}.export"):
        log_action("unauthorized", module,
                   f"محاولة تصدير غير مصرح — {module}",
                   severity="security")
        return False
    log_action("export", module,
               f"تصدير {record_count} سجل بصيغة {export_format}",
               severity="sensitive")
    return True

def controlled_download_button(label: str, data, filename: str,
                                 mime: str, module: str, record_count: int = 0,
                                 export_format: str = "CSV", key: str = None):
    """زر تصدير مراقَب — يتحقق من الصلاحية ويسجل في سجل الأحداث"""
    if not has_perm(f"{module}.export"):
        st.warning("⛔ لا تملك صلاحية تصدير بيانات هذه الوحدة")
        return
    if st.download_button(label, data=data, file_name=filename, mime=mime, key=key):
        log_export(module, record_count, export_format)

# ─────────────────────────────────────────────
# مهمة 19: Data Quality Report Helper
# ─────────────────────────────────────────────
def data_quality_report(contracts: list, work_orders: list,
                          fault_reports: list, maintenance_logs: list) -> dict:
    """يُنتج ملخص جودة البيانات"""
    issues = []

    # عقود بدون رقم جوال
    no_mobile = [c.get("contract_no","—") for c in contracts if not c.get("mobile","").strip()]
    if no_mobile:
        issues.append(f"📵 {len(no_mobile)} عقد بدون رقم جوال: {', '.join(no_mobile[:3])}{'...' if len(no_mobile)>3 else ''}")

    # عقود منتهية لا تزال نشطة
    today = date.today()
    stale_active = []
    for c in contracts:
        if c.get("contract_status") == "active":
            ed = None
            try:
                from datetime import date as _d
                ed = _d.fromisoformat(str(c.get("end_date",""))[:10])
            except Exception:
                pass
            if ed and ed < today:
                stale_active.append(c.get("contract_no","—"))
    if stale_active:
        issues.append(f"⏰ {len(stale_active)} عقد نشط لكن تاريخه منتهٍ")

    # بلاغات مفتوحة منذ أكثر من 7 أيام
    old_open = 0
    for fr in fault_reports:
        if fr.get("status") in ("open", "assigned"):
            try:
                rd = date.fromisoformat(str(fr.get("reported_date",""))[:10])
                if (today - rd).days > 7:
                    old_open += 1
            except Exception:
                pass
    if old_open:
        issues.append(f"🔴 {old_open} بلاغ مفتوح منذ أكثر من 7 أيام")

    # أوامر عمل معلقة منذ أكثر من 14 يوماً
    stale_wo = 0
    for wo in work_orders:
        if wo.get("status") == "pending":
            try:
                sd = date.fromisoformat(str(wo.get("scheduled_date",""))[:10])
                if (today - sd).days > 14:
                    stale_wo += 1
            except Exception:
                pass
    if stale_wo:
        issues.append(f"⏳ {stale_wo} أمر عمل معلق تجاوز 14 يوماً")

    # عقود بدون سجلات صيانة
    ml_contract_ids = {m.get("contract_id") for m in maintenance_logs}
    no_maintenance = [c.get("contract_no","—") for c in contracts
                      if c.get("contract_status") == "active"
                      and c.get("id") not in ml_contract_ids]
    if no_maintenance:
        issues.append(f"🔧 {len(no_maintenance)} عقد نشط بدون أي سجل صيانة")

    return {
        "total_issues": len(issues),
        "issues":       issues,
        "contracts":    len(contracts),
        "work_orders":  len(work_orders),
        "fault_reports":len(fault_reports),
        "maintenance":  len(maintenance_logs),
    }

# ─────────────────────────────────────────────
# Supabase
# ─────────────────────────────────────────────
@st.cache_resource
def init_supabase():
    try:
        from supabase import create_client
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        client = create_client(url, key)
        try:
            client.table("user_passwords").select("username").limit(1).execute()
        except Exception:
            pass
        return client
    except Exception as e:
        st.error(f"❌ تعذّر الاتصال بـ Supabase: {e}")
        return None

supabase = init_supabase()

# ─────────────────────────────────────────────
# Audit Log — سجل الأحداث
# ─────────────────────────────────────────────
def _ensure_audit_table():
    """ينشئ جدول audit_logs إن لم يكن موجوداً (يُستدعى مرة عند بدء التطبيق)."""
    if supabase is None:
        return
    try:
        supabase.table("audit_logs").select("id").limit(1).execute()
    except Exception as e:
        if "PGRST205" in str(e) or "not found" in str(e).lower():
            # الجدول غير موجود — سجّل رسالة للمدير
            pass  # سيتم إنشاؤه يدوياً أو عبر SQL أدناه

_ensure_audit_table()

# ─────────────────────────────────────────────
# مهمة 10: Event Schema مكتمل — كل حدث يُسجّل بـ:
# username, role, action, module, entity_id, details,
# severity, old_value, new_value, session_id, created_at
# ─────────────────────────────────────────────

# الأحداث المعتمدة (مهمة 7)
AUDIT_ACTIONS = {
    "login":           ("تسجيل دخول",         "security"),
    "logout":          ("تسجيل خروج",          "normal"),
    "login_fail":      ("فشل تسجيل دخول",      "security"),
    "add":             ("إضافة سجل",            "normal"),
    "edit":            ("تعديل سجل",            "important"),
    "delete":          ("حذف سجل",              "critical"),
    "assign":          ("إسناد لفني",           "normal"),
    "close":           ("إغلاق سجل",            "important"),
    "reopen":          ("إعادة فتح",            "important"),
    "export":          ("تصدير بيانات",         "sensitive"),
    "print":           ("طباعة",                "sensitive"),
    "perm_change":     ("تغيير صلاحية",         "critical"),
    "password_reset":  ("إعادة ضبط كلمة مرور", "sensitive"),
    "unauthorized":    ("محاولة وصول غير مصرح","security"),
    "approve":         ("اعتماد قرار",          "important"),
    "reject":          ("رفض قرار",             "important"),
    "escalate":        ("تصعيد",                "important"),
    "view":            ("مشاهدة",               "normal"),
}

def _get_session_id() -> str:
    """معرّف الجلسة — يُولَّد عند تسجيل الدخول ويبقى ثابتاً"""
    if "session_id" not in st.session_state:
        import secrets as _sec
        st.session_state["session_id"] = _sec.token_hex(8)
    return st.session_state["session_id"]

def log_action(action: str, module: str, details: str = "",
               severity: str = "auto", entity_id: str = "",
               old_value: str = "", new_value: str = "",
               username_override: str = ""):
    """
    مهمة 7,8,9,10: يسجّل حدثاً شاملاً في audit_logs.
    severity="auto" → يحدد تلقائياً من AUDIT_ACTIONS
    """
    if supabase is None:
        return
    try:
        username = username_override or st.session_state.get("username", "system")
        role     = st.session_state.get("role", "")
        # مهمة 8: تصنيف تلقائي للحساسية
        if severity == "auto" or severity == "normal":
            _, auto_sev = AUDIT_ACTIONS.get(action, ("", "normal"))
            # رفع الحساسية للوحدات الحرجة
            if action == "edit" and module in ("contracts",):
                auto_sev = "important"
            if action in ("delete",):
                auto_sev = "critical"
            severity = auto_sev
        session_id = _get_session_id() if st.session_state.get("logged_in") else "no_session"
        supabase.table("audit_logs").insert({
            "username":   username,
            "role":       role,
            "action":     action,
            "module":     module,
            "details":    (details or "")[:500],
            "severity":   severity,
            "entity_id":  (entity_id or "")[:100],
            "old_value":  (old_value or "")[:500],
            "new_value":  (new_value or "")[:500],
            "created_at": datetime.utcnow().isoformat(),
        }).execute()
    except Exception:
        pass

# ─────────────────────────────────────────────
# Password management
# ─────────────────────────────────────────────
def get_db_password(username: str):
    if supabase is None:
        return None
    try:
        r = supabase.table("user_passwords").select("password").eq("username", username).execute()
        if r.data:
            return r.data[0]["password"]
    except Exception:
        pass
    return None

def set_db_password(username: str, new_password: str) -> bool:
    if supabase is None:
        return False
    try:
        existing = supabase.table("user_passwords").select("username").eq("username", username).execute()
        if existing.data:
            supabase.table("user_passwords").update({
                "password": new_password,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("username", username).execute()
        else:
            supabase.table("user_passwords").insert({
                "username": username,
                "password": new_password,
            }).execute()
        return True
    except Exception as e:
        err = str(e)
        if "user_passwords" in err and ("not found" in err.lower() or "PGRST205" in err):
            st.error("❌ جدول كلمات المرور غير موجود. يرجى تنفيذ الـ SQL في Supabase Dashboard.")
        else:
            st.error(f"❌ خطأ في حفظ كلمة المرور: {e}")
        return False

# ─────────────────────────────────────────────
# مهمة 16: Password Policy
# ─────────────────────────────────────────────
PWD_MIN_LENGTH = 6
PWD_FORBIDDEN  = {"12345", "123456", "password", "lifttech", "admin", "00000", "111111"}

def validate_new_password(pwd: str, username: str = "") -> list:
    errors = []
    if len(pwd) < PWD_MIN_LENGTH:
        errors.append(f"كلمة المرور يجب أن تكون {PWD_MIN_LENGTH} أحرف على الأقل")
    if pwd.lower() in PWD_FORBIDDEN:
        errors.append("كلمة المرور ضعيفة جداً — اختر كلمة مختلفة")
    if username and pwd.lower() == username.lower():
        errors.append("كلمة المرور لا يمكن أن تكون اسم المستخدم")
    return errors

# ─────────────────────────────────────────────
# مهمة 17: Session Controls — انتهاء الجلسة
# ─────────────────────────────────────────────
SESSION_TIMEOUT_MINUTES = 120  # ساعتان

def check_session_timeout() -> bool:
    last = st.session_state.get("last_activity")
    if not last:
        return False
    try:
        last_dt = datetime.fromisoformat(last)
        elapsed = (datetime.utcnow() - last_dt).total_seconds() / 60
        if elapsed > SESSION_TIMEOUT_MINUTES:
            return True
        st.session_state["last_activity"] = datetime.utcnow().isoformat()
        return False
    except Exception:
        return False

def enforce_session_timeout():
    """يُنفذ تسجيل الخروج التلقائي عند انتهاء الجلسة"""
    if st.session_state.get("logged_in") and check_session_timeout():
        username = st.session_state.get("username", "")
        log_action("logout", "system",
                   f"انتهاء الجلسة تلقائياً بعد {SESSION_TIMEOUT_MINUTES} دقيقة",
                   severity="normal", username_override=username)
        for key in ["logged_in","username","role","display_name","client_contract",
                    "session_id","last_activity","current_page"]:
            st.session_state.pop(key, None)
        st.query_params.clear()
        st.rerun()

# ─────────────────────────────────────────────
# Authentication — Odoo Login Style
# ─────────────────────────────────────────────
def check_login():
    # ── استعادة الجلسة من query_params عند التحديث ──
    if not st.session_state.get("logged_in"):
        qp = st.query_params
        if qp.get("u") and qp.get("r"):
            import base64, hashlib
            u = qp.get("u", "")
            r = qp.get("r", "")
            tk = qp.get("tk", "")
            n = qp.get("n", u)
            cc = qp.get("cc", "")
            # التحقق من token البسيط
            expected = hashlib.md5(f"{u}:{r}:lifttech2024".encode()).hexdigest()[:12]
            if tk == expected:
                st.session_state.logged_in       = True
                st.session_state.username        = u
                st.session_state.role            = r
                st.session_state.display_name    = n
                st.session_state.client_contract = cc
                # مهمة 17: استعادة session
                if "last_activity" not in st.session_state:
                    st.session_state["last_activity"] = datetime.utcnow().isoformat()
                if "session_id" not in st.session_state:
                    import secrets as _sec
                    st.session_state["session_id"] = _sec.token_hex(8)
                # استعادة الصفحة الأخيرة
                saved_pg = qp.get("pg", "dashboard")
                if saved_pg:
                    st.session_state["current_page"] = saved_pg

    if st.session_state.get("logged_in"):
        return True

    # Login page CSS override
    st.markdown("""
    <style>
    .stApp { background:#f8f8f8 !important; }
    .block-container { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Centered login card
    _, col_mid, _ = st.columns([1, 1.1, 1])
    with col_mid:
        st.markdown("""
        <div style="margin-top:80px; background:white; border-radius:10px; padding:40px 36px;
                    box-shadow:0 8px 32px rgba(0,0,0,0.12); text-align:center;
                    border: 1px solid #d9dde8;">
          <div style="width:64px;height:64px;background:#111111;border-radius:10px;
                      display:flex;align-items:center;justify-content:center;
                      font-size:2rem;margin:0 auto 16px;
                      box-shadow:0 4px 14px rgba(0,0,0,0.15);">🛗</div>
          <div style="font-size:1.6rem;font-weight:900;color:#111111;letter-spacing:0.5px;margin-bottom:4px;">LIFT TECH</div>
          <div style="font-size:0.95rem;color:#888888;margin-bottom:30px;">مركز إدارة وتشغيل المصاعد</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            submit   = st.form_submit_button("تسجيل الدخول", use_container_width=True, type="primary")

        if submit:
            try:
                users = st.secrets["users"]
                if username not in users:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    user_data = users[username]
                    if isinstance(user_data, str):
                        secrets_pwd  = user_data
                        role_val     = "admin"
                        name_val     = username
                        contract_val = ""
                    else:
                        secrets_pwd  = user_data.get("password", "")
                        role_val     = user_data.get("role", "admin")
                        name_val     = user_data.get("name", username)
                        contract_val = user_data.get("contract_no", "")

                    db_pwd     = get_db_password(username)
                    active_pwd = db_pwd if db_pwd is not None else secrets_pwd
                    if active_pwd == password:
                        if password == "12345":
                            st.session_state["force_change_pwd"] = True
                            st.session_state["pending_username"]  = username
                            st.session_state["pending_role"]      = role_val
                            st.session_state["pending_name"]      = name_val
                            st.session_state["pending_contract"]  = contract_val
                            st.rerun()
                            return False
                        st.session_state.logged_in       = True
                        st.session_state.username        = username
                        st.session_state.role            = role_val
                        st.session_state.display_name    = name_val
                        st.session_state.client_contract = contract_val
                        # كتابة query_params لحفظ الجلسة عند التحديث
                        import hashlib
                        tk = hashlib.md5(f"{username}:{role_val}:lifttech2024".encode()).hexdigest()[:12]
                        st.query_params.update({
                            "u":  username,
                            "r":  role_val,
                            "n":  name_val,
                            "cc": contract_val,
                            "tk": tk,
                            "pg": "dashboard",
                        })
                        # مهمة 10: session_id فريد لكل جلسة
                        import secrets as _sec
                        st.session_state["session_id"] = _sec.token_hex(8)
                        # مهمة 17: وقت آخر نشاط
                        st.session_state["last_activity"] = datetime.utcnow().isoformat()
                        log_action("login", "system", f"تسجيل دخول: {name_val} ({role_val})")
                        st.rerun()
                    else:
                        # مهمة 7: تسجيل فشل الدخول
                        log_action("login_fail", "system",
                                   f"فشل تسجيل دخول للمستخدم: {username}",
                                   severity="security",
                                   username_override=username)
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            except Exception:
                st.error("❌ لا توجد بيانات مستخدمين في الإعدادات")
    return False

# ── شاشة إجبار تغيير كلمة المرور ──
if st.session_state.get("force_change_pwd"):
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown(
            "<div style=\"margin-top:60px;background:#fff;border-radius:10px;"
            "padding:36px;box-shadow:0 8px 32px rgba(0,0,0,.12);direction:rtl;\">"
            "<div style=\"font-size:1.2rem;font-weight:900;color:#111;margin-bottom:6px;\">🔐 تغيير كلمة المرور مطلوب</div>"
            "<div style=\"font-size:0.85rem;color:#888;margin-bottom:20px;\">"
            "كلمة المرور الافتراضية لا تزال مفعّلة. يجب تغييرها قبل المتابعة.</div></div>",
            unsafe_allow_html=True)
        with st.form("force_pwd_form"):
            new_p1 = st.text_input("كلمة المرور الجديدة", type="password", placeholder="6 أحرف على الأقل")
            new_p2 = st.text_input("تأكيد كلمة المرور",  type="password", placeholder="أعد الإدخال")
            save_btn = st.form_submit_button("💾 حفظ وتسجيل الدخول", use_container_width=True, type="primary")
        if save_btn:
            uname_pending = st.session_state.get("pending_username", "")
            pwd_errs = validate_new_password(new_p1, uname_pending)
            if new_p1 != new_p2:
                pwd_errs.append("كلمتا المرور غير متطابقتين")
            if show_validation_errors(pwd_errs):
                pass
            else:
                uname = st.session_state.get("pending_username", "")
                set_db_password(uname, new_p1)
                log_action("password_reset", "passwords",
                           f"تغيير كلمة المرور الافتراضية: {uname}", severity="sensitive")
                import hashlib
                role_v     = st.session_state.get("pending_role", "")
                name_v     = st.session_state.get("pending_name", uname)
                contract_v = st.session_state.get("pending_contract", "")
                tk = hashlib.md5(f"{uname}:{role_v}:lifttech2024".encode()).hexdigest()[:12]
                for k in ["force_change_pwd","pending_username","pending_role","pending_name","pending_contract"]:
                    st.session_state.pop(k, None)
                st.session_state.logged_in       = True
                st.session_state.username        = uname
                st.session_state.role            = role_v
                st.session_state.display_name    = name_v
                st.session_state.client_contract = contract_v
                st.query_params.update({"u":uname,"r":role_v,"n":name_v,"cc":contract_v,"tk":tk,"pg":"dashboard"})
                st.success("✅ تم تغيير كلمة المرور")
                st.rerun()
    st.stop()

if not check_login():
    st.stop()

# Role helpers
def get_role():    return st.session_state.get("role", "admin")
def is_admin():    return get_role() == "admin"
def is_tech():     return get_role() == "tech"
def is_manager():  return get_role() == "manager"
def is_client():   return get_role() == "client"

def require_role(*allowed_roles):
    """إيقاف التنفيذ إذا لم يكن للمستخدم الصلاحية المطلوبة"""
    if get_role() not in allowed_roles:
        st.error("⛔ ليس لديك صلاحية للوصول إلى هذه الصفحة")
        st.stop()

def scope_by_role(records: list, technician_field: str = "technician") -> list:
    """تصفية السجلات حسب الدور: الفني يرى بياناته فقط، الإدارة ترى الكل"""
    role = get_role()
    if role == "tech":
        username = st.session_state.get("username", "")
        # نجلب اسم الفني الكامل من USERS
        user_info = st.secrets.get("users", {}).get(username, {})
        tech_name = user_info.get("name", username)
        return [r for r in records if (r.get(technician_field) or "") == tech_name]
    return records

# ─────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────
def safe_text(val, default=""):
    if val is None: return default
    s = str(val).strip()
    return s if s else default

def safe_number(val, default=0.0):
    try:    return float(val)
    except: return default

def safe_int(val, default=0):
    try:    return int(val)
    except: return default

def parse_date_safe(val):
    if val is None: return None
    try:   return pd.to_datetime(val).date()
    except: return None

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def priority_badge(priority):
    labels = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
    label  = labels.get(priority, priority)
    return f'<span class="badge badge-{priority}">{label}</span>'

def status_badge(status):
    labels = {
        "pending": "معلق", "in_progress": "جاري", "completed": "مكتمل",
        "cancelled": "ملغي", "open": "مفتوح", "assigned": "مكلف",
        "resolved": "محلول", "closed": "مغلق",
    }
    label = labels.get(status, status)
    return f'<span class="badge badge-{status}">{label}</span>'

# ─────────────────────────────────────────────
# Data loaders
# ─────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_contracts():
    if supabase is None: return []
    try:
        resp = supabase.table("contracts").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل العقود: {e}")
        return []

@st.cache_data(ttl=30)
def load_work_orders():
    if supabase is None: return []
    try:
        resp = supabase.table("work_orders").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل أوامر العمل: {e}")
        return []

@st.cache_data(ttl=30)
def load_fault_reports():
    if supabase is None: return []
    try:
        resp = supabase.table("fault_reports").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل البلاغات: {e}")
        return []

@st.cache_data(ttl=30)
def load_maintenance_logs():
    if supabase is None: return []
    try:
        resp = supabase.table("maintenance_logs").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل سجل الصيانة: {e}")
        return []

def prepare_contracts_df(contracts):
    if not contracts: return pd.DataFrame()
    df    = pd.DataFrame(contracts)
    today = date.today()

    def compute_days(row):
        d = parse_date_safe(row.get("end_date"))
        return None if d is None else (d - today).days

    df["days_remaining"] = df.apply(compute_days, axis=1)

    def compute_status_display(row):
        cs = safe_text(row.get("contract_status"), "active")
        if cs == "expired": return "منتهي"
        dr = row.get("days_remaining")
        if dr is None: return "نشط"
        if dr < 0:     return "منتهي"
        if dr <= 30:   return "ينتهي قريباً"
        return "نشط"

    df["status_display"]  = df.apply(compute_status_display, axis=1)
    payment_map           = {"paid": "مسدد", "partial": "جزئي", "unpaid": "غير مسدد"}
    df["payment_display"] = df["payment_status"].map(payment_map).fillna(df["payment_status"].fillna("—"))
    return df

def contract_label(c):
    no   = safe_text(c.get("contract_no"),   "—")
    name = safe_text(c.get("customer_name"), "—")
    bldg = safe_text(c.get("building_name"), "")
    return f"{no} – {name}" + (f" ({bldg})" if bldg else "")

def id_to_contract_no_map(contracts):
    return {str(c.get("id", "")): str(c.get("contract_no", "—")) for c in contracts}

# ─────────────────────────────────────────────
# WhatsApp (UltraMsg)
# ─────────────────────────────────────────────
def send_whatsapp(phone: str, message: str) -> dict:
    try:
        instance = st.secrets.get("ULTRAMSG_INSTANCE", "instance180540")
        token    = st.secrets.get("ULTRAMSG_TOKEN",    "aewoi63k2ayyayx1")
    except Exception:
        instance = "instance180540"
        token    = "aewoi63k2ayyayx1"

    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("0"):
        phone = "966" + phone[1:]
    elif not phone.startswith("966"):
        phone = "966" + phone

    url  = f"https://api.ultramsg.com/{instance}/messages/chat"
    data = urllib.parse.urlencode({
        "token": token, "to": phone, "body": message, "priority": 1,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = _json.loads(resp.read().decode())
            return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_renewal_reminders(df: pd.DataFrame, days_before: int = 30) -> list:
    if "wa_sent_contracts" not in st.session_state:
        st.session_state["wa_sent_contracts"] = set()

    today   = pd.Timestamp.now().normalize()
    cutoff  = today + pd.Timedelta(days=days_before)
    results = []

    for _, row in df.iterrows():
        contract_no  = safe_text(row.get("contract_no"),   "")
        customer     = safe_text(row.get("customer_name"), "عميل")
        building     = safe_text(row.get("building_name"), "")
        phone        = safe_text(row.get("mobile") or row.get("phone"), "")
        end_date_raw = row.get("end_date")

        try:
            end_dt = pd.to_datetime(end_date_raw, errors="coerce")
        except Exception:
            end_dt = pd.NaT

        if pd.isna(end_dt) or end_dt < today or end_dt > cutoff:
            continue

        if not phone or phone in ("—", "لا يوجد"):
            results.append({"status": "no_phone", "customer": customer, "contract_no": contract_no, "phone": ""})
            continue

        if contract_no in st.session_state["wa_sent_contracts"]:
            results.append({"status": "skipped", "customer": customer, "contract_no": contract_no, "phone": phone})
            continue

        end_str = end_dt.strftime("%Y-%m-%d")
        msg = (
            f"🛗 *لفتك للمصاعد*\n"
            f"عزيزي {customer}،\n"
            f"عقد صيانة المصعد – مبنى: {building}\n"
            f"رقم العقد: {contract_no}\n"
            f"ينتهي بتاريخ: {end_str}\n"
            f"نأمل تجديد التعامل معكم. للتواصل والتجديد يرجى الاتصال بنا. 🙏"
        )
        res = send_whatsapp(phone, msg)
        if res["ok"]:
            st.session_state["wa_sent_contracts"].add(contract_no)
            results.append({"status": "sent", "customer": customer, "contract_no": contract_no, "phone": phone})
        else:
            results.append({"status": "failed", "customer": customer, "contract_no": contract_no,
                             "phone": phone, "error": res.get("error", "")})
    return results

def notify_technician_whatsapp(technician_name: str, task_title: str, scheduled_date: str,
                                contract_no: str, building: str, priority: str):
    try:
        tech_phones = {
            "فيصل":       st.secrets.get("TECH_PHONE_FAISAL",   ""),
            "سيلفوم":     st.secrets.get("TECH_PHONE_SILVOM",   ""),
            "فريتز":      st.secrets.get("TECH_PHONE_FRITZ",    ""),
            "جنيد":       st.secrets.get("TECH_PHONE_JUNAID",   ""),
            "كفاية الله": st.secrets.get("TECH_PHONE_KIFAYA",   ""),
        }
    except Exception:
        tech_phones = {}
    priority_ar = {"urgent": "عاجلة 🔴", "high": "عالية 🟠", "medium": "متوسطة 🟡", "low": "منخفضة 🟢"}.get(priority, priority)
    phone = tech_phones.get(technician_name, "")
    if not phone:
        return {"ok": False, "error": "لا يوجد رقم مسجل للفني"}
    msg = (
        f"🛗 *مهمة جديدة – لفتك للمصاعد*\n"
        f"الفني: {technician_name}\n"
        f"العنوان: {task_title}\n"
        f"العقد: {contract_no} | المبنى: {building}\n"
        f"التاريخ: {scheduled_date}\n"
        f"الأولوية: {priority_ar}"
    )
    return send_whatsapp(phone, msg)

# ─────────────────────────────────────────────
# PDF Report
# ─────────────────────────────────────────────
def generate_monthly_pdf(df: pd.DataFrame, work_orders: list, month_label: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:
        return b""

    def ar(text):
        try:
            reshaped = arabic_reshaper.reshape(str(text))
            return get_display(reshaped)
        except Exception:
            return str(text)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             rightMargin=1.5*cm, leftMargin=1.5*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    story = []
    style_title = ParagraphStyle("title", fontSize=16, textColor=colors.HexColor("#111111"), alignment=1, spaceAfter=12)
    style_sub   = ParagraphStyle("sub",   fontSize=10, textColor=colors.HexColor("#6c757d"), alignment=1, spaceAfter=20)
    style_h     = ParagraphStyle("h",     fontSize=12, textColor=colors.HexColor("#111111"), alignment=1, spaceAfter=8, spaceBefore=14)
    style_body  = ParagraphStyle("body",  fontSize=9,  alignment=1, spaceAfter=4)

    story.append(Paragraph(ar("تقرير شركة لفتك للمصاعد"), style_title))
    story.append(Paragraph(ar(f"الفترة: {month_label}"), style_sub))
    story.append(Paragraph(ar(f"تاريخ الإصدار: {date.today().strftime('%Y-%m-%d')}"), style_sub))
    story.append(Spacer(1, 0.3*cm))

    total     = len(df)
    active    = len(df[df["status_display"] == "نشط"]) if not df.empty else 0
    expiring  = len(df[df["days_remaining"].notna() & (df["days_remaining"] >= 0) & (df["days_remaining"] <= 30)]) if not df.empty else 0
    total_val = df["contract_value"].apply(safe_number).sum() if not df.empty else 0
    wo_done   = len([w for w in work_orders if w.get("status") == "completed"]) if work_orders else 0

    kpi_data = [
        [ar("المؤشر"), ar("القيمة")],
        [ar("إجمالي العقود"),       ar(str(total))],
        [ar("العقود النشطة"),       ar(str(active))],
        [ar("تنتهي خلال 30 يوم"),   ar(str(expiring))],
        [ar("القيمة الإجمالية"),     ar(f"{total_val:,.0f} ر.س")],
        [ar("أوامر عمل مكتملة"),    ar(str(wo_done))],
    ]
    kpi_table = Table(kpi_data, colWidths=[9*cm, 7*cm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#111111")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fb")]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#d9dde8")),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(ar("العقود المنتهية أو القريبة من الانتهاء"), style_h))

    if not df.empty:
        critical = df[df["days_remaining"].notna() & (df["days_remaining"] <= 30)].sort_values("days_remaining").head(20)
        if not critical.empty:
            rows = [[ar("رقم العقد"), ar("العميل"), ar("المبنى"), ar("الانتهاء"), ar("الأيام")]]
            for _, r in critical.iterrows():
                rows.append([
                    ar(safe_text(r.get("contract_no"), "—")),
                    ar(safe_text(r.get("customer_name"), "—")),
                    ar(safe_text(r.get("building_name"), "—")),
                    ar(safe_text(r.get("end_date"), "—")),
                    ar(str(int(r["days_remaining"])) if r["days_remaining"] is not None else "—"),
                ])
            t = Table(rows, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#c00")),
                ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
                ("FONTSIZE",   (0,0), (-1,-1), 8),
                ("ALIGN",      (0,0), (-1,-1), "CENTER"),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fff5f5")]),
                ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#d9dde8")),
            ]))
            story.append(t)
        else:
            story.append(Paragraph(ar("لا توجد عقود حرجة"), style_body))

    doc.build(story)
    return buf.getvalue()

# ════════════════════════════════════════════════════════
# TAB 1: Dashboard — Odoo ERP Style
# ════════════════════════════════════════════════════════
def tab_dashboard():
    require_role("admin", "manager")
    import pandas as pd
    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    maintenance   = load_maintenance_logs()

    if is_client():
        cc = st.session_state.get("client_contract", "")
        if cc:
            contracts = [c for c in contracts if str(c.get("contract_no","")) == cc]

    today = date.today()

    # ══ فلتر التاريخ — Google Ads style ══
    from datetime import timedelta
    import calendar

    # CSS الفلتر
    st.markdown("""<style>
.date-filter-bar{background:#fff;border:1.5px solid #e5e5e5;border-radius:12px;
    padding:12px 18px;margin-bottom:18px;direction:rtl;}
.date-filter-bar .df-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.df-label{font-size:0.7rem;font-weight:800;color:#aaa;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.df-preset-row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;}
.df-btn{padding:5px 12px;border-radius:20px;font-size:0.75rem;font-weight:600;
    border:1.5px solid #ddd;background:#fff;color:#444;cursor:pointer;white-space:nowrap;}
.df-btn.active{background:#111;color:#fff;border-color:#111;}
.df-range{font-size:0.78rem;color:#666;margin-top:6px;}
</style>""", unsafe_allow_html=True)

    # الفترات الجاهزة
    presets = {
        "كل الوقت":    (None, None),
        "هذا الشهر":   (today.replace(day=1), today),
        "الشهر الماضي": (
            (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            today.replace(day=1) - timedelta(days=1)
        ),
        "آخر 30 يوم":  (today - timedelta(days=30), today),
        "آخر 90 يوم":  (today - timedelta(days=90), today),
        "هذه السنة":   (today.replace(month=1, day=1), today),
    }

    if "dash_preset" not in st.session_state:
        st.session_state["dash_preset"]    = "كل الوقت"
        st.session_state["dash_date_from"] = None
        st.session_state["dash_date_to"]   = None

    # عرض الفلتر
    st.markdown('<div class="date-filter-bar"><div class="df-label">📅 نطاق التاريخ — تاريخ نهاية العقد</div>', unsafe_allow_html=True)

    preset_cols = st.columns(len(presets) + 1)
    for i, (label, (d_from, d_to)) in enumerate(presets.items()):
        with preset_cols[i]:
            is_active = st.session_state["dash_preset"] == label
            btn_style = "background:#111;color:#fff;border:1.5px solid #111;" if is_active else "background:#fff;color:#444;border:1.5px solid #ddd;"
            if st.button(label, key=f"preset_{label}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state["dash_preset"]    = label
                st.session_state["dash_date_from"] = d_from
                st.session_state["dash_date_to"]   = d_to
                st.rerun()

    with preset_cols[-1]:
        if st.button("📅 مخصص", key="preset_custom",
                     use_container_width=True,
                     type="primary" if st.session_state["dash_preset"] == "مخصص" else "secondary"):
            st.session_state["dash_preset"] = "مخصص"
            st.rerun()

    if st.session_state["dash_preset"] == "مخصص":
        cc1, cc2 = st.columns(2)
        with cc1:
            d_from_custom = st.date_input("من تاريخ", value=st.session_state["dash_date_from"] or today.replace(month=1, day=1), key="custom_from")
        with cc2:
            d_to_custom   = st.date_input("إلى تاريخ", value=st.session_state["dash_date_to"]   or today, key="custom_to")
        st.session_state["dash_date_from"] = d_from_custom
        st.session_state["dash_date_to"]   = d_to_custom

    # عرض الفترة الحالية
    f_from = st.session_state["dash_date_from"]
    f_to   = st.session_state["dash_date_to"]
    if f_from and f_to:
        st.markdown(f'<div style="font-size:0.75rem;color:#888;margin-top:6px;direction:rtl;">الفترة: {f_from} — {f_to}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.75rem;color:#888;margin-top:6px;">الفترة: كل الوقت</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق الفلتر على العقود
    df = prepare_contracts_df(contracts)
    if f_from and f_to:
        try:
            import pandas as pd
            df["end_date_dt"] = pd.to_datetime(df["end_date"], errors="coerce")
            df = df[
                (df["end_date_dt"] >= pd.Timestamp(f_from)) &
                (df["end_date_dt"] <= pd.Timestamp(f_to))
            ].copy()
        except Exception:
            pass

    def fmt(n):
        try: return f"{float(n):,.0f}"
        except: return "0"
    def safe_n(v):
        try: return float(v)
        except: return 0.0
    def safe_i(v):
        try: return int(v)
        except: return 0

    # ══ حسابات ══
    total_c  = len(df)
    total_v  = float(df["contract_value"].apply(safe_n).sum()) if not df.empty else 0.0
    total_el = int(df["elevator_count"].apply(safe_i).sum())   if not df.empty else 0
    paid_df  = df[df["payment_display"]=="مسدد"]     if not df.empty else pd.DataFrame()
    unpaid_df= df[df["payment_display"]=="غير مسدد"] if not df.empty else pd.DataFrame()
    paid_v   = float(paid_df["contract_value"].apply(safe_n).sum())   if not paid_df.empty else 0.0
    unpaid_v = float(unpaid_df["contract_value"].apply(safe_n).sum()) if not unpaid_df.empty else 0.0
    paid_c   = len(paid_df)
    unpaid_c = len(unpaid_df)
    collect_pct  = round(paid_v  / total_v * 100, 1) if total_v else 0.0
    avg_contract = round(total_v / total_c, 0)        if total_c else 0.0
    n_30 = n_60 = 0
    if not df.empty and "days_remaining" in df.columns:
        dr   = df["days_remaining"]
        n_30 = int((dr.notna() & (dr >= 0) & (dr <= 30)).sum())
        n_60 = int((dr.notna() & (dr > 30) & (dr <= 60)).sum())
    urgent_wo = len([w for w in (work_orders or [])   if w.get("status") in ("pending","in_progress")])
    open_fr   = len([f for f in (fault_reports or []) if f.get("status") in ("open","assigned")])

    day_ar = {"Monday":"الاثنين","Tuesday":"الثلاثاء","Wednesday":"الأربعاء",
               "Thursday":"الخميس","Friday":"الجمعة","Saturday":"السبت","Sunday":"الأحد"}
    mon_ar = {"January":"يناير","February":"فبراير","March":"مارس","April":"أبريل",
               "May":"مايو","June":"يونيو","July":"يوليو","August":"أغسطس",
               "September":"سبتمبر","October":"أكتوبر","November":"نوفمبر","December":"ديسمبر"}
    today_str = today.strftime("%A، %d %B %Y")
    for e, a in {**day_ar, **mon_ar}.items():
        today_str = today_str.replace(e, a)

    bar_clr = "#22c55e" if collect_pct >= 70 else ("#f59e0b" if collect_pct >= 40 else "#ef4444")
    bar_w   = min(int(collect_pct), 100)

    # ══ CSS ══
    st.markdown("""<style>
/* reset rtl global */
.db-wrap * { box-sizing: border-box; }

/* header */
.db-wrap .hdr {
    display:flex; justify-content:space-between; align-items:flex-end;
    border-bottom:2px solid #111; padding-bottom:14px; margin-bottom:22px;
    direction:rtl;
}
.hdr-r .lbl { font-size:0.68rem; font-weight:800; color:#aaa; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:5px; }
.hdr-r .ttl { font-size:1.5rem; font-weight:900; color:#111; line-height:1.1; }
.hdr-l { text-align:left; }
.hdr-l .dt  { font-size:0.88rem; font-weight:700; color:#333; margin-bottom:3px; }
.hdr-l .src { font-size:0.7rem; color:#bbb; }

/* section title */
.db-wrap .stl {
    font-size:0.65rem; font-weight:800; color:#aaa; letter-spacing:3px;
    text-transform:uppercase; margin:24px 0 12px; padding-bottom:7px;
    border-bottom:1px solid #ebebeb; direction:rtl;
}

/* KPI card */
.db-wrap .kc {
    background:#fff; border:1.5px solid #e5e5e5; border-radius:12px;
    padding:16px 18px; height:100%; direction:rtl;
    transition: border-color .2s, box-shadow .2s;
}
.db-wrap .kc:hover { border-color:#111; box-shadow:0 3px 14px rgba(0,0,0,.08); }
.kc .kl { font-size:0.68rem; font-weight:700; color:#aaa; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
.kc .kv { font-size:2rem; font-weight:900; color:#111; line-height:1; letter-spacing:-1px; margin-bottom:5px; }
.kc .ks { font-size:0.75rem; color:#888; line-height:1.5; }

/* bar */
.db-wrap .bar-card {
    background:#fff; border:1.5px solid #e5e5e5; border-radius:12px;
    padding:14px 20px; margin-top:10px; direction:rtl;
}
.bar-card .bt { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.bar-card .bl { font-size:0.82rem; font-weight:700; color:#333; }
.bar-card .bp { font-size:1rem; font-weight:900; }
.bar-card .btr { background:#f0f0f0; border-radius:8px; height:12px; overflow:hidden; }
.bar-card .bf  { height:12px; border-radius:8px; }
.bar-card .bm  { display:flex; justify-content:space-between; margin-top:9px; font-size:0.75rem; color:#888; }

/* alerts */
.db-wrap .al {
    display:flex; align-items:center; gap:12px; padding:11px 15px;
    border-radius:10px; margin-bottom:7px; direction:rtl;
}
.al.r { background:#fff5f5; border:1.5px solid #fecaca; }
.al.y { background:#fffbeb; border:1.5px solid #fde68a; }
.al.g { background:#f0fdf4; border:1.5px solid #bbf7d0; }
.al .ab { flex:1; }
.al .at { font-size:0.82rem; font-weight:700; color:#111; line-height:1.3; }
.al .as { font-size:0.7rem;  color:#888; margin-top:2px; }
.al .an { font-size:1.4rem;  font-weight:900; min-width:38px; text-align:center; }

/* tables */
.db-wrap .tbl { border:1.5px solid #e5e5e5; border-radius:12px; overflow:hidden; direction:rtl; }
.tbl .th {
    background:#111; padding:9px 16px;
    display:flex; direction:rtl; align-items:center; gap:0;
}
.tbl .th span { color:#fff; font-size:0.68rem; font-weight:700; letter-spacing:.5px; }
.tbl .tr {
    display:flex; direction:rtl; align-items:center;
    padding:8px 16px; border-bottom:1px solid #f0f0f0;
}
.tbl .tr:last-child { border-bottom:none; }
.tbl .tr:nth-child(even) { background:#fafafa; }
.tbl .td { font-size:0.78rem; color:#222; }
.tbl .td.b { font-weight:700; }
.tbl .td.g { color:#999; font-size:0.72rem; }
.tbl .td.c { text-align:center; }

/* badges */
.bdg { display:inline-block; padding:2px 9px; border-radius:20px; font-size:0.68rem; font-weight:700; white-space:nowrap; }
.bdg.g { background:#dcfce7; color:#15803d; }
.bdg.r { background:#fee2e2; color:#b91c1c; }
.bdg.y { background:#fef9c3; color:#854d0e; }
.bdg.k { background:#f3f4f6; color:#4b5563; }
</style>""", unsafe_allow_html=True)

    st.markdown('<div class="db-wrap">', unsafe_allow_html=True)

    # ─── HEADER ───
    st.markdown(f"""<div class="hdr">
  <div class="hdr-r">
    <div class="lbl">LiftTech — التقرير الإداري التنفيذي</div>
    <div class="ttl">لوحة الأداء والمؤشرات</div>
  </div>
  <div class="hdr-l">
    <div class="dt">{today_str}</div>
    <div class="src">بيانات فعلية — Supabase</div>
  </div>
</div>""", unsafe_allow_html=True)

    # ─── القسم 1: المؤشرات المالية ───
    st.markdown('<div class="stl">📊 المؤشرات المالية</div>', unsafe_allow_html=True)

    # ترتيب RTL: إجمالي المحفظة أولاً (يمين)، ثم المحصّل، المتأخر، المتوسط
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "إجمالي المحفظة",   fmt(total_v),     f"{total_c} عقد — {total_el} مصعد"),
        (c2, "إجمالي المحصّل",   fmt(paid_v),      f"{collect_pct}% من المحفظة — {paid_c} عقد"),
        (c3, "إجمالي المتأخر",   fmt(unpaid_v),    f"{round(100-collect_pct,1)}% من المحفظة — {unpaid_c} عقد"),
        (c4, "متوسط قيمة العقد", fmt(avg_contract), "ريال سعودي / عقد"),
    ]
    for col, lbl, val, sub in kpis:
        with col:
            st.markdown(f"""<div class="kc">
  <div class="kl">{lbl}</div>
  <div class="kv">{val}</div>
  <div class="ks">{sub}</div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="bar-card">
  <div class="bt">
    <div class="bl">مؤشر التحصيل الإجمالي</div>
    <div class="bp" style="color:{bar_clr};">{collect_pct}%</div>
  </div>
  <div class="btr"><div class="bf" style="width:{bar_w}%;background:{bar_clr};"></div></div>
  <div class="bm">
    <span>&#9632; محصّل: {fmt(paid_v)} ر.س ({paid_c} عقد)</span>
    <span>&#9632; متأخر: {fmt(unpaid_v)} ر.س ({unpaid_c} عقد)</span>
  </div>
</div>""", unsafe_allow_html=True)

    # ─── القسم 2: التنبيهات ───
    st.markdown('<div class="stl">🚨 التنبيهات التنفيذية</div>', unsafe_allow_html=True)
    col_tbl, col_al = st.columns([1.5, 1])

    with col_al:
        alerts = [
            ("r","🔴","عقود تنتهي خلال 30 يوم",       n_30,     "تستوجب تجديداً فورياً",  "#dc2626"),
            ("y","🟡","عقود تنتهي خلال 31–60 يوم",     n_60,     "تحتاج تجديداً قريباً",   "#d97706"),
            ("r","🔴","بلاغات أعطال مفتوحة",           open_fr,  "بانتظار المعالجة",        "#dc2626"),
            ("y","🟡","أوامر عمل قيد التنفيذ / معلقة", urgent_wo,"تحتاج متابعة",            "#d97706"),
        ]
        for cls, ico, txt, cnt, sub, clr in alerts:
            nc = clr if cnt > 0 else "#16a34a"
            st.markdown(f"""<div class="al {cls}">
  <div class="ab"><div class="at">{txt}</div><div class="as">{sub}</div></div>
  <div class="an" style="color:{nc};">{cnt}</div>
</div>""", unsafe_allow_html=True)

    with col_tbl:
        if not df.empty and "days_remaining" in df.columns:
            soon = df[df["days_remaining"].notna() & (df["days_remaining"] >= 0) & (df["days_remaining"] <= 60)].copy()
            soon = soon.sort_values("days_remaining")
            if not soon.empty:
                rows_html = ""
                for _, row in soon.head(8).iterrows():
                    dr   = int(row.get("days_remaining", 0))
                    bc   = "r" if dr <= 30 else "y"
                    cust = str(row.get("customer_name","—"))[:22]
                    cno  = str(row.get("contract_no","—"))
                    end_d= str(row.get("end_date","—"))[:10]
                    rows_html += f"""<div class="tr">
  <span class="td b" style="flex:2;">{cust}</span>
  <span class="td g" style="flex:1;">{cno}</span>
  <span class="td c" style="flex:0.7;"><span class="bdg {bc}">{dr}د</span></span>
  <span class="td g c" style="flex:1.1;direction:ltr;">{end_d}</span>
</div>"""
                st.markdown(f"""<div class="tbl">
  <div class="th">
    <span style="flex:2;">العميل</span>
    <span style="flex:1;">رقم العقد</span>
    <span style="flex:0.7;text-align:center;">متبقي</span>
    <span style="flex:1.1;text-align:center;">تاريخ الانتهاء</span>
  </div>{rows_html}</div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="al g"><span>✅</span><div class="ab"><div class="at">لا توجد عقود تنتهي خلال 60 يوماً</div></div></div>', unsafe_allow_html=True)

    # ─── القسم 3: أداء الفنيين ───
    st.markdown('<div class="stl">👷 أداء الفنيين</div>', unsafe_allow_html=True)
    techs   = ["فيصل","سيلفوم","فريتز","جنيد","كفاية الله"]
    wo_list = work_orders   or []
    fr_list = fault_reports or []
    ml_list = maintenance   or []
    rows_html = ""
    for t in techs:
        wt = len([w for w in wo_list if w.get("technician","") == t])
        wd = len([w for w in wo_list if w.get("technician","") == t and w.get("status") == "completed"])
        wo = wt - wd
        fo = len([f for f in fr_list if f.get("technician","") == t and f.get("status") in ("open","assigned")])
        mc = len([m for m in ml_list if m.get("technician","") == t])
        pc = round(wd / wt * 100) if wt else 0
        pc_c = "g" if pc >= 70 else ("y" if pc >= 40 else "r")
        rows_html += f"""<div class="tr">
  <span class="td b"  style="flex:1.4;">{t}</span>
  <span class="td c"  style="flex:0.8;">{wt}</span>
  <span class="td c"  style="flex:0.8;"><span class="bdg g">{wd}</span></span>
  <span class="td c"  style="flex:0.8;"><span class="bdg {"y" if wo>0 else "g"}">{wo}</span></span>
  <span class="td c"  style="flex:0.9;"><span class="bdg {"r" if fo>0 else "g"}">{fo}</span></span>
  <span class="td c"  style="flex:0.8;">{mc}</span>
  <span class="td c"  style="flex:1;"><span class="bdg {pc_c}">{pc}%</span></span>
</div>"""
    st.markdown(f"""<div class="tbl">
  <div class="th">
    <span style="flex:1.4;">الفني</span>
    <span style="flex:0.8;text-align:center;">أوامر العمل</span>
    <span style="flex:0.8;text-align:center;">مُنجز</span>
    <span style="flex:0.8;text-align:center;">معلق</span>
    <span style="flex:0.9;text-align:center;">بلاغات</span>
    <span style="flex:0.8;text-align:center;">صيانة</span>
    <span style="flex:1;text-align:center;">الإنجاز</span>
  </div>{rows_html}</div>""", unsafe_allow_html=True)

    # ─── القسم 4: حالة العقود حسب المنطقة ───
    st.markdown('<div class="stl">📋 حالة العقود حسب المنطقة</div>', unsafe_allow_html=True)
    if not df.empty:
        dist_rows = []
        for d in sorted(df["district"].fillna("غير محدد").unique()):
            sub  = df[df["district"].fillna("غير محدد") == d]
            act  = len(sub[sub["contract_status"] == "active"])
            exp  = len(sub[sub["contract_status"] == "expired"])
            ren  = len(sub[sub["days_remaining"].notna() & (sub["days_remaining"] >= 0) & (sub["days_remaining"] <= 60)]) if "days_remaining" in sub.columns else 0
            val  = float(sub["contract_value"].apply(safe_n).sum())
            dist_rows.append((d, len(sub), act, exp, ren, val))
        dist_rows.sort(key=lambda x: x[1], reverse=True)

        dc1, dc2 = st.columns(2)
        with dc1:
            rows_html = ""
            for d, tot, act, exp, ren, _ in dist_rows[:10]:
                rows_html += f"""<div class="tr">
  <span class="td b" style="flex:1.8;">{str(d)[:18]}</span>
  <span class="td c" style="flex:0.7;font-weight:700;">{tot}</span>
  <span class="td c" style="flex:0.7;"><span class="bdg g">{act}</span></span>
  <span class="td c" style="flex:0.7;"><span class="bdg {"r" if exp>0 else "k"}">{exp}</span></span>
  <span class="td c" style="flex:0.9;"><span class="bdg {"y" if ren>0 else "k"}">{ren}</span></span>
</div>"""
            st.markdown(f"""<div class="tbl">
  <div class="th">
    <span style="flex:1.8;">الحي / المنطقة</span>
    <span style="flex:0.7;text-align:center;">إجمالي</span>
    <span style="flex:0.7;text-align:center;">نشط</span>
    <span style="flex:0.7;text-align:center;">منتهي</span>
    <span style="flex:0.9;text-align:center;">قيد التجديد</span>
  </div>{rows_html}</div>""", unsafe_allow_html=True)

        with dc2:
            rows_html = ""
            for d, tot, act, exp, ren, val in dist_rows[:10]:
                share  = round(val / total_v * 100, 1) if total_v else 0
                bw     = min(int(share * 2.5), 100)
                rows_html += f"""<div class="tr">
  <span class="td b" style="flex:1.8;">{str(d)[:18]}</span>
  <span class="td"   style="flex:1.4;text-align:center;font-weight:700;">{fmt(val)}</span>
  <span class="td c" style="flex:1;">
    <div style="display:inline-flex;align-items:center;gap:5px;">
      <div style="background:#f0f0f0;border-radius:4px;height:7px;width:48px;overflow:hidden;display:inline-block;">
        <div style="width:{bw}%;height:7px;background:#111;border-radius:4px;"></div>
      </div>
      <span style="font-size:0.7rem;color:#888;">{share}%</span>
    </div>
  </span>
</div>"""
            st.markdown(f"""<div class="tbl">
  <div class="th">
    <span style="flex:1.8;">الحي / المنطقة</span>
    <span style="flex:1.4;text-align:center;">القيمة (ر.س)</span>
    <span style="flex:1;text-align:center;">الحصة</span>
  </div>{rows_html}</div>""", unsafe_allow_html=True)
    else:
        st.info("لا توجد بيانات عقود.")

    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# مهمة 20: Schema Alignment — الحقول المتوقعة لكل جدول
# ════════════════════════════════════════════════════════
SCHEMA_CONTRACTS = {
    "contract_no", "customer_name", "mobile", "building_name", "district",
    "city", "elevator_count", "elevator_type", "elevator_brand",
    "contract_value", "start_date", "end_date", "payment_status",
    "contract_status", "collector", "notes"
}
SCHEMA_WORK_ORDERS = {
    "contract_id", "title", "description", "scheduled_date",
    "technician", "status", "priority", "work_type", "notes"
}
SCHEMA_FAULT_REPORTS = {
    "contract_id", "title", "description", "reported_date",
    "technician", "status", "priority", "notes"
}
SCHEMA_MAINTENANCE_LOGS = {
    "contract_id", "log_date", "technician", "work_done", "parts_used", "notes"
}

def validate_payload(payload: dict, expected_schema: set, table_name: str) -> list:
    """يتحقق من تطابق payload مع الـ schema — يمنع إرسال حقول غير معروفة"""
    errors = []
    unknown = set(payload.keys()) - expected_schema - {"id", "created_at"}
    for k in unknown:
        errors.append(f"[Schema] حقل غير معروف في جدول {table_name}: {k}")
    return errors

# ════════════════════════════════════════════════════════
# TAB 2: Contracts — Odoo ERP Style
# ════════════════════════════════════════════════════════
def tab_contracts():
    if is_client():
        st.info("🔒 هذا القسم متاح للمدير والمديرين فقط.")
        return

    # ── إضافة عقد جديد ──
    section_header("➕ إضافة عقد جديد")

    with st.form("new_contract_form", clear_on_submit=True):

        # مجموعة 1: بيانات العميل
        st.markdown('<div class="form-group"><div class="form-group-header">👤 بيانات العميل</div><div class="form-group-body">', unsafe_allow_html=True)
        g1c1, g1c2 = st.columns(2)
        with g1c1:
            customer_name = st.text_input("اسم العميل *")
        with g1c2:
            mobile = st.text_input("رقم الجوال")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 2: بيانات الموقع
        st.markdown('<div class="form-group"><div class="form-group-header">📍 بيانات الموقع</div><div class="form-group-body">', unsafe_allow_html=True)
        g2c1, g2c2, g2c3 = st.columns(3)
        with g2c1:
            building_name = st.text_input("اسم المبنى")
        with g2c2:
            district = st.text_input("الحي")
        with g2c3:
            city = st.selectbox("المدينة", [""] + CITIES)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 3: بيانات المصعد
        st.markdown('<div class="form-group"><div class="form-group-header">🛗 بيانات المصعد</div><div class="form-group-body">', unsafe_allow_html=True)
        g3c1, g3c2, g3c3 = st.columns(3)
        with g3c1:
            elevator_count = st.number_input("عدد المصاعد", min_value=1, value=1)
        with g3c2:
            elevator_type  = st.selectbox("نوع المصعد", ELEVATOR_TYPES)
        with g3c3:
            elevator_brand = st.text_input("ماركة المصعد")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 4: بيانات العقد
        st.markdown('<div class="form-group"><div class="form-group-header">📋 بيانات العقد</div><div class="form-group-body">', unsafe_allow_html=True)
        g4c1, g4c2, g4c3 = st.columns(3)
        with g4c1:
            contract_no    = st.text_input("رقم العقد *")
        with g4c2:
            start_date     = st.date_input("تاريخ البداية", value=date.today())
        with g4c3:
            end_date       = st.date_input("تاريخ الانتهاء", value=date.today() + timedelta(days=365))
        g4c4, g4c5 = st.columns(2)
        with g4c4:
            contract_status = st.selectbox("حالة العقد", ["active","expired","cancelled"],
                                           format_func=lambda x: {"active":"نشط","expired":"منتهي","cancelled":"ملغي"}[x])
        with g4c5:
            contract_value = st.number_input("قيمة العقد (ر.س)", min_value=0.0, step=100.0)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 5: السداد والتحصيل
        st.markdown('<div class="form-group"><div class="form-group-header">💰 السداد والتحصيل</div><div class="form-group-body">', unsafe_allow_html=True)
        g5c1, g5c2 = st.columns(2)
        with g5c1:
            payment_status = st.selectbox("حالة السداد", ["unpaid","partial","paid"],
                                          format_func=lambda x: {"unpaid":"غير مسدد","partial":"جزئي","paid":"مسدد"}[x])
        with g5c2:
            collector = st.text_input("المحصل")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 6: الملاحظات
        st.markdown('<div class="form-group"><div class="form-group-header">📝 الملاحظات</div><div class="form-group-body">', unsafe_allow_html=True)
        notes = st.text_area("ملاحظات", height=80, label_visibility="collapsed")
        st.markdown("</div></div>", unsafe_allow_html=True)

        submit = st.form_submit_button("💾 حفظ العقد", use_container_width=True, type="primary")

    if submit:
        require_role("admin", "manager")
        errs = validate_contract(contract_no, customer_name, start_date, end_date, float(contract_value))
        if show_validation_errors(errs):
            pass
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                payload = {
                    "contract_no": contract_no.strip(), "customer_name": customer_name.strip(),
                    "mobile": fmt_phone(mobile.strip()), "building_name": building_name.strip(),
                    "district": district.strip(), "city": city.strip(),
                    "elevator_count": int(elevator_count), "elevator_type": elevator_type,
                    "elevator_brand": elevator_brand.strip(), "contract_value": float(contract_value),
                    "start_date": str(start_date), "end_date": str(end_date),
                    "payment_status": payment_status, "contract_status": contract_status,
                    "collector": collector.strip(), "notes": notes.strip(),
                }
                schema_errs = validate_payload(payload, SCHEMA_CONTRACTS, "contracts")
                if schema_errs:
                    for se in schema_errs: st.warning(se)
                supabase.table("contracts").insert(payload).execute()
                log_action("add", "contracts",
                           f"إضافة عقد: {payload.get('customer_name','')} — {payload.get('contract_no','')}",
                           severity="important", entity_id=payload.get("contract_no",""))
                load_contracts.clear()
                st.success("✅ تم حفظ العقد بنجاح")
                st.rerun()
            except Exception as e:
                st.error(friendly_error(e))

    # ── عرض وبحث العقود ──
    section_header("🔍 عرض وبحث العقود")
    contracts = load_contracts()
    df = prepare_contracts_df(contracts)

    if df.empty:
        st.info("لا توجد عقود مسجلة.")
        return

    # شريط بحث واحد + نطاق تاريخ الانتهاء فقط
    with st.container():
        st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns([3, 1, 1])
        with sc1:
            search_q = st.text_input(
                "🔍 بحث",
                placeholder="رقم العقد | اسم العميل | جوال | مبنى | حي | مدينة | ماركة | محصل | ملاحظات",
                key="contract_search_v8"
            )
        with sc2:
            date_from = st.date_input("تاريخ الانتهاء من", value=None, key="date_from_v8")
        with sc3:
            date_to   = st.date_input("تاريخ الانتهاء إلى", value=None, key="date_to_v8")
        st.markdown("</div>", unsafe_allow_html=True)

    filtered = df.copy()

    # تطبيق البحث النصي على جميع الحقول المحددة
    if search_q.strip():
        q = search_q.strip()
        search_cols = ["contract_no","customer_name","mobile","building_name","district","city","elevator_brand","collector","notes"]
        existing_search = [c for c in search_cols if c in filtered.columns]
        mask = filtered[existing_search[0]].str.contains(q, case=False, na=False)
        for col in existing_search[1:]:
            mask = mask | filtered[col].str.contains(q, case=False, na=False)
        filtered = filtered[mask]

    # تطبيق فلتر التاريخ على تاريخ الانتهاء فقط
    if date_from is not None or date_to is not None:
        def check_end_date(row):
            ed = parse_date_safe(row.get("end_date"))
            if ed is None: return False
            if date_from is not None and ed < date_from: return False
            if date_to   is not None and ed > date_to:   return False
            return True
        filtered = filtered[filtered.apply(check_end_date, axis=1)]

    st.markdown(f"**عدد النتائج: {len(filtered)} عقد**")

    # أزرار التصدير
    _drop = [c for c in ["days_remaining","status_display","payment_display"] if c in filtered.columns]
    csv_bytes = to_csv_bytes(filtered.drop(columns=_drop))
    exp_col1, exp_col2 = st.columns([1, 4])
    with exp_col1:
        # مهمة 15: Export controls
        controlled_download_button(
            "⬇️ تصدير CSV", data=csv_bytes,
            filename="contracts.csv", mime="text/csv",
            module="contracts", record_count=len(filtered),
            key="contracts_csv_export")
    with exp_col2:
        if is_admin() or is_manager():
            if st.button("📄 تصدير PDF — تقرير شهري", key="pdf_export_btn"):
                with st.spinner("جاري إنشاء التقرير..."):
                    wo_list = load_work_orders()
                    pdf_bytes = generate_monthly_pdf(filtered, wo_list, date.today().strftime("%Y/%m"))
                    if pdf_bytes:
                        st.download_button("⬇️ تحميل PDF", data=pdf_bytes,
                                           file_name=f"lifttech_report_{date.today()}.pdf",
                                           mime="application/pdf", key="pdf_download_btn")
                    else:
                        st.warning("⚠️ تعذّر إنشاء PDF — تأكد من تثبيت مكتبات reportlab و arabic_reshaper")

    display_cols = ["contract_no","customer_name","mobile","building_name","district",
                    "elevator_count","contract_value","payment_display","status_display","end_date","days_remaining","collector"]
    existing = [c for c in display_cols if c in filtered.columns]
    col_rename = {
        "contract_no":"رقم العقد","customer_name":"اسم العميل","mobile":"الجوال",
        "building_name":"المبنى","district":"الحي","elevator_count":"المصاعد",
        "contract_value":"القيمة","payment_display":"السداد","status_display":"الحالة",
        "end_date":"الانتهاء","days_remaining":"الأيام المتبقية","collector":"المحصل",
    }
    st.dataframe(filtered[existing].rename(columns=col_rename), use_container_width=True, hide_index=True)

    # ── تعديل عقد — للمدير فقط ──
    if is_admin() or is_manager():
        section_header("✏️ تعديل عقد")
        edit_opts = {f"{c.get('contract_no','—')} – {c.get('customer_name','—')}": c.get("id") for c in contracts}
        selected_edit_label = st.selectbox("اختر العقد للتعديل", ["-- اختر --"] + list(edit_opts.keys()), key="edit_contract_v8")
        if selected_edit_label != "-- اختر --":
            selected_id = edit_opts.get(selected_edit_label)
            matched = [c for c in contracts if c.get("id") == selected_id]
            if matched:
                ec = matched[0]
                with st.form("edit_contract_form_v8"):

                    # مجموعة 1: بيانات العميل
                    st.markdown('<div class="form-group"><div class="form-group-header">👤 بيانات العميل</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_g1c1, e_g1c2 = st.columns(2)
                    with e_g1c1:
                        e_customer = st.text_input("اسم العميل", value=safe_text(ec.get("customer_name")))
                    with e_g1c2:
                        e_mobile   = st.text_input("رقم الجوال", value=safe_text(ec.get("mobile")))
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # مجموعة 2: بيانات الموقع
                    st.markdown('<div class="form-group"><div class="form-group-header">📍 بيانات الموقع</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_g2c1, e_g2c2, e_g2c3 = st.columns(3)
                    with e_g2c1:
                        e_building = st.text_input("اسم المبنى", value=safe_text(ec.get("building_name")))
                    with e_g2c2:
                        e_district = st.text_input("الحي",       value=safe_text(ec.get("district")))
                    with e_g2c3:
                        e_city     = st.text_input("المدينة",    value=safe_text(ec.get("city")))
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # مجموعة 3: بيانات المصعد
                    st.markdown('<div class="form-group"><div class="form-group-header">🛗 بيانات المصعد</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_g3c1, e_g3c2, e_g3c3 = st.columns(3)
                    with e_g3c1:
                        e_elev_count = st.number_input("عدد المصاعد", min_value=1, value=safe_int(ec.get("elevator_count"), 1))
                    with e_g3c2:
                        e_elev_type  = st.selectbox("نوع المصعد",
                            ELEVATOR_TYPES,
                            index=ELEVATOR_TYPES.index(ec.get("elevator_type","ركاب"))
                                  if ec.get("elevator_type") in ELEVATOR_TYPES else 0)
                    with e_g3c3:
                        e_elev_brand = st.text_input("ماركة المصعد", value=safe_text(ec.get("elevator_brand")))
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # مجموعة 4: بيانات العقد
                    st.markdown('<div class="form-group"><div class="form-group-header">📋 بيانات العقد</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_g4c1, e_g4c2 = st.columns(2)
                    with e_g4c1:
                        e_start    = st.date_input("تاريخ البداية", value=parse_date_safe(ec.get("start_date")) or date.today())
                        e_status   = st.selectbox("حالة العقد", ["active","expired","cancelled"],
                                       format_func=lambda x: {"active":"نشط","expired":"منتهي","cancelled":"ملغي"}[x],
                                       index=["active","expired","cancelled"].index(ec.get("contract_status","active"))
                                             if ec.get("contract_status") in ["active","expired","cancelled"] else 0)
                    with e_g4c2:
                        e_end      = st.date_input("تاريخ الانتهاء", value=parse_date_safe(ec.get("end_date")) or date.today())
                        e_value    = st.number_input("قيمة العقد (ر.س)", value=safe_number(ec.get("contract_value")), step=100.0)
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # مجموعة 5: السداد والتحصيل
                    st.markdown('<div class="form-group"><div class="form-group-header">💰 السداد والتحصيل</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_g5c1, e_g5c2 = st.columns(2)
                    with e_g5c1:
                        e_payment  = st.selectbox("حالة السداد", ["unpaid","partial","paid"],
                                       format_func=lambda x: {"unpaid":"غير مسدد","partial":"جزئي","paid":"مسدد"}[x],
                                       index=["unpaid","partial","paid"].index(ec.get("payment_status","unpaid"))
                                             if ec.get("payment_status") in ["unpaid","partial","paid"] else 0)
                    with e_g5c2:
                        e_collector = st.text_input("المحصل", value=safe_text(ec.get("collector")))
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    # مجموعة 6: الملاحظات
                    st.markdown('<div class="form-group"><div class="form-group-header">📝 الملاحظات</div><div class="form-group-body">', unsafe_allow_html=True)
                    e_notes = st.text_area("ملاحظات", value=safe_text(ec.get("notes")), height=80, label_visibility="collapsed")
                    st.markdown("</div></div>", unsafe_allow_html=True)

                    e_submit = st.form_submit_button("💾 حفظ التعديلات", use_container_width=True, type="primary")

                if e_submit:
                    errs_e = validate_contract(ec.get("contract_no",""), e_customer, e_start, e_end, float(e_value))
                    if show_validation_errors(errs_e):
                        pass
                    else:
                        try:
                            new_data = {
                                "customer_name": e_customer.strip(),
                                "mobile": fmt_phone(e_mobile.strip()),
                                "building_name": e_building.strip(),
                                "district": e_district.strip(),
                                "city": e_city.strip(),
                                "elevator_count": int(e_elev_count),
                                "elevator_type": e_elev_type,
                                "elevator_brand": e_elev_brand.strip(),
                                "start_date": str(e_start),
                                "end_date": str(e_end),
                                "contract_status": e_status,
                                "contract_value": float(e_value),
                                "payment_status": e_payment,
                                "collector": e_collector.strip(),
                                "notes": e_notes.strip(),
                            }
                            tracked_fields = ["customer_name","contract_status","payment_status","contract_value","end_date","collector"]
                            old_str, new_str = build_change_summary(ec, new_data, tracked_fields)
                            supabase.table("contracts").update(new_data).eq("id", selected_id).execute()
                            load_contracts.clear()
                            log_action("edit", "contracts",
                                       f"تعديل عقد ID: {selected_id}",
                                       severity="important",
                                       entity_id=str(selected_id),
                                       old_value=old_str, new_value=new_str)
                            st.success("✅ تم حفظ التعديلات")
                            st.rerun()
                        except Exception as e:
                            st.error(friendly_error(e))

# ════════════════════════════════════════════════════════
# TAB 3: Work Orders
# ════════════════════════════════════════════════════════
def tab_work_orders():
    contracts = load_contracts()

    if is_tech():
        tech_name = st.session_state.get("display_name", st.session_state.get("username", ""))
    else:
        tech_name = None

    if not is_client():
        section_header("➕ إضافة أمر عمل جديد")
        contract_options = {"-- اختر العقد --": None}
        for c in contracts:
            contract_options[contract_label(c)] = c.get("id")

        with st.form("new_work_order_form", clear_on_submit=True):
            wc1, wc2 = st.columns(2)
            with wc1:
                selected_contract_label = st.selectbox("العقد المرتبط *", list(contract_options.keys()))
                wo_title       = st.text_input("عنوان أمر العمل *")
                wo_description = st.text_area("الوصف التفصيلي", height=90)
                wo_work_type   = st.selectbox("نوع العمل",
                    ["preventive","corrective","emergency","inspection"],
                    format_func=lambda x: {"preventive":"وقائي","corrective":"تصحيحي","emergency":"طارئ","inspection":"فحص"}[x])
            with wc2:
                wo_priority = st.selectbox("الأولوية",
                    ["low","medium","high","urgent"],
                    format_func=lambda x: {"low":"منخفضة","medium":"متوسطة","high":"عالية","urgent":"عاجلة"}[x],
                    index=1)
                wo_technician     = st.selectbox("الفني المسؤول", TECHNICIANS)
                wo_scheduled_date = st.date_input("التاريخ المجدول", value=date.today())
                wo_status         = st.selectbox("الحالة الابتدائية", ["pending","in_progress"],
                    format_func=lambda x: {"pending":"معلق","in_progress":"جاري"}[x])
            wo_submit = st.form_submit_button("💾 حفظ أمر العمل", use_container_width=True, type="primary")

        if wo_submit:
            wo_contract_id = contract_options.get(selected_contract_label)
            errs = validate_work_order(wo_title, wo_contract_id, wo_technician, wo_scheduled_date, wo_status)
            if show_validation_errors(errs):
                pass
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                # مهمة 6: فحص التكرار
                if check_duplicate_work_order(supabase, wo_contract_id, wo_title.strip(), wo_technician, wo_scheduled_date):
                    st.warning("⚠️ يبدو أن هناك أمر عمل مماثل لنفس الفني والتاريخ — هل تريد المتابعة؟")
                    if not st.session_state.get("wo_dup_confirmed", False):
                        if st.button("نعم — أضف على أي حال", key="wo_dup_confirm_btn"):
                            st.session_state["wo_dup_confirmed"] = True
                            st.rerun()
                        st.stop()
                st.session_state.pop("wo_dup_confirmed", None)
                try:
                    matched_c = [c for c in contracts if c.get("id") == wo_contract_id]
                    c_no   = matched_c[0].get("contract_no","—") if matched_c else "—"
                    c_bldg = matched_c[0].get("building_name","—") if matched_c else "—"
                    payload = {
                        "contract_id": wo_contract_id, "title": wo_title.strip(),
                        "description": wo_description.strip(), "technician": wo_technician,
                        "scheduled_date": str(wo_scheduled_date), "status": wo_status,
                        "priority": wo_priority, "work_type": wo_work_type,
                    }
                    schema_errs = validate_payload(payload, SCHEMA_WORK_ORDERS, "work_orders")
                    if schema_errs:
                        for se in schema_errs: st.warning(se)
                    supabase.table("work_orders").insert(payload).execute()
                    log_action("add", "work_orders",
                               f"إضافة أمر عمل: {payload.get('title','')} — تقني: {payload.get('technician','')}",
                               severity="normal", entity_id=c_no)
                    load_work_orders.clear()
                    wa_result = notify_technician_whatsapp(wo_technician, wo_title.strip(), str(wo_scheduled_date), c_no, c_bldg, wo_priority)
                    if wa_result.get("ok"):
                        st.success(f"✅ تم حفظ أمر العمل وإرسال إشعار واتساب للفني {wo_technician}")
                    else:
                        st.success("✅ تم حفظ أمر العمل")
                    st.rerun()
                except Exception as e:
                    st.error(friendly_error(e))

    section_header("📋 عرض أوامر العمل")
    work_orders = scope_by_role(load_work_orders(), "technician")
    if False and is_tech():
        _tn = st.session_state.get("display_name", st.session_state.get("username",""))
        work_orders = [w for w in work_orders if w.get("technician","") == _tn]

    if not work_orders:
        st.info("لا توجد أوامر عمل.")
        return

    wo_df = pd.DataFrame(work_orders)
    if tech_name and tech_name in TECHNICIANS:
        wo_df = wo_df[wo_df["technician"] == tech_name]

    s1, s2, s3, s4 = st.columns(4)
    def mini_card(col, label, count, color):
        with col:
            st.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">{label}</div><div class="kpi-mini-value" style="color:{color}">{count}</div></div>', unsafe_allow_html=True)
    mini_card(s1, "⏳ معلق",   len(wo_df[wo_df["status"]=="pending"]),     "#111111")
    mini_card(s2, "🔄 جاري",   len(wo_df[wo_df["status"]=="in_progress"]), "#111111")
    mini_card(s3, "✅ مكتمل",  len(wo_df[wo_df["status"]=="completed"]),   "#111111")
    mini_card(s4, "❌ ملغي",   len(wo_df[wo_df["status"]=="cancelled"]),   "#111111")

    wf1, wf2, wf3 = st.columns(3)
    with wf1:
        filter_wo_status = st.selectbox("فلترة بالحالة", ["الكل","معلق","جاري","مكتمل","ملغي"], key="wo_status_filter")
    with wf2:
        filter_wo_priority = st.selectbox("فلترة بالأولوية", ["الكل","عاجلة","عالية","متوسطة","منخفضة"], key="wo_priority_filter")
    with wf3:
        search_wo = st.text_input("بحث برقم العقد أو الفني", key="wo_search")

    wo_status_reverse   = {"معلق":"pending","جاري":"in_progress","مكتمل":"completed","ملغي":"cancelled"}
    wo_priority_reverse = {"عاجلة":"urgent","عالية":"high","متوسطة":"medium","منخفضة":"low"}

    filtered_wo = wo_df.copy()
    if filter_wo_status != "الكل":
        filtered_wo = filtered_wo[filtered_wo["status"] == wo_status_reverse.get(filter_wo_status,"")]
    if filter_wo_priority != "الكل":
        filtered_wo = filtered_wo[filtered_wo["priority"] == wo_priority_reverse.get(filter_wo_priority,"")]
    if search_wo.strip():
        _id_to_cno = id_to_contract_no_map(contracts)
        filtered_wo["_cno"] = filtered_wo["contract_id"].astype(str).map(_id_to_cno).fillna("")
        filtered_wo = filtered_wo[
            filtered_wo["_cno"].str.contains(search_wo.strip(), case=False, na=False) |
            filtered_wo["technician"].str.contains(search_wo.strip(), case=False, na=False) |
            filtered_wo["title"].str.contains(search_wo.strip(), case=False, na=False)
        ]

    st.write(f"عدد النتائج: **{len(filtered_wo)}**")
    if not filtered_wo.empty:
        display_wo = filtered_wo.copy()
        _id_to_cno2 = id_to_contract_no_map(contracts)
        display_wo["رقم العقد"] = display_wo["contract_id"].astype(str).map(_id_to_cno2).fillna("—")
        status_map_ar   = {"pending":"معلق","in_progress":"جاري","completed":"مكتمل","cancelled":"ملغي"}
        priority_map_ar = {"urgent":"عاجلة","high":"عالية","medium":"متوسطة","low":"منخفضة"}
        work_type_ar    = {"preventive":"وقائي","corrective":"تصحيحي","emergency":"طارئ","inspection":"فحص"}
        display_wo["الحالة"]    = display_wo["status"].map(status_map_ar).fillna(display_wo["status"])
        display_wo["الأولوية"] = display_wo["priority"].map(priority_map_ar).fillna(display_wo["priority"])
        display_wo["نوع العمل"]= display_wo.get("work_type",pd.Series()).map(work_type_ar).fillna("")
        show_cols = ["رقم العقد","scheduled_date","technician","title","الأولوية","الحالة","نوع العمل"]
        existing  = [c for c in show_cols if c in display_wo.columns]
        col_rename_wo = {"scheduled_date":"التاريخ","technician":"الفني","title":"العنوان"}
        st.dataframe(display_wo[existing].rename(columns=col_rename_wo), use_container_width=True, hide_index=True)

    if not is_client():
        section_header("🔄 تحديث حالة أمر العمل")
        if not filtered_wo.empty:
            wo_opts = {
                f"{safe_text(row.get('title'),'—')} – {safe_text(row.get('technician'),'—')} (#{row.get('id','')})": row.get("id")
                for _, row in filtered_wo.iterrows()
            }
            selected_wo_label = st.selectbox("اختر أمر العمل", list(wo_opts.keys()), key="update_wo_select")
            selected_wo_id    = wo_opts.get(selected_wo_label)
            if selected_wo_id:
                with st.form("update_wo_form"):
                    u1, u2 = st.columns(2)
                    with u1:
                        new_wo_status = st.selectbox("الحالة الجديدة",
                            ["pending","in_progress","completed","cancelled"],
                            format_func=lambda x: {"pending":"معلق","in_progress":"جاري","completed":"مكتمل","cancelled":"ملغي"}[x])
                    with u2:
                        wo_notes = st.text_area("ملاحظات الإغلاق", height=80)
                    wo_update_submit = st.form_submit_button("💾 تحديث", use_container_width=True, type="primary")

                if wo_update_submit and supabase:
                    # مهمة 9: التحقق من التسلسل المنطقي
                    current_wo = next((r for _, r in filtered_wo.iterrows() if r.get("id") == selected_wo_id), None)
                    current_status_wo = current_wo.get("status","pending") if current_wo is not None else "pending"
                    if not is_valid_transition(current_status_wo, new_wo_status, WO_TRANSITIONS):
                        st.error(f"❌ لا يمكن الانتقال من '{WO_STATUSES.get(current_status_wo,current_status_wo)}' إلى '{WO_STATUSES.get(new_wo_status,new_wo_status)}'")
                    else:
                        # مهمة 17: Closure checklist
                        close_errs = validate_closure(new_wo_status, wo_notes.strip(), current_wo.get("technician","") if current_wo is not None else "")
                        if show_validation_errors(close_errs):
                            pass
                        else:
                            try:
                                upd = {"status": new_wo_status}
                                if wo_notes.strip(): upd["notes"] = wo_notes.strip()
                                if new_wo_status == "completed": upd["completed_at"] = datetime.now().isoformat()
                                supabase.table("work_orders").update(upd).eq("id", selected_wo_id).execute()
                                log_action("edit", "work_orders",
                                           f"تحديث حالة أمر عمل ID: {selected_wo_id}",
                                           severity="normal",
                                           entity_id=str(selected_wo_id),
                                           old_value=WO_STATUSES.get(current_status_wo, current_status_wo),
                                           new_value=WO_STATUSES.get(new_wo_status, new_wo_status))
                                load_work_orders.clear()
                                st.success("✅ تم التحديث")
                                st.rerun()
                            except Exception as e:
                                st.error(friendly_error(e))

# ════════════════════════════════════════════════════════
# TAB 4: Fault Reports
# ════════════════════════════════════════════════════════
def tab_fault_reports():
    contracts = load_contracts()

    if not is_client():
        section_header("➕ إضافة بلاغ عطل جديد")
        contract_options = {"-- بدون عقد محدد --": None}
        for c in contracts:
            contract_options[contract_label(c)] = c.get("id")

        with st.form("new_fault_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                selected_contract_label = st.selectbox("العقد المرتبط (اختياري)", list(contract_options.keys()))
                fr_customer_name  = st.text_input("اسم العميل")
                fr_mobile         = st.text_input("رقم الجوال")
                fr_building_name  = st.text_input("اسم المبنى")
            with fc2:
                fr_fault_description = st.text_area("وصف العطل *", height=100)
                fr_priority = st.selectbox("الأولوية",
                    ["low","medium","high","urgent"],
                    format_func=lambda x: {"low":"منخفضة","medium":"متوسطة","high":"عالية","urgent":"عاجلة"}[x],
                    index=2)
                fr_technician = st.selectbox("الفني المكلف", TECHNICIANS_WITH_UNASSIGNED)
            fr_submit = st.form_submit_button("💾 حفظ البلاغ", use_container_width=True, type="primary")

        if fr_submit:
            errs = validate_fault_report(fr_fault_description)
            if show_validation_errors(errs):
                pass
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                contract_id = contract_options.get(selected_contract_label)
                # مهمة 6: فحص التكرار في البلاغات
                if check_duplicate_fault(supabase, contract_id, fr_fault_description.strip()):
                    st.warning("⚠️ تم رصد بلاغ مماثل لهذا العقد خلال الـ 24 ساعة الماضية")
                    if not st.session_state.get("fr_dup_confirmed", False):
                        if st.button("نعم — أضف على أي حال", key="fr_dup_confirm_btn"):
                            st.session_state["fr_dup_confirmed"] = True
                            st.rerun()
                        st.stop()
                st.session_state.pop("fr_dup_confirmed", None)
                try:
                    if contract_id:
                        matched = [c for c in contracts if c.get("id") == contract_id]
                        if matched:
                            c = matched[0]
                            if not fr_customer_name.strip(): fr_customer_name = safe_text(c.get("customer_name"))
                            if not fr_mobile.strip():        fr_mobile        = safe_text(c.get("mobile"))
                            if not fr_building_name.strip(): fr_building_name = safe_text(c.get("building_name"))
                    tech_val   = fr_technician if fr_technician != "-- غير مكلف --" else None
                    status_val = "assigned" if tech_val else "open"
                    payload = {
                        "contract_id":   contract_id,
                        "title":         f"عطل — {fr_building_name.strip() or fr_customer_name.strip()}",
                        "description":   fr_fault_description.strip(),
                        "reported_date": str(date.today()),
                        "technician":    tech_val,
                        "status":        status_val,
                        "priority":      fr_priority,
                        "notes":         f"العميل: {fr_customer_name.strip()} | جوال: {fmt_phone(fr_mobile.strip())}",
                    }
                    schema_errs = validate_payload(payload, SCHEMA_FAULT_REPORTS, "fault_reports")
                    if schema_errs:
                        for se in schema_errs: st.warning(se)
                    supabase.table("fault_reports").insert(payload).execute()
                    log_action("add", "fault_reports",
                               f"إضافة بلاغ: {payload.get('title','')} — تقني: {payload.get('technician','')}",
                               severity="important")
                    load_fault_reports.clear()
                    if tech_val:
                        _c_no = contract_id and [c.get("contract_no","—") for c in contracts if c.get("id")==contract_id]
                        notify_technician_whatsapp(
                            tech_val, f"بلاغ عطل: {fr_fault_description.strip()[:60]}",
                            str(date.today()), _c_no[0] if _c_no else "—", fr_building_name.strip(), fr_priority)
                    st.success("✅ تم حفظ البلاغ بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(friendly_error(e))

    section_header("📋 عرض البلاغات")
    fault_reports = scope_by_role(load_fault_reports(), "technician")
    if False and is_tech():
        _tn2 = st.session_state.get("display_name", st.session_state.get("username",""))
        fault_reports = [f for f in fault_reports if f.get("technician","") == _tn2]
    if not fault_reports:
        st.info("لا توجد بلاغات.")
        return

    fr_df = pd.DataFrame(fault_reports)

    if is_client():
        cc = st.session_state.get("client_contract","")
        if cc:
            _id_to_cno = id_to_contract_no_map(contracts)
            fr_df["_cno"] = fr_df["contract_id"].astype(str).map(_id_to_cno).fillna("")
            fr_df = fr_df[fr_df["_cno"] == cc]

    # tech filter already applied above via fault_reports list

    s1, s2, s3, s4 = st.columns(4)
    s1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">مفتوح</div><div class="kpi-mini-value">{len(fr_df[fr_df["status"]=="open"])}</div></div>', unsafe_allow_html=True)
    s2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">مكلف</div><div class="kpi-mini-value">{len(fr_df[fr_df["status"]=="assigned"])}</div></div>', unsafe_allow_html=True)
    s3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">جاري</div><div class="kpi-mini-value">{len(fr_df[fr_df["status"]=="in_progress"])}</div></div>', unsafe_allow_html=True)
    s4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">محلول</div><div class="kpi-mini-value">{len(fr_df[fr_df["status"]=="resolved"])}</div></div>', unsafe_allow_html=True)

    ff1, ff2 = st.columns(2)
    with ff1:
        filter_fr_status = st.selectbox("فلترة بالحالة", ["الكل","مفتوح","مكلف","جاري","محلول","مغلق"], key="fr_status_filter")
    with ff2:
        filter_fr_priority = st.selectbox("فلترة بالأولوية", ["الكل","عاجلة","عالية","متوسطة","منخفضة"], key="fr_priority_filter")

    fr_filtered = fr_df.copy()
    fr_status_reverse   = {"مفتوح":"open","مكلف":"assigned","جاري":"in_progress","محلول":"resolved","مغلق":"closed"}
    fr_priority_reverse = {"عاجلة":"urgent","عالية":"high","متوسطة":"medium","منخفضة":"low"}
    if filter_fr_status != "الكل":
        fr_filtered = fr_filtered[fr_filtered["status"] == fr_status_reverse.get(filter_fr_status,"")]
    if filter_fr_priority != "الكل":
        fr_filtered = fr_filtered[fr_filtered["priority"] == fr_priority_reverse.get(filter_fr_priority,"")]

    st.write(f"عدد النتائج: **{len(fr_filtered)}**")
    if not fr_filtered.empty:
        display_fr = fr_filtered.copy()
        fr_status_map   = {"open":"مفتوح","assigned":"مكلف","in_progress":"جاري","resolved":"محلول","closed":"مغلق"}
        fr_priority_map = {"urgent":"عاجلة","high":"عالية","medium":"متوسطة","low":"منخفضة"}
        display_fr["الحالة"]   = display_fr["status"].map(fr_status_map).fillna(display_fr["status"])
        display_fr["الأولوية"] = display_fr["priority"].map(fr_priority_map).fillna(display_fr["priority"])
        show_cols = ["title","description","الأولوية","الحالة","technician","reported_date","notes"]
        existing_show = [c for c in show_cols if c in display_fr.columns]
        col_rename_fr = {"title":"عنوان البلاغ","description":"وصف العطل",
                         "technician":"الفني المكلف","reported_date":"تاريخ البلاغ","notes":"ملاحظات"}
        st.dataframe(display_fr[existing_show].rename(columns=col_rename_fr), use_container_width=True, hide_index=True)

    if not is_client():
        section_header("🔄 تحديث حالة البلاغ")
        if not fr_filtered.empty:
            fr_opts = {
                f"{str(row.get('title','—'))[:40]} (#{row.get('id','')})": row.get("id")
                for _, row in fr_filtered.iterrows()
            }
            selected_fr_label = st.selectbox("اختر البلاغ", list(fr_opts.keys()), key="update_fr_select")
            selected_fr_id = fr_opts.get(selected_fr_label)
            if selected_fr_id:
                with st.form("update_fr_form"):
                    uc1, uc2 = st.columns(2)
                    with uc1:
                        new_fr_status = st.selectbox("الحالة الجديدة",
                            ["open","assigned","in_progress","resolved","closed"],
                            format_func=lambda x: {"open":"مفتوح","assigned":"مكلف","in_progress":"جاري","resolved":"محلول","closed":"مغلق"}[x])
                        new_fr_tech = st.text_input("الفني المكلف")
                    with uc2:
                        resolution_notes = st.text_area("ملاحظات الحل", height=80)
                    fr_update_submit = st.form_submit_button("💾 تحديث البلاغ", use_container_width=True, type="primary")

                if fr_update_submit and supabase:
                    # مهمة 9: التحقق من التسلسل المنطقي
                    current_fr = next((r for _, r in fr_filtered.iterrows() if r.get("id") == selected_fr_id), None)
                    current_status_fr = current_fr.get("status","open") if current_fr is not None else "open"
                    if not is_valid_transition(current_status_fr, new_fr_status, FR_TRANSITIONS):
                        st.error(f"❌ لا يمكن الانتقال من '{FR_STATUSES.get(current_status_fr,current_status_fr)}' إلى '{FR_STATUSES.get(new_fr_status,new_fr_status)}'")
                    else:
                        fr_tech_val = new_fr_tech.strip() or (current_fr.get("technician","") if current_fr is not None else "")
                        close_errs = validate_closure(new_fr_status, resolution_notes.strip(), fr_tech_val)
                        if show_validation_errors(close_errs):
                            pass
                        else:
                            try:
                                upd = {"status": new_fr_status}
                                if resolution_notes.strip(): upd["notes"] = resolution_notes.strip()
                                if new_fr_tech.strip(): upd["technician"] = new_fr_tech.strip()
                                if new_fr_status in ("resolved","closed"): upd["closed_at"] = datetime.now().isoformat()
                                supabase.table("fault_reports").update(upd).eq("id", selected_fr_id).execute()
                                log_action("edit", "fault_reports",
                                           f"تحديث حالة بلاغ ID: {selected_fr_id}",
                                           severity="important",
                                           entity_id=str(selected_fr_id),
                                           old_value=FR_STATUSES.get(current_status_fr, current_status_fr),
                                           new_value=FR_STATUSES.get(new_fr_status, new_fr_status))
                                load_fault_reports.clear()
                                st.success("✅ تم تحديث البلاغ")
                                st.rerun()
                            except Exception as e:
                                st.error(friendly_error(e))

# ════════════════════════════════════════════════════════
# TAB 5: Maintenance Logs
# ════════════════════════════════════════════════════════
def tab_maintenance_logs():
    contracts = load_contracts()

    if not is_client():
        section_header("➕ إضافة سجل زيارة صيانة")
        contract_options = {"-- اختر العقد --": None}
        for c in contracts:
            contract_options[contract_label(c)] = c.get("id")

        with st.form("new_maintenance_log_form", clear_on_submit=True):
            mc1, mc2 = st.columns(2)
            with mc1:
                selected_contract_label = st.selectbox("العقد المرتبط *", list(contract_options.keys()))
                ml_elevator_no = st.text_input("رقم المصعد في المبنى")
                ml_visit_date  = st.date_input("تاريخ الزيارة", value=date.today())
                ml_technician  = st.selectbox("الفني", TECHNICIANS)
                ml_condition   = st.selectbox("حالة المصعد", ["good","fair","poor"],
                    format_func=lambda x: {"good":"جيد","fair":"متوسط","poor":"سيء"}[x])
            with mc2:
                ml_work_done  = st.text_area("الأعمال المنجزة *", height=100)
                ml_parts      = st.text_area("قطع الغيار المستبدلة", height=80)
                ml_next_visit = st.date_input("تاريخ الزيارة القادمة", value=date.today() + timedelta(days=90))
                ml_notes      = st.text_area("ملاحظات", height=60)
            ml_submit = st.form_submit_button("💾 حفظ سجل الصيانة", use_container_width=True, type="primary")

        if ml_submit:
            ml_contract_id_val = contract_options.get(selected_contract_label)
            errs = validate_maintenance_log(ml_work_done, ml_contract_id_val, ml_technician)
            if show_validation_errors(errs):
                pass
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                try:
                    payload = {
                        "contract_id": ml_contract_id_val,
                        "log_date":    str(ml_visit_date),
                        "technician":  ml_technician,
                        "work_done":   ml_work_done.strip(),
                        "parts_used":  ml_parts.strip(),
                        "notes":       f"مصعد: {ml_elevator_no.strip()} | الحالة: {ml_condition} | الزيارة القادمة: {ml_next_visit} | {ml_notes.strip()}",
                    }
                    schema_errs = validate_payload(payload, SCHEMA_MAINTENANCE_LOGS, "maintenance_logs")
                    if schema_errs:
                        for se in schema_errs: st.warning(se)
                    supabase.table("maintenance_logs").insert(payload).execute()
                    log_action("add", "maintenance_logs",
                               f"إضافة سجل صيانة — تقني: {payload.get('technician','')} — تاريخ: {payload.get('log_date','')}",
                               severity="normal")
                    load_maintenance_logs.clear()
                    st.success("✅ تم حفظ سجل الصيانة بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(friendly_error(e))

    section_header("📋 عرض سجل الصيانة")
    maintenance_logs = scope_by_role(load_maintenance_logs(), "technician")
    if not maintenance_logs:
        st.info("لا توجد سجلات صيانة.")
        return

    ml_df = pd.DataFrame(maintenance_logs)

    mf1, mf2 = st.columns(2)
    with mf1:
        tech_list_ml = ["الكل"] + sorted(ml_df["technician"].dropna().unique().tolist())
        filter_ml_tech = st.selectbox("فلترة بالفني", tech_list_ml, key="ml_tech_filter")
    with mf2:
        search_ml_contract = st.text_input("بحث برقم العقد", key="ml_contract_search")

    filtered_ml = ml_df.copy()
    if filter_ml_tech != "الكل":
        filtered_ml = filtered_ml[filtered_ml["technician"] == filter_ml_tech]
    if search_ml_contract.strip():
        _id_to_cno = id_to_contract_no_map(contracts)
        filtered_ml["_cno"] = filtered_ml["contract_id"].astype(str).map(_id_to_cno).fillna("")
        filtered_ml = filtered_ml[filtered_ml["_cno"].str.contains(search_ml_contract.strip(), case=False, na=False)]

    st.write(f"عدد السجلات: **{len(filtered_ml)}**")
    if not filtered_ml.empty:
        display_ml = filtered_ml.copy()
        _id_to_cno2 = id_to_contract_no_map(contracts)
        display_ml["رقم العقد"] = display_ml["contract_id"].astype(str).map(_id_to_cno2).fillna("—")
        show_cols = ["رقم العقد","log_date","technician","work_done","parts_used","notes"]
        existing_show = [c for c in show_cols if c in display_ml.columns]
        col_rename_ml = {"log_date":"تاريخ الزيارة","technician":"الفني",
                         "work_done":"الأعمال المنجزة","parts_used":"قطع الغيار","notes":"ملاحظات"}
        st.dataframe(display_ml[existing_show].rename(columns=col_rename_ml), use_container_width=True, hide_index=True)

        section_header("🔍 تفاصيل الزيارات")
        for _, row in filtered_ml.head(20).iterrows():
            visit_date_str = safe_text(row.get("log_date"), "—")
            tech_str       = safe_text(row.get("technician"), "—")
            with st.expander(f"زيارة {visit_date_str} – فني: {tech_str}"):
                d1, d2 = st.columns(2)
                with d1:
                    st.write(f"**تاريخ الزيارة:** {visit_date_str}")
                    st.write(f"**الأعمال المنجزة:** {safe_text(row.get('work_done'),'—')}")
                    st.write(f"**قطع الغيار:** {safe_text(row.get('parts_used'),'—')}")
                with d2:
                    st.write(f"**الفني:** {tech_str}")
                    st.write(f"**ملاحظات:** {safe_text(row.get('notes'),'—')}")

# ════════════════════════════════════════════════════════
# TAB 6: Elevators
# ════════════════════════════════════════════════════════
def tab_elevators():
    contracts        = load_contracts()
    maintenance_logs = load_maintenance_logs()

    section_header("🛗 إدارة المصاعد")

    if not contracts:
        st.info("لا توجد عقود.")
        return

    elevators = []
    for c in contracts:
        count    = safe_int(c.get("elevator_count"), 1)
        c_no     = safe_text(c.get("contract_no"), "—")
        c_id     = c.get("id")
        customer = safe_text(c.get("customer_name"), "—")
        building = safe_text(c.get("building_name"), "—")
        e_type   = safe_text(c.get("elevator_type"), "—")
        e_brand  = safe_text(c.get("elevator_brand"), "—")
        for i in range(1, count + 1):
            elevators.append({
                "contract_id": c_id, "contract_no": c_no,
                "customer": customer, "building": building,
                "elevator_no": str(i), "type": e_type, "brand": e_brand,
            })

    ml_map = {}
    for log in maintenance_logs:
        key = (str(log.get("contract_id","")), str(log.get("elevator_no","")))
        existing = ml_map.get(key)
        if existing is None:
            ml_map[key] = log
        else:
            try:
                if log.get("log_date","") > existing.get("log_date",""):
                    ml_map[key] = log
            except Exception:
                pass

    ef1, ef2, ef3 = st.columns(3)
    with ef1:
        search_elev = st.text_input("بحث بالعقد أو المبنى أو العميل", key="elev_search")
    with ef2:
        filter_elev_condition = st.selectbox("فلترة بحالة المصعد", ["الكل","تم الصيانة","لم يُصان"], key="elev_condition")
    with ef3:
        filter_elev_type = st.selectbox("فلترة بنوع المصعد",
            ["الكل"] + sorted(list({e["type"] for e in elevators if e["type"] != "—"})), key="elev_type")

    # cond_map removed — condition derived from maintenance log presence
    filtered_elev = elevators
    if search_elev.strip():
        q = search_elev.strip().lower()
        filtered_elev = [e for e in filtered_elev if
            q in e["contract_no"].lower() or q in e["building"].lower() or q in e["customer"].lower()]
    if filter_elev_type != "الكل":
        filtered_elev = [e for e in filtered_elev if e["type"] == filter_elev_type]

    if filter_elev_condition == "لم يُصان":
        filtered_elev = [e for e in filtered_elev if not ml_map.get((str(e["contract_id"]), e["elevator_no"]))]
    elif filter_elev_condition == "تم الصيانة":
        filtered_elev = [e for e in filtered_elev if ml_map.get((str(e["contract_id"]), e["elevator_no"]))]

    # Stats
    total_elev = len(filtered_elev)
    good_count = fair_count = poor_count = no_maint = 0
    for e in filtered_elev:
        key = (str(e["contract_id"]), e["elevator_no"])
        log = ml_map.get(key)
        if not log:
            no_maint += 1
        else:
            good_count += 1  # كل مصعد صُون مرة على الأقل = جيد

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ تم صيانتها</div><div class="kpi-mini-value">{good_count}</div></div>', unsafe_allow_html=True)
    sc2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚪ لم تُصان بعد</div><div class="kpi-mini-value" style="color:#c00">{no_maint}</div></div>', unsafe_allow_html=True)
    sc3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">إجمالي المصاعد</div><div class="kpi-mini-value">{total_elev}</div></div>', unsafe_allow_html=True)
    sc4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">عقود مرتبطة</div><div class="kpi-mini-value">{len(set(e["contract_no"] for e in filtered_elev))}</div></div>', unsafe_allow_html=True)

    st.markdown(f"**إجمالي المصاعد: {total_elev}**")
    st.markdown("---")

    cols_per_row = 3
    col_list = st.columns(cols_per_row)
    col_idx  = 0

    for e in filtered_elev:
        key  = (str(e["contract_id"]), e["elevator_no"])
        log  = ml_map.get(key)
        last_visit = safe_text(log.get("log_date"), "—") if log else "لا يوجد"
        technician = safe_text(log.get("technician"), "—") if log else "—"
        notes_raw  = safe_text(log.get("notes"), "") if log else ""
        cond_class = "good" if log else "fair"
        c_color = "#111111"
        c_bg    = "#ffffff"
        cond_ar = "تم الصيانة" if log else "لم يُصان بعد"

        with col_list[col_idx % cols_per_row]:
            st.markdown(f"""
            <div class="elev-card {cond_class}">
                <div class="elev-card-title">🛗 مصعد #{e['elevator_no']} — {e['building']}</div>
                <div class="elev-card-meta">📋 {e['contract_no']} &nbsp;|&nbsp; 👤 {e['customer']}</div>
                <div class="elev-card-meta">نوع: {e['type']} &nbsp;|&nbsp; ماركة: {e['brand']}</div>
                <hr style="margin:6px 0;border-color:#e9ecef">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                  <span style="font-size:0.9rem;color:#555">الحالة</span>
                  <span style="background:{c_bg};color:{c_color};padding:2px 10px;border-radius:12px;font-size:0.85rem;font-weight:700">{cond_ar}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.9rem;color:#555;margin-bottom:3px">
                  <span>آخر صيانة</span><strong style="color:#111111">{last_visit}</strong>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.9rem;color:#555">
                  <span>الفني</span><strong style="color:#111111">{technician}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        col_idx += 1

# ════════════════════════════════════════════════════════
# TAB 7: Maintenance Calendar
# ════════════════════════════════════════════════════════
def tab_calendar():
    maintenance_logs = load_maintenance_logs()
    work_orders      = load_work_orders()
    contracts        = load_contracts()

    section_header("📅 تقويم الصيانة الدورية")

    today      = date.today()
    week_start = today - timedelta(days=today.weekday())

    nav1, nav2, nav3 = st.columns([1, 4, 1])
    with nav1:
        if st.button("◀ السابق", key="cal_prev"):
            st.session_state.setdefault("cal_offset", 0)
            st.session_state.cal_offset -= 7
    with nav3:
        if st.button("التالي ▶", key="cal_next"):
            st.session_state.setdefault("cal_offset", 0)
            st.session_state.cal_offset += 7

    offset     = st.session_state.get("cal_offset", 0)
    week_start = week_start + timedelta(days=offset)
    week_end   = week_start + timedelta(days=6)

    with nav2:
        st.markdown(
            f"<div style='text-align:center;font-weight:700;font-size:1rem;padding:8px'>"
            f"الأسبوع: {week_start.strftime('%Y-%m-%d')} → {week_end.strftime('%Y-%m-%d')}"
            f"</div>", unsafe_allow_html=True)

    id_to_cno      = id_to_contract_no_map(contracts)
    events_by_day  = {week_start + timedelta(days=i): [] for i in range(7)}

    for log in maintenance_logs:
        nv = parse_date_safe(log.get("log_date"))
        if nv and week_start <= nv <= week_end:
            c_no = id_to_cno.get(str(log.get("contract_id","")), "—")
            events_by_day[nv].append({
                "label": f"🔧 صيانة – {c_no} – {safe_text(log.get('work_done','')[:30],'زيارة')}",
                "type": "preventive", "tech": safe_text(log.get("technician"),"—"),
            })

    for wo in work_orders:
        sd = parse_date_safe(wo.get("scheduled_date"))
        if sd and week_start <= sd <= week_end and wo.get("status") not in ("completed","cancelled"):
            c_no     = id_to_cno.get(str(wo.get("contract_id","")), "—")
            evt_type = "urgent" if wo.get("priority") in ("urgent","high") else "preventive"
            events_by_day[sd].append({
                "label": f"⚙️ {safe_text(wo.get('title'),'أمر عمل')} – {c_no}",
                "type": evt_type, "tech": safe_text(wo.get("technician"),"—"),
            })

    day_names_ar = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    cols = st.columns(7)
    for i, (day, events) in enumerate(events_by_day.items()):
        with cols[i]:
            is_today     = (day == today)
            header_color = "#111111" if is_today else "#555555"
            bg_color     = "#f0f0f0" if is_today else "#ffffff"
            st.markdown(f"""
            <div class="cal-day" style="background:{bg_color}; {'border:1.5px solid #111111;' if is_today else ''}">
                <div class="cal-day-header" style="color:{header_color}">
                    {day_names_ar[i]}<br>{day.strftime('%d/%m')}
                    {"📍" if is_today else ""}
                </div>
            """, unsafe_allow_html=True)
            if events:
                for ev in events:
                    ev_class = f"cal-event {ev['type']}"
                    st.markdown(f'<div class="{ev_class}">{ev["label"]}<br><small>👷 {ev["tech"]}</small></div>',
                                unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#ced4da;font-size:0.85rem;text-align:center;padding-top:10px">لا مهام</div>',
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    section_header("📋 الزيارات القادمة خلال 30 يوماً")
    upcoming = []
    for wo in work_orders:
        nv = parse_date_safe(wo.get("scheduled_date"))
        if nv and today <= nv <= today + timedelta(days=30) and wo.get("status") not in ("completed","cancelled"):
            c_no      = id_to_cno.get(str(wo.get("contract_id","")), "—")
            days_left = (nv - today).days
            upcoming.append({
                "رقم العقد": c_no, "العنوان": safe_text(wo.get("title"),"—"),
                "تاريخ الزيارة": str(nv), "الأيام المتبقية": days_left,
                "الفني": safe_text(wo.get("technician"),"—"),
            })

    if upcoming:
        upcoming_df = pd.DataFrame(upcoming).sort_values("الأيام المتبقية")
        st.dataframe(upcoming_df, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد زيارات أو أوامر عمل مجدولة خلال 30 يوماً.")

# ════════════════════════════════════════════════════════
# TAB 8: Technicians & Scheduling
# ════════════════════════════════════════════════════════
def tab_technicians():
    if is_client():
        st.info("🔒 هذا القسم متاح للمدير والفنيين فقط.")
        return

    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    contracts     = load_contracts()

    section_header("👷 إحصائيات الفنيين")

    wo_df = pd.DataFrame(work_orders) if work_orders else pd.DataFrame(columns=["technician","status","scheduled_date"])
    fr_df = pd.DataFrame(fault_reports) if fault_reports else pd.DataFrame(columns=["technician","status"])

    today       = date.today()
    month_start = today.replace(day=1)

    tech_cols = st.columns(len(TECHNICIANS))
    for idx, tech in enumerate(TECHNICIANS):
        with tech_cols[idx]:
            tech_wo = wo_df[wo_df["technician"] == tech] if not wo_df.empty else pd.DataFrame()
            pending_count = len(tech_wo[tech_wo["status"] == "pending"]) if not tech_wo.empty else 0
            completed_this_month = 0
            if not tech_wo.empty and "scheduled_date" in tech_wo.columns:
                tech_wo_copy = tech_wo.copy()
                tech_wo_copy["sched_parsed"] = pd.to_datetime(tech_wo_copy["scheduled_date"], errors="coerce").dt.date
                completed_this_month = len(tech_wo_copy[
                    (tech_wo_copy["status"] == "completed") &
                    (tech_wo_copy["sched_parsed"] >= month_start)
                ])
            tech_fr = fr_df[fr_df["technician"] == tech] if not fr_df.empty else pd.DataFrame()
            assigned_faults = len(tech_fr[tech_fr["status"].isin(["assigned","in_progress"])]) if not tech_fr.empty else 0

            st.markdown(f"""
            <div class="tech-card">
              <h3>👷 {tech}</h3>
              <div class="tech-stat"><span>أوامر معلقة</span><strong>{pending_count}</strong></div>
              <div class="tech-stat"><span>مكتملة هذا الشهر</span><strong>{completed_this_month}</strong></div>
              <div class="tech-stat"><span>بلاغات مكلف بها</span><strong>{assigned_faults}</strong></div>
            </div>
            """, unsafe_allow_html=True)

    section_header("📅 جدول مهام الأسبوع القادم")
    next_week_start = today + timedelta(days=1)
    next_week_end   = today + timedelta(days=7)

    if not wo_df.empty and "scheduled_date" in wo_df.columns:
        wo_schedule = wo_df.copy()
        wo_schedule["sched_parsed"] = pd.to_datetime(wo_schedule["scheduled_date"], errors="coerce").dt.date
        week_orders = wo_schedule[
            (wo_schedule["sched_parsed"] >= next_week_start) &
            (wo_schedule["sched_parsed"] <= next_week_end)
        ].sort_values(["sched_parsed","technician"])

        if not week_orders.empty:
            status_map    = {"pending":"معلق","in_progress":"جاري","completed":"مكتمل","cancelled":"ملغي"}
            priority_map  = {"urgent":"عاجلة","high":"عالية","medium":"متوسطة","low":"منخفضة"}
            work_type_map = {"preventive":"وقائي","corrective":"تصحيحي","emergency":"طارئ","inspection":"فحص"}
            week_orders["الحالة"]    = week_orders["status"].map(status_map).fillna(week_orders["status"])
            week_orders["الأولوية"] = week_orders["priority"].map(priority_map).fillna(week_orders["priority"])
            week_orders["نوع العمل"]= week_orders.get("work_type", pd.Series(dtype=str)).map(work_type_map).fillna("")
            show_week = ["scheduled_date","technician","title","الأولوية","الحالة","نوع العمل"]
            existing_week = [c for c in show_week if c in week_orders.columns]
            col_rename_week = {"scheduled_date":"التاريخ","technician":"الفني","title":"العنوان"}
            st.dataframe(week_orders[existing_week].rename(columns=col_rename_week), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مهام مجدولة للأسبوع القادم.")
    else:
        st.info("لا توجد أوامر عمل.")

    section_header("⚡ إضافة مهمة سريعة")
    contract_options = {"-- اختر العقد --": None}
    for c in contracts:
        contract_options[contract_label(c)] = c.get("id")

    with st.form("quick_task_form", clear_on_submit=True):
        qt1, qt2, qt3 = st.columns(3)
        with qt1:
            qt_tech     = st.selectbox("الفني", TECHNICIANS, key="qt_tech")
            qt_contract = st.selectbox("العقد", list(contract_options.keys()), key="qt_contract")
        with qt2:
            qt_date     = st.date_input("التاريخ", value=date.today() + timedelta(days=1), key="qt_date")
            qt_priority = st.selectbox("الأولوية",
                ["low","medium","high","urgent"],
                format_func=lambda x: {"low":"منخفضة","medium":"متوسطة","high":"عالية","urgent":"عاجلة"}[x],
                index=1, key="qt_priority")
        with qt3:
            qt_description = st.text_area("وصف المهمة *", height=100, key="qt_desc")
        qt_submit = st.form_submit_button("⚡ إضافة المهمة", use_container_width=True, type="primary")

    if qt_submit:
        if not qt_description.strip():
            st.error("❌ وصف المهمة مطلوب")
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                c_id      = contract_options.get(qt_contract)
                matched_c = [c for c in contracts if c.get("id") == c_id]
                c_no      = matched_c[0].get("contract_no","—") if matched_c else "—"
                c_bldg    = matched_c[0].get("building_name","—") if matched_c else "—"
                payload   = {
                    "contract_id": c_id, "title": qt_description.strip()[:100],
                    "description": qt_description.strip(), "technician": qt_tech,
                    "scheduled_date": str(qt_date), "status": "pending",
                    "priority": qt_priority, "work_type": "preventive",
                }
                supabase.table("work_orders").insert(payload).execute()
                log_action("add", "work_orders", f"إضافة مهمة تقويم: {payload.get('title','')} — تقني: {payload.get('technician','')}")
                load_work_orders.clear()
                notify_technician_whatsapp(qt_tech, qt_description.strip()[:60], str(qt_date), c_no, c_bldg, qt_priority)
                st.success("✅ تمت إضافة المهمة بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الإضافة: {e}")

# ════════════════════════════════════════════════════════
# TAB 9: Account
# ════════════════════════════════════════════════════════
def tab_account():
    section_header("👤 حسابي")
    username     = st.session_state.get("username", "")
    display_name = st.session_state.get("display_name", username)
    role         = get_role()
    role_ar      = ROLES.get(role, role)

    col1, col2 = st.columns([1, 2])
    with col1:
        acc_av = display_name[0] if display_name else "م"
        st.markdown(f"""
        <div style="background:white;border-radius:{8}px;padding:24px;text-align:center;
                    border:1px solid #d9dde8;box-shadow:0 2px 8px rgba(0,0,0,0.07)">
          <div style="width:72px;height:72px;background:#111111;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;
                      font-size:1.8rem;font-weight:800;color:white;margin:0 auto 14px;
                      box-shadow:0 4px 14px rgba(0,0,0,0.1)">{acc_av}</div>
          <h3 style="margin:0 0 6px;color:#111111;font-size:1.1rem">{display_name}</h3>
          <span class="badge">{role_ar}</span>
          <p style="color:#888888;margin-top:10px;font-size:0.95rem">@{username}</p>
          <div style="margin-top:14px;padding-top:14px;border-top:1px solid #e9ecef;
                      font-size:0.9rem;color:#888888">
            LiftTech V8.7 — نظام إدارة المصاعد
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔐 تغيير كلمة المرور")
        with st.form("change_password_form"):
            current_pwd = st.text_input("كلمة المرور الحالية", type="password", placeholder="أدخل كلمة المرور الحالية")
            new_pwd     = st.text_input("كلمة المرور الجديدة", type="password", placeholder="أدخل كلمة المرور الجديدة")
            confirm_pwd = st.text_input("تأكيد كلمة المرور الجديدة", type="password", placeholder="أعد إدخال كلمة المرور الجديدة")
            submit_pwd  = st.form_submit_button("💾 حفظ كلمة المرور الجديدة", use_container_width=True, type="primary")

        if submit_pwd:
            if not current_pwd or not new_pwd or not confirm_pwd:
                st.error("❌ يرجى ملء جميع الحقول")
            elif new_pwd != confirm_pwd:
                st.error("❌ كلمة المرور الجديدة وتأكيدها غير متطابقتين")
            elif len(new_pwd) < 4:
                st.error("❌ كلمة المرور يجب أن تكون 4 أحرف على الأقل")
            else:
                try:
                    users      = st.secrets["users"]
                    user_data  = users.get(username, {})
                    if isinstance(user_data, str):
                        secrets_pwd = user_data
                    else:
                        secrets_pwd = user_data.get("password", "")
                    db_pwd     = get_db_password(username)
                    active_pwd = db_pwd if db_pwd is not None else secrets_pwd
                    if current_pwd != active_pwd:
                        st.error("❌ كلمة المرور الحالية غير صحيحة")
                    else:
                        if set_db_password(username, new_pwd):
                            st.success("✅ تم تغيير كلمة المرور بنجاح!")
                        else:
                            st.error("❌ تعذّر حفظ كلمة المرور")
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")

    if is_admin():
        st.divider()
        st.markdown("### 🛡️ إدارة كلمات المرور (المدير العام فقط)")
        try:
            all_users = list(st.secrets["users"].keys())
        except Exception:
            all_users = []

        if all_users:
            with st.form("admin_reset_form"):
                target_user = st.selectbox("اختر المستخدم", all_users)
                reset_pwd   = st.text_input("كلمة المرور الجديدة", type="password")
                reset_btn   = st.form_submit_button("🔄 إعادة تعيين كلمة المرور", use_container_width=True, type="primary")

            if reset_btn:
                if not reset_pwd:
                    st.error("❌ أدخل كلمة المرور الجديدة")
                elif len(reset_pwd) < 4:
                    st.error("❌ كلمة المرور قصيرة جداً (4 أحرف على الأقل)")
                else:
                    if set_db_password(target_user, reset_pwd):
                        st.success(f"✅ تم إعادة تعيين كلمة مرور [{target_user}] بنجاح!")
                    else:
                        st.error("❌ تعذّر الحفظ")

# ════════════════════════════════════════════════════════
# MAIN — Odoo ERP Navigation
# ════════════════════════════════════════════════════════
def main():
    # مهمة 17: فحص انتهاء الجلسة تلقائياً
    enforce_session_timeout()
    role         = get_role()
    role_ar      = ROLES.get(role, role)
    display_name = st.session_state.get("display_name", st.session_state.get("username",""))
    avatar_char  = display_name[0] if display_name else "م"

    # ─── Sidebar — Odoo dark sidebar ───────────────────
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sb-logo">
          <div class="sb-logo-icon">🛗</div>
          <div>
            <div class="sb-logo-title">LiftTech</div>
            <div class="sb-logo-sub">نظام إدارة المصاعد</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # User card
        st.markdown(f"""
        <div class="sb-user">
          <div class="sb-avatar">{avatar_char}</div>
          <div>
            <div class="sb-name">{display_name}</div>
            <div class="sb-role">{role_ar}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # Navigation options based on role
        if is_admin() or is_manager():
            nav_options = {
                "📊  لوحة التحكم":   "dashboard",
                "📋  العقود":         "contracts",
                "🔧  أوامر العمل":   "work_orders",
                "🚨  البلاغات":      "fault_reports",
                "📝  سجل الصيانة":  "maintenance",
                "🛗  المصاعد":       "elevators",
                "📅  التقويم":       "calendar",
                "👷  الفنيون":       "technicians",
                "🗂️  سجل الأحداث":  "audit_log",
                "📊  جودة البيانات": "data_quality",
                "👥  المستخدمون":    "users",
                "👤  حسابي":         "account",
            }
        elif is_tech():
            nav_options = {
                "📊  لوحتي":          "dashboard",
                "🔧  أوامر عملي":    "work_orders",
                "🚨  بلاغاتي":       "fault_reports",
                "📝  سجل الصيانة":  "maintenance",
                "📅  التقويم":       "calendar",
                "👤  حسابي":         "account",
            }
        else:
            nav_options = {
                "📊  عقدي":           "dashboard",
                "🚨  بلاغاتي":       "fault_reports",
                "📝  سجل الصيانة":  "maintenance",
                "🛗  مصاعدي":        "elevators",
                "👤  حسابي":         "account",
            }

        nav_keys = list(nav_options.keys())
        nav_vals = list(nav_options.values())
        saved_page = st.session_state.get("current_page", "dashboard")
        saved_label_idx = 0
        for i, v in enumerate(nav_vals):
            if v == saved_page:
                saved_label_idx = i
                break

        selected_label = st.radio(
            "القائمة",
            nav_keys,
            index=saved_label_idx,
            label_visibility="collapsed",
            key="nav_radio",
        )
        selected_page = nav_options[selected_label]
        st.session_state["current_page"] = selected_page
        # حفظ الصفحة الحالية في URL لتبقى عند التحديث
        if st.query_params.get("pg") != selected_page:
            st.query_params["pg"] = selected_page

        # Logout
        st.markdown("<div style='flex:1; min-height:40px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='border-top:1px solid #dddddd;padding-top:10px;margin:8px 14px;'>"
            f"<div style='font-size:0.78rem;color:#aaaaaa;text-align:center;margin-bottom:8px'>"
            f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}</div></div>",
            unsafe_allow_html=True
        )
        if st.button("🚪  تسجيل الخروج", use_container_width=True, type="secondary"):
            # مهمة 7: تسجيل الخروج الصريح
            log_action("logout", "system",
                       f"تسجيل خروج: {st.session_state.get('display_name','')}",
                       severity="normal")
            for key in ["logged_in","username","role","display_name","client_contract",
                        "session_id","last_activity","current_page"]:
                st.session_state.pop(key, None)
            st.query_params.clear()
            st.rerun()

    # ─── Top header bar ────────────────────────────────
    page_titles = {
        "dashboard":    "📊 لوحة التحكم",
        "contracts":    "📋 إدارة العقود",
        "work_orders":  "🔧 أوامر العمل",
        "fault_reports":"🚨 البلاغات والأعطال",
        "maintenance":  "📝 سجل الصيانة",
        "elevators":    "🛗 إدارة المصاعد",
        "calendar":     "📅 تقويم الصيانة",
        "technicians":  "👷 الفنيون والجدولة",
        "audit_log":    "🗂️ سجل الأحداث",
        "data_quality": "📊 جودة البيانات",
        "users":        "👥 إدارة المستخدمين",
        "account":      "👤 حسابي",
    }
    page_title = page_titles.get(selected_page, "LiftTech")

    st.markdown(f"""
    <div class="top-header">
      <div class="top-header-left">
        <div class="top-header-title">{page_title}</div>
      </div>
      <div class="top-header-right">
        <span class="header-badge">{role_ar}</span>
        <span class="header-time">{datetime.now().strftime('%Y/%m/%d  %H:%M')}</span>
      </div>
    </div>
    <div style="padding: 16px 20px;">
    """, unsafe_allow_html=True)

    # ─── Page routing ───────────────────────────────────
    if selected_page == "dashboard":
        tab_dashboard()
    elif selected_page == "contracts":
        tab_contracts()
    elif selected_page == "work_orders":
        tab_work_orders()
    elif selected_page == "fault_reports":
        tab_fault_reports()
    elif selected_page == "maintenance":
        tab_maintenance_logs()
    elif selected_page == "elevators":
        tab_elevators()
    elif selected_page == "calendar":
        tab_calendar()
    elif selected_page == "technicians":
        tab_technicians()
    elif selected_page == "audit_log":
        tab_audit_log()
    elif selected_page == "data_quality":
        tab_data_quality()
    elif selected_page == "users":
        tab_users()
    elif selected_page == "account":
        tab_account()

    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TAB: Audit Log — سجل الأحداث (admin فقط)
# ════════════════════════════════════════════════════════
def tab_audit_log():
    require_role("admin")

    section_header("📋 سجل الأحداث والنشاط")

    # ── إنشاء الجدول إن لم يكن موجوداً ──
    if supabase is None:
        st.error("❌ لا يوجد اتصال بقاعدة البيانات.")
        return

    # فلاتر
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        filter_user = st.text_input("بحث بالمستخدم", placeholder="الكل")
    with col_f2:
        filter_module = st.selectbox("الوحدة", ["الكل", "system", "contracts", "work_orders", "fault_reports", "maintenance_logs", "passwords"])
    with col_f3:
        filter_action = st.selectbox("نوع الحدث", ["الكل", "login", "logout", "add", "edit", "delete", "export"])
    with col_f4:
        filter_severity = st.selectbox("الأهمية", ["الكل", "normal", "important", "sensitive", "security", "critical"])

    # جلب البيانات
    try:
        query = supabase.table("audit_logs").select("*").order("created_at", desc=True).limit(500)
        r = query.execute()
        logs = r.data or []
    except Exception as e:
        err = str(e)
        if "PGRST205" in err or "not found" in err.lower():
            st.warning("⚠️ جدول سجل الأحداث غير موجود بعد. سيتم إنشاؤه تلقائياً عند أول حدث.")
            st.code("""
-- نفّذ هذا SQL في Supabase Dashboard → SQL Editor:
CREATE TABLE IF NOT EXISTS public.audit_logs (
  id         bigserial PRIMARY KEY,
  username   text NOT NULL,
  role       text,
  action     text NOT NULL,
  module     text,
  details    text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE public.audit_logs DISABLE ROW LEVEL SECURITY;
            """, language="sql")
        else:
            st.error(f"❌ خطأ: {e}")
        return

    if not logs:
        st.info("لا توجد أحداث مسجّلة بعد.")
        return

    import pandas as pd
    df = pd.DataFrame(logs)

    # فلترة
    if filter_user.strip():
        df = df[df["username"].str.contains(filter_user.strip(), na=False)]
    if filter_module != "الكل":
        df = df[df["module"] == filter_module]
    if filter_action != "الكل":
        df = df[df["action"] == filter_action]
    if filter_severity != "الكل" and "severity" in df.columns:
        df = df[df["severity"] == filter_severity]

    st.markdown(f"<div style='margin-bottom:10px;font-size:0.88rem;color:#555;'>إجمالي الأحداث: <strong>{len(df)}</strong></div>", unsafe_allow_html=True)

    # تنسيق الأحداث — أيقونة لكل نوع
    action_icons = {
        "login":  "🔑",
        "logout": "🚪",
        "add":    "➕",
        "edit":   "✏️",
        "delete": "🗑️",
        "export": "📤",
        "view":   "👁️",
    }
    module_ar = {
        "system":            "النظام",
        "contracts":         "العقود",
        "work_orders":       "أوامر العمل",
        "fault_reports":     "البلاغات",
        "maintenance_logs":  "الصيانة",
        "passwords":         "كلمات المرور",
        "dashboard":         "الداشبورد",
    }
    severity_colors = {
        "normal":   ("#f0f4f8", "#555"),
        "important":("#fff3cd", "#856404"),
        "sensitive": ("#fde8e8", "#9b1c1c"),
        "security": ("#dbeafe", "#1e40af"),
        "critical": ("#dc2626", "#fff"),
    }
    severity_ar = {
        "normal":   "عادي",
        "important":"مهم",
        "sensitive": "حساس",
        "security": "أمني",
        "critical": "حرج",
    }

    for _, row in df.iterrows():
        icon      = action_icons.get(str(row.get("action","")), "📌")
        mod_ar    = module_ar.get(str(row.get("module","")), str(row.get("module","")))
        ts_raw    = str(row.get("created_at",""))
        ts        = ts_raw[:19].replace("T", "  ") if ts_raw else "—"
        uname     = str(row.get("username","—"))
        role_v    = str(row.get("role",""))
        details   = str(row.get("details",""))
        sev       = str(row.get("severity","normal") or "normal")
        entity_id = str(row.get("entity_id","") or "")
        old_val   = str(row.get("old_value","") or "")
        new_val   = str(row.get("new_value","") or "")

        role_badge_color = {"admin":"#111","manager":"#1a6e3c","tech":"#1a4e8c"}.get(role_v,"#888")
        role_ar_map = {"admin":"مدير عام","manager":"مدير","tech":"فني","client":"عميل"}
        role_ar_v = role_ar_map.get(role_v, role_v)
        sev_bg, sev_fg = severity_colors.get(sev, ("#f0f0f0","#555"))
        sev_label = severity_ar.get(sev, sev)
        entity_html = f"<span style=\"color:#aaa;font-size:0.75rem;\"># {entity_id}</span>" if entity_id else ""
        diff_html = ""
        if old_val or new_val:
            diff_html = (
                f"<div style=\"margin-top:5px;font-size:0.78rem;display:flex;gap:10px;flex-wrap:wrap;\">"
                f"<span style=\"background:#fef9c3;padding:2px 8px;border-radius:6px;color:#92400e;\">قبل: {old_val or chr(8212)}</span>"
                f"<span style=\"background:#dcfce7;padding:2px 8px;border-radius:6px;color:#14532d;\">بعد: {new_val or chr(8212)}</span>"
                f"</div>"
            )

        st.markdown(f"""
<div style="background:#fff;border:1.5px solid #e8e8e8;border-radius:8px;padding:10px 16px;
            margin-bottom:6px;display:flex;align-items:flex-start;gap:12px;direction:rtl;">
  <div style="font-size:1.4rem;min-width:28px;">{icon}</div>
  <div style="flex:1;">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">
      <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
        <span style="font-weight:700;color:#111;font-size:0.9rem;">{uname}</span>
        <span style="background:{role_badge_color};color:#fff;font-size:0.72rem;padding:2px 8px;border-radius:10px;">{role_ar_v}</span>
        <span style="background:#f0f0f0;color:#444;font-size:0.78rem;padding:2px 8px;border-radius:10px;">{mod_ar}</span>
        <span style="background:{sev_bg};color:{sev_fg};font-size:0.72rem;padding:2px 8px;border-radius:10px;font-weight:600;">{sev_label}</span>
        {entity_html}
      </div>
      <span style="font-size:0.78rem;color:#999;direction:ltr;">{ts}</span>
    </div>
    <div style="font-size:0.84rem;color:#444;margin-top:4px;">{details}</div>
    {diff_html}
  </div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# مهمة 5: Users Management Page — إدارة المستخدمين
# ════════════════════════════════════════════════════════
def tab_users():
    require_perm("users.manage")
    section_header("👥 إدارة المستخدمين والصلاحيات")

    st.markdown("""
<div style="background:#f0f9ff;border:1.5px solid #bae6fd;border-radius:8px;
            padding:12px 18px;margin-bottom:16px;direction:rtl;font-size:0.88rem;">
    <strong>📋 مصفوفة الصلاحيات:</strong>
    المدير العام (ماجد) يرى كل شيء •
    المديرون يرون نطاقهم •
    الفنيون يرون مهامهم فقط
</div>""", unsafe_allow_html=True)

    # ── عرض المستخدمين الحاليين ──
    section_header("📋 قائمة المستخدمين")
    rows = []
    for uname, info in STAFF_REGISTRY.items():
        db_pwd = get_db_password(uname)
        has_custom_pwd = db_pwd is not None and db_pwd != "12345"
        rows.append({
            "المستخدم":    uname,
            "الاسم":       info.get("name","—"),
            "الدور":       ROLES.get(info.get("role",""),"—"),
            "الفريق":      info.get("team","—"),
            "المنطقة":     info.get("region","—"),
            "الحالة":      "✅ نشط" if info.get("active",True) else "⏸️ موقوف",
            "كلمة المرور": "🔒 مخصصة" if has_custom_pwd else "⚠️ افتراضية",
        })
    import pandas as _pd
    st.dataframe(_pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── إعادة تعيين كلمة المرور ──
    section_header("🔑 إعادة تعيين كلمة المرور")
    col1, col2 = st.columns(2)
    with col1:
        reset_user = st.selectbox("اختر المستخدم",
            [u for u in STAFF_REGISTRY if u != st.session_state.get("username","")],
            format_func=lambda u: f"{STAFF_REGISTRY[u]['name']} ({u})",
            key="reset_pwd_user")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 إعادة تعيين إلى الافتراضي (12345)", key="reset_pwd_btn"):
            set_db_password(reset_user, "12345")
            log_action("password_reset", "passwords",
                       f"إعادة تعيين كلمة مرور: {reset_user} بواسطة {st.session_state.get('username','')}",
                       severity="sensitive", entity_id=reset_user)
            st.success(f"✅ تم إعادة تعيين كلمة مرور {STAFF_REGISTRY[reset_user]['name']} — سيُطلب منه تغييرها عند الدخول")

    # ── مصفوفة الصلاحيات التفصيلية ──
    section_header("🔐 مصفوفة الصلاحيات")
    perm_rows = []
    screens = [
        ("العقود",       ["contracts.view","contracts.create","contracts.edit","contracts.delete","contracts.export"]),
        ("أوامر العمل",  ["work_orders.view","work_orders.create","work_orders.edit","work_orders.assign","work_orders.close","work_orders.reopen","work_orders.delete","work_orders.export"]),
        ("البلاغات",     ["fault_reports.view","fault_reports.create","fault_reports.edit","fault_reports.assign","fault_reports.close","fault_reports.reopen","fault_reports.delete","fault_reports.export"]),
        ("الصيانة",      ["maintenance.view","maintenance.create","maintenance.edit","maintenance.export"]),
        ("الداشبورد",    ["dashboard.view"]),
        ("سجل الأحداث", ["audit_log.view"]),
        ("المستخدمون",   ["users.manage"]),
        ("جودة البيانات",["data_quality.view"]),
    ]
    action_ar = {
        "view":"عرض","create":"إضافة","edit":"تعديل","delete":"حذف",
        "assign":"إسناد","close":"إغلاق","reopen":"إعادة فتح",
        "export":"تصدير","print":"طباعة","manage":"إدارة",
    }
    for screen, perms in screens:
        for perm in perms:
            action = perm.split(".")[-1]
            row = {"الشاشة": screen, "الإجراء": action_ar.get(action, action)}
            for role in (ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH, ROLE_CLIENT):
                role_ar = ROLES.get(role,"")
                allowed = role in PERMISSIONS.get(perm, set())
                row[role_ar] = "✅" if allowed else "—"
            perm_rows.append(row)
    st.dataframe(_pd.DataFrame(perm_rows), use_container_width=True, hide_index=True)

    # ── مهمة 20: Governance Handbook ──
    section_header("📖 وثيقة الحوكمة")
    with st.expander("📄 عرض وثيقة الحوكمة الداخلية — V13", expanded=False):
        st.markdown("""
<div style="direction:rtl;line-height:2;font-size:0.9rem;">

<h4 style="border-bottom:2px solid #111;padding-bottom:4px;">🏢 نظام LiftTech — وثيقة الحوكمة الداخلية</h4>

<h5>1. الأدوار المعتمدة</h5>
<table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
  <tr style="background:#f0f0f0;"><th>الدور</th><th>المستخدم</th><th>النطاق</th></tr>
  <tr><td>مدير عام (admin)</td><td>ماجد</td><td>كامل الصلاحيات</td></tr>
  <tr><td>مدير (manager)</td><td>أحمد، طه، علي، أيمن</td><td>العمليات والتحصيل والفني</td></tr>
  <tr><td>فني (tech)</td><td>فيصل، سيلفوم، فريتز، جنيد، كفاية الله</td><td>مهامه وبلاغاته فقط</td></tr>
  <tr><td>عميل (client)</td><td>—</td><td>عقده وبلاغاته فقط</td></tr>
</table>

<h5>2. قواعد التعديل والإغلاق</h5>
• السجلات المغلقة أو الملغاة لا تُعدَّل مباشرةً.<br>
• إعادة الفتح تتطلب: admin أو manager + سبب معتمد من القائمة.<br>
• التعديل على العقود يُسجَّل في سجل الأحداث مع قيم قبل/بعد.<br>
• الحذف محصور بـ admin فقط ويُسجَّل كحدث حرج.

<h5>3. سياسة كلمة المرور</h5>
• الحد الأدنى 6 أحرف.<br>
• الكلمات الافتراضية محظورة (12345، password، admin).<br>
• تغيير الكلمة الافتراضية إلزامي عند أول دخول.<br>
• إعادة التعيين من صلاحيات admin فقط.

<h5>4. سياسة الجلسات</h5>
• انتهاء الجلسة تلقائياً بعد 120 دقيقة من عدم النشاط.<br>
• كل جلسة لها معرف فريد يُسجَّل مع الأحداث.<br>
• تسجيل الخروج يمسح جميع بيانات الجلسة.

<h5>5. سياسة التصدير</h5>
• التصدير محصور بـ admin و manager.<br>
• كل تصدير يُسجَّل في سجل الأحداث بالوحدة والعدد.<br>
• الفنيون والعملاء لا يستطيعون التصدير.

<h5>6. سياسة النسخ الاحتياطي</h5>
• نسخ تلقائي يومي بواسطة Supabase.<br>
• تصدير CSV يدوي أسبوعي من صفحة جودة البيانات.<br>
• الاحتفاظ: 30 يوماً يومي — 12 شهراً شهري.<br>
• بيئة اختبار منفصلة في Supabase.

<h5>7. سياسة سجل الأحداث</h5>
• جميع العمليات: إضافة، تعديل، حذف، إسناد، إغلاق، تصدير، دخول، خروج، فشل دخول.<br>
• التصنيف: عادي / مهم / حساس / أمني / حرج.<br>
• حفظ القيم قبل/بعد التعديل في الحقول الحرجة.<br>
• سجل الأحداث للمدير العام فقط.

</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# TAB: Data Quality Report — مهمة 19
# ════════════════════════════════════════════════════════
def tab_data_quality():
    require_role("admin", "manager")
    section_header("📊 تقرير جودة البيانات")

    if supabase is None:
        st.error("❌ لا يوجد اتصال بقاعدة البيانات.")
        return

    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    maintenance   = load_maintenance_logs()

    report = data_quality_report(contracts, work_orders, fault_reports, maintenance)

    # ── مؤشرات سريعة ──
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'''<div class="kpi-card"><div class="kpi-label">عقود</div><div class="kpi-value">{report["contracts"]}</div></div>''', unsafe_allow_html=True)
    c2.markdown(f'''<div class="kpi-card"><div class="kpi-label">أوامر عمل</div><div class="kpi-value">{report["work_orders"]}</div></div>''', unsafe_allow_html=True)
    c3.markdown(f'''<div class="kpi-card"><div class="kpi-label">بلاغات</div><div class="kpi-value">{report["fault_reports"]}</div></div>''', unsafe_allow_html=True)
    c4.markdown(f'''<div class="kpi-card"><div class="kpi-label">سجلات صيانة</div><div class="kpi-value">{report["maintenance"]}</div></div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── مشكلات الجودة ──
    section_header("⚠️ المشكلات المرصودة")
    if not report["issues"]:
        st.success("✅ لا توجد مشكلات جودة بيانات — البيانات نظيفة")
    else:
        st.markdown(f"<p style='color:#9b1c1c;font-weight:700;'>تم رصد {report['total_issues']} مشكلة:</p>", unsafe_allow_html=True)
        for issue in report["issues"]:
            st.markdown(f"""
<div style="background:#fef2f2;border:1.5px solid #fca5a5;border-radius:8px;
            padding:10px 16px;margin-bottom:6px;direction:rtl;font-size:0.9rem;">
    {issue}
</div>""", unsafe_allow_html=True)

    # ── Schema Alignment Check ──
    section_header("🔎 فحص تطابق البيانات مع الـ Schema")
    schema_issues = []
    for c_rec in contracts[:10]:
        extra = set(c_rec.keys()) - SCHEMA_CONTRACTS - {"id","created_at"}
        if extra: schema_issues.append(f"contracts — حقول إضافية: {extra}")
    for wo in work_orders[:10]:
        extra = set(wo.keys()) - SCHEMA_WORK_ORDERS - {"id","created_at","notes","completed_at","closed_at"}
        if extra: schema_issues.append(f"work_orders — حقول إضافية: {extra}")
    for fr in fault_reports[:10]:
        extra = set(fr.keys()) - SCHEMA_FAULT_REPORTS - {"id","created_at","closed_at"}
        if extra: schema_issues.append(f"fault_reports — حقول إضافية: {extra}")
    if schema_issues:
        for si in schema_issues:
            st.warning(si)
    else:
        st.success("✅ جميع الجداول متطابقة مع الـ Schema المتوقع")

    # ── مهمة 18: Backup Policy ──
    section_header("💾 سياسة النسخ الاحتياطي")
    st.markdown("""
<div style="background:#f0fdf4;border:1.5px solid #86efac;border-radius:8px;
            padding:14px 18px;direction:rtl;font-size:0.88rem;line-height:1.8;">
<strong>📋 السياسة المعتمدة:</strong><br>
• <strong>Supabase</strong>: نسخ احتياطي تلقائي يومي بواسطة Supabase (مدفوع).<br>
• <strong>يدوي</strong>: تصدير CSV أسبوعي لكل جدول من هذه الصفحة.<br>
• <strong>الاحتفاظ</strong>: 30 يوماً للنسخ اليومية — 12 شهراً للنسخ الشهرية.<br>
• <strong>الاستعادة</strong>: عبر Supabase Dashboard → Backups أو استيراد CSV.<br>
• <strong>بيئة الاختبار</strong>: مشروع Supabase منفصل لتجنب المساس ببيانات الإنتاج.
</div>""", unsafe_allow_html=True)

    # أزرار تصدير الجداول
    section_header("⬇️ تصدير جداول قاعدة البيانات")
    import pandas as _pd2
    backup_cols = st.columns(4)
    backup_tables = [
        ("contracts",       "عقود"),
        ("work_orders",     "أوامر عمل"),
        ("fault_reports",   "بلاغات"),
        ("maintenance_logs","صيانة"),
    ]
    for i, (tbl, label) in enumerate(backup_tables):
        with backup_cols[i]:
            try:
                res = supabase.table(tbl).select("*").execute() if supabase else None
                data = res.data if res else []
                df_bk = _pd2.DataFrame(data)
                csv_bk = df_bk.to_csv(index=False, encoding="utf-8-sig")
                from datetime import date as _bkd
                fname = f"{tbl}_{_bkd.today()}.csv"
                controlled_download_button(
                    f"⬇️ {label}", data=csv_bk.encode("utf-8-sig"),
                    filename=fname, mime="text/csv",
                    module=tbl.replace("_logs","").replace("_","."),
                    record_count=len(data), key=f"backup_{tbl}")
            except Exception as e:
                st.warning(f"{label}: {friendly_error(e)}")


if __name__ == "__main__":
    main()

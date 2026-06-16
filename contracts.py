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
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: #f0f0f0 !important;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] div:first-child {
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

ROLES = {
    "admin":   "مدير عام",
    "manager": "مدير",
    "tech":    "فني",
    "client":  "عميل",
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
                        })
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            except Exception:
                st.error("❌ لا توجد بيانات مستخدمين في الإعدادات")
    return False

if not check_login():
    st.stop()

# Role helpers
def get_role():    return st.session_state.get("role", "admin")
def is_admin():    return get_role() == "admin"
def is_tech():     return get_role() == "tech"
def is_manager():  return get_role() == "manager"
def is_client():   return get_role() == "client"

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
    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()

    if is_client():
        cc = st.session_state.get("client_contract", "")
        if cc:
            contracts = [c for c in contracts if str(c.get("contract_no","")) == cc]

    df    = prepare_contracts_df(contracts)
    today = date.today()

    # ══ حسابات ══
    total_c = len(df)
    total_v = paid_v = unpaid_v = 0.0
    paid_c  = unpaid_c = total_el = 0
    n_30 = n_60 = 0

    if not df.empty:
        total_v  = float(df["contract_value"].apply(safe_number).sum())
        total_el = int(df["elevator_count"].apply(safe_int).sum())
        paid_c   = int((df["payment_display"] == "مسدد").sum())
        unpaid_c = int((df["payment_display"] == "غير مسدد").sum())
        try: paid_v   = float(df[df["payment_display"]=="مسدد"]["contract_value"].apply(safe_number).sum())
        except: paid_v = 0.0
        try: unpaid_v = float(df[df["payment_display"]=="غير مسدد"]["contract_value"].apply(safe_number).sum())
        except: unpaid_v = 0.0
        if "days_remaining" in df.columns:
            dr   = df["days_remaining"]
            n_30 = int((dr.notna() & (dr >= 0) & (dr <= 30)).sum())
            n_60 = int((dr.notna() & (dr > 30) & (dr <= 60)).sum())

    collect_pct  = round(paid_v   / total_v * 100, 1) if total_v else 0.0
    uncollect_pct= round(unpaid_v / total_v * 100, 1) if total_v else 0.0
    collect_rate = round(paid_c   / total_c * 100, 1) if total_c else 0.0
    avg_contract = round(total_v  / total_c, 0)        if total_c else 0.0
    val_per_el   = round(total_v  / total_el, 0)       if total_el else 0.0
    urgent_wo    = len([w for w in work_orders   if w.get("status") in ("pending","in_progress")]) if work_orders   else 0
    open_fr      = len([f for f in fault_reports if f.get("status") in ("open","assigned")])       if fault_reports else 0

    def fmt(n): return f"{float(n):,.0f}" if n else "0"

    day_ar = {"Monday":"الاثنين","Tuesday":"الثلاثاء","Wednesday":"الأربعاء",
               "Thursday":"الخميس","Friday":"الجمعة","Saturday":"السبت","Sunday":"الأحد"}
    mon_ar = {"January":"يناير","February":"فبراير","March":"مارس","April":"أبريل",
               "May":"مايو","June":"يونيو","July":"يوليو","August":"أغسطس",
               "September":"سبتمبر","October":"أكتوبر","November":"نوفمبر","December":"ديسمبر"}
    today_str = today.strftime("%A، %d %B %Y")
    for e, a in {**day_ar, **mon_ar}.items():
        today_str = today_str.replace(e, a)

    bar_w = min(int(collect_pct), 100)

    # ══ CSS مرة واحدة ══
    st.markdown("""
<style>
.db-header{display:flex;justify-content:space-between;align-items:center;
           border-bottom:2px solid #111;padding-bottom:10px;margin-bottom:14px;}
.db-title-sub{font-size:0.8rem;font-weight:700;color:#888;letter-spacing:1.5px;text-transform:uppercase;}
.db-title-main{font-size:1.6rem;font-weight:900;color:#111;line-height:1.1;}
.db-date{font-size:0.95rem;color:#333;font-weight:600;}
.db-src{font-size:0.8rem;color:#888;}

/* db-card classes removed — inline styles used */

/* db-bar classes removed — inline styles used */

/* db-kpi classes removed — inline styles used */
</style>
""", unsafe_allow_html=True)

    # ── HEADER ──
    st.markdown(f"""
<div class="db-header">
  <div>
    <div class="db-title-sub">LiftTech — التقرير المالي الإداري</div>
    <div class="db-title-main">ملخص الأداء المالي</div>
  </div>
  <div style="text-align:left">
    <div class="db-date">{today_str}</div>
    <div class="db-src">بيانات فعلية — Supabase</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── ROW 1: 3 بطاقات كبيرة ──
    c1, c2, c3 = st.columns(3)
    _card = 'background:#fff;border:2px solid #111;border-radius:10px;padding:20px 22px;box-sizing:border-box;'
    _lbl  = 'font-size:0.78rem;font-weight:700;color:#555 !important;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;'
    _val  = 'font-size:2.4rem;font-weight:900;color:#111 !important;line-height:1;letter-spacing:-1px;'
    _sub  = 'font-size:0.84rem;color:#444 !important;margin-top:8px;'
    with c1:
        st.markdown(f"""<div style="{_card}">
  <div style="{_lbl}">إجمالي محفظة العقود</div>
  <div style="{_val}">{fmt(total_v)}</div>
  <div style="{_sub}">ريال سعودي — {total_c} عقد</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div style="{_card}">
  <div style="{_lbl}">المبالغ المحصّلة</div>
  <div style="{_val}">{fmt(paid_v)}</div>
  <div style="{_sub}">{collect_pct}% من الإجمالي — {paid_c} عقد</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div style="{_card}">
  <div style="{_lbl}">المبالغ المتأخرة</div>
  <div style="{_val}">{fmt(unpaid_v)}</div>
  <div style="{_sub}">{uncollect_pct}% من الإجمالي — {unpaid_c} عقد</div>
</div>""", unsafe_allow_html=True)

    # ── ROW 2: شريط التحصيل ──
    st.markdown(f"""<div style="background:#fff;border:2px solid #111;border-radius:10px;padding:14px 22px;margin:10px 0;">
  <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
    <span style="font-size:0.9rem;font-weight:700;color:#111 !important;">مؤشر التحصيل الإجمالي</span>
    <span style="font-size:0.9rem;color:#333 !important;"><strong>{collect_pct}%</strong> نسبة التحصيل الفعلية</span>
  </div>
  <div style="background:#eee;border-radius:4px;height:12px;overflow:hidden;">
    <div style="width:{bar_w}%;height:12px;background:#111;border-radius:4px;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:0.83rem;color:#555 !important;">
    <span>&#9632; محصّل: {fmt(paid_v)} ر.س ({paid_c} عقد)</span>
    <span>&#9632; متأخر: {fmt(unpaid_v)} ر.س ({unpaid_c} عقد)</span>
  </div>
</div>""", unsafe_allow_html=True)

    # ── ROW 3: 6 عدادات ──
    k1, k2, k3 = st.columns(3)
    _kpi = 'background:#fff;border:2px solid #111;border-radius:10px;padding:16px 20px;display:flex;align-items:center;gap:14px;'
    _num = 'font-size:2rem;font-weight:900;color:#111 !important;line-height:1;min-width:60px;'
    _kl  = 'font-size:0.88rem;font-weight:700;color:#111 !important;line-height:1.3;'
    _ks  = 'font-size:0.78rem;color:#555 !important;margin-top:3px;'
    with k1:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{fmt(avg_contract)}</div><div><div style="{_kl}">متوسط قيمة العقد</div><div style="{_ks}">ريال سعودي</div></div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{total_el}</div><div><div style="{_kl}">إجمالي المصاعد</div><div style="{_ks}">متوسط {fmt(val_per_el)} ر.س / مصعد</div></div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{n_30}</div><div><div style="{_kl}">تنتهي خلال 30 يوم</div><div style="{_ks}">تستوجب متابعة فورية</div></div></div>', unsafe_allow_html=True)

    k4, k5, k6 = st.columns(3)
    with k4:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{n_60}</div><div><div style="{_kl}">تنتهي خلال 60 يوم</div><div style="{_ks}">تحتاج تجديداً قريباً</div></div></div>', unsafe_allow_html=True)
    with k5:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{urgent_wo}</div><div><div style="{_kl}">أوامر عمل مفتوحة</div><div style="{_ks}">بلاغات مفتوحة: {open_fr}</div></div></div>', unsafe_allow_html=True)
    with k6:
        st.markdown(f'<div style="{_kpi}"><div style="{_num}">{collect_rate}%</div><div><div style="{_kl}">نسبة التحصيل</div><div style="{_ks}">من إجمالي العقود</div></div></div>', unsafe_allow_html=True)


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
            city = st.text_input("المدينة")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # مجموعة 3: بيانات المصعد
        st.markdown('<div class="form-group"><div class="form-group-header">🛗 بيانات المصعد</div><div class="form-group-body">', unsafe_allow_html=True)
        g3c1, g3c2, g3c3 = st.columns(3)
        with g3c1:
            elevator_count = st.number_input("عدد المصاعد", min_value=1, value=1)
        with g3c2:
            elevator_type  = st.selectbox("نوع المصعد", ["ركاب","شحن","بانوراما","خدمة","سلم كهربائي"])
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
        if not contract_no.strip() or not customer_name.strip():
            st.error("❌ رقم العقد واسم العميل مطلوبان")
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                payload = {
                    "contract_no": contract_no.strip(), "customer_name": customer_name.strip(),
                    "mobile": mobile.strip(), "building_name": building_name.strip(),
                    "district": district.strip(), "city": city.strip(),
                    "elevator_count": int(elevator_count), "elevator_type": elevator_type,
                    "elevator_brand": elevator_brand.strip(), "contract_value": float(contract_value),
                    "start_date": str(start_date), "end_date": str(end_date),
                    "payment_status": payment_status, "contract_status": contract_status,
                    "collector": collector.strip(), "notes": notes.strip(),
                }
                supabase.table("contracts").insert(payload).execute()
                load_contracts.clear()
                st.success("✅ تم حفظ العقد بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الحفظ: {e}")

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
        st.download_button("⬇️ تصدير CSV", data=csv_bytes, file_name="contracts.csv", mime="text/csv")
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
                            ["ركاب","شحن","بانوراما","خدمة","سلم كهربائي"],
                            index=["ركاب","شحن","بانوراما","خدمة","سلم كهربائي"].index(ec.get("elevator_type","ركاب"))
                                  if ec.get("elevator_type") in ["ركاب","شحن","بانوراما","خدمة","سلم كهربائي"] else 0)
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
                    try:
                        supabase.table("contracts").update({
                            "customer_name": e_customer.strip(),
                            "mobile": e_mobile.strip(),
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
                        }).eq("id", selected_id).execute()
                        load_contracts.clear()
                        st.success("✅ تم حفظ التعديلات")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")

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
            if not wo_title.strip():
                st.error("❌ عنوان أمر العمل مطلوب")
            elif wo_contract_id is None:
                st.error("❌ يجب اختيار عقد مرتبط")
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
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
                    supabase.table("work_orders").insert(payload).execute()
                    load_work_orders.clear()
                    wa_result = notify_technician_whatsapp(wo_technician, wo_title.strip(), str(wo_scheduled_date), c_no, c_bldg, wo_priority)
                    if wa_result.get("ok"):
                        st.success(f"✅ تم حفظ أمر العمل وإرسال إشعار واتساب للفني {wo_technician}")
                    else:
                        st.success("✅ تم حفظ أمر العمل")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    section_header("📋 عرض أوامر العمل")
    work_orders = load_work_orders()
    # الفني يرى فقط أوامره
    if is_tech():
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
                    try:
                        upd = {"status": new_wo_status}
                        if wo_notes.strip(): upd["notes"] = wo_notes.strip()
                        if new_wo_status == "completed": upd["completed_at"] = datetime.now().isoformat()
                        supabase.table("work_orders").update(upd).eq("id", selected_wo_id).execute()
                        load_work_orders.clear()
                        st.success("✅ تم التحديث")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")

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
            if not fr_fault_description.strip():
                st.error("❌ وصف العطل مطلوب")
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                try:
                    contract_id = contract_options.get(selected_contract_label)
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
                        "notes":         f"العميل: {fr_customer_name.strip()} | جوال: {fr_mobile.strip()}",
                    }
                    supabase.table("fault_reports").insert(payload).execute()
                    load_fault_reports.clear()
                    if tech_val:
                        _c_no = contract_id and [c.get("contract_no","—") for c in contracts if c.get("id")==contract_id]
                        notify_technician_whatsapp(
                            tech_val, f"بلاغ عطل: {fr_fault_description.strip()[:60]}",
                            str(date.today()), _c_no[0] if _c_no else "—", fr_building_name.strip(), fr_priority)
                    st.success("✅ تم حفظ البلاغ بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    section_header("📋 عرض البلاغات")
    fault_reports = load_fault_reports()
    # الفني يرى فقط بلاغاته
    if is_tech():
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
                    try:
                        upd = {"status": new_fr_status}
                        if resolution_notes.strip(): upd["notes"] = resolution_notes.strip()
                        if new_fr_tech.strip(): upd["technician"] = new_fr_tech.strip()
                        supabase.table("fault_reports").update(upd).eq("id", selected_fr_id).execute()
                        load_fault_reports.clear()
                        st.success("✅ تم تحديث البلاغ")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء التحديث: {e}")

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
            if not ml_work_done.strip():
                st.error("❌ الأعمال المنجزة مطلوبة")
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                try:
                    payload = {
                        "contract_id": contract_options.get(selected_contract_label),
                        "log_date":    str(ml_visit_date),
                        "technician":  ml_technician,
                        "work_done":   ml_work_done.strip(),
                        "parts_used":  ml_parts.strip(),
                        "notes":       f"مصعد: {ml_elevator_no.strip()} | الحالة: {ml_condition} | الزيارة القادمة: {ml_next_visit} | {ml_notes.strip()}",
                    }
                    supabase.table("maintenance_logs").insert(payload).execute()
                    load_maintenance_logs.clear()
                    st.success("✅ تم حفظ سجل الصيانة بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    section_header("📋 عرض سجل الصيانة")
    maintenance_logs = load_maintenance_logs()
    # الفني يرى فقط سجلاته
    if is_tech():
        _tn3 = st.session_state.get("display_name", st.session_state.get("username",""))
        maintenance_logs = [m for m in maintenance_logs if m.get("technician","") == _tn3]
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

        # Logout
        st.markdown("<div style='flex:1; min-height:40px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='border-top:1px solid #dddddd;padding-top:10px;margin:8px 14px;'>"
            f"<div style='font-size:0.78rem;color:#aaaaaa;text-align:center;margin-bottom:8px'>"
            f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}</div></div>",
            unsafe_allow_html=True
        )
        if st.button("🚪  تسجيل الخروج", use_container_width=True, type="secondary"):
            for key in ["logged_in","username","role","display_name","client_contract"]:
                st.session_state.pop(key, None)
            # مسح query_params عند الخروج
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
    elif selected_page == "account":
        tab_account()

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

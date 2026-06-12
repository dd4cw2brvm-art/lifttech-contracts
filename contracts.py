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
    page_title="LiftTech V5.1",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Google Fonts + Global CSS
# ─────────────────────────────────────────────
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("""
<style>
  * { font-family: 'Cairo', sans-serif !important; }
  body, .stApp { direction: rtl; background-color: #f1f5f9 !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 1400px !important; }

  .app-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    color: white; padding: 1.2rem 2rem; border-radius: 16px;
    margin-bottom: 1.5rem; display: flex; align-items: center;
    justify-content: space-between; box-shadow: 0 4px 20px rgba(15,23,42,0.25);
  }
  .app-header h1 { margin: 0; font-size: 1.8rem; font-weight: 800; }
  .app-header p  { margin: 0; font-size: 0.9rem; opacity: 0.75; }

  .kpi-card {
    background: white; border-radius: 14px; padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); border-right: 5px solid #3b82f6;
    margin-bottom: 1rem; transition: transform 0.2s;
  }
  .kpi-card:hover { transform: translateY(-3px); }
  .kpi-card.danger  { border-right-color: #ef4444; }
  .kpi-card.success { border-right-color: #22c55e; }
  .kpi-card.warning { border-right-color: #f59e0b; }
  .kpi-card.info    { border-right-color: #3b82f6; }
  .kpi-card .kpi-icon  { font-size: 2rem; float: left; }
  .kpi-card .kpi-value { font-size: 2rem; font-weight: 800; color: #0f172a; }
  .kpi-card .kpi-title { font-size: 0.85rem; color: #64748b; margin-top: 0.2rem; }

  .section-header {
    background: white; border-radius: 10px; padding: 0.7rem 1.2rem;
    margin: 1.2rem 0 0.8rem 0; border-right: 4px solid #3b82f6;
    font-size: 1.05rem; font-weight: 700; color: #0f172a;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  }

  .alert-expired { background:#fef2f2; border-right:4px solid #ef4444; color:#991b1b; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-30      { background:#fff7ed; border-right:4px solid #f97316; color:#9a3412; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-60      { background:#fefce8; border-right:4px solid #eab308; color:#713f12; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-90      { background:#f0fdf4; border-right:4px solid #22c55e; color:#14532d; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }

  .badge { display:inline-block; padding:2px 10px; border-radius:12px; font-size:0.78rem; font-weight:700; white-space:nowrap; }
  .badge-urgent     { background:#fee2e2; color:#dc2626; }
  .badge-high       { background:#ffedd5; color:#ea580c; }
  .badge-medium     { background:#fef9c3; color:#ca8a04; }
  .badge-low        { background:#dcfce7; color:#16a34a; }
  .badge-pending    { background:#f1f5f9; color:#475569; }
  .badge-in_progress{ background:#dbeafe; color:#1d4ed8; }
  .badge-completed  { background:#dcfce7; color:#15803d; }
  .badge-cancelled  { background:#fee2e2; color:#b91c1c; }
  .badge-open       { background:#f1f5f9; color:#475569; }
  .badge-assigned   { background:#fef9c3; color:#92400e; }
  .badge-resolved   { background:#dcfce7; color:#15803d; }
  .badge-closed     { background:#e2e8f0; color:#334155; }

  .stTextInput>div>div>input,
  .stTextArea>div>div>textarea,
  .stSelectbox>div>div>div,
  .stNumberInput>div>div>input,
  .stDateInput>div>div>input {
    border-radius:8px !important; border:1.5px solid #e2e8f0 !important;
    font-family:'Cairo',sans-serif !important; direction:rtl !important; text-align:right !important;
  }
  .stButton>button { border-radius:8px !important; font-family:'Cairo',sans-serif !important; font-weight:700 !important; }

  .stTabs [data-baseweb="tab-list"] {
    background:white; border-radius:10px; padding:4px;
    box-shadow:0 1px 6px rgba(0,0,0,0.07); gap:4px; flex-wrap:wrap;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius:8px !important; font-family:'Cairo',sans-serif !important;
    font-weight:600 !important; padding:0.5rem 1rem !important; color:#475569 !important;
  }
  .stTabs [aria-selected="true"] { background:#3b82f6 !important; color:white !important; }
  .stDataFrame { border-radius:10px; overflow:hidden; }

  .tech-card {
    background:white; border-radius:14px; padding:1.2rem 1.4rem;
    box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:1rem; border-top:4px solid #3b82f6;
  }
  .tech-card h3   { margin:0 0 0.8rem 0; font-size:1.1rem; color:#0f172a; }
  .tech-stat      { display:flex; justify-content:space-between; margin-bottom:0.4rem; font-size:0.9rem; }
  .tech-stat span { font-weight:700; color:#3b82f6; }

  /* Role badge */
  .role-admin   { background:#dbeafe; color:#1d4ed8; padding:3px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }
  .role-tech    { background:#dcfce7; color:#15803d; padding:3px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }
  .role-client  { background:#fef9c3; color:#92400e; padding:3px 10px; border-radius:20px; font-size:0.8rem; font-weight:700; }

  /* Calendar */
  .cal-day {
    background:white; border-radius:10px; padding:0.6rem 0.8rem;
    box-shadow:0 1px 6px rgba(0,0,0,0.07); margin-bottom:0.5rem; min-height:80px;
  }
  .cal-day-header { font-size:0.8rem; color:#64748b; margin-bottom:0.3rem; font-weight:700; }
  .cal-event { background:#dbeafe; color:#1d4ed8; border-radius:6px; padding:2px 8px; font-size:0.78rem; margin-bottom:3px; }
  .cal-event.urgent { background:#fee2e2; color:#dc2626; }
  .cal-event.preventive { background:#dcfce7; color:#15803d; }

  .login-container {
    max-width:420px; margin:5rem auto; background:white; border-radius:20px;
    padding:2.5rem; box-shadow:0 8px 32px rgba(0,0,0,0.12); text-align:center;
  }
  .login-container h2 { color:#0f172a; margin-bottom:0.4rem; }
  .login-container p  { color:#64748b; margin-bottom:2rem; }

  /* Elevator card */
  .elev-card {
    background:white; border-radius:12px; padding:1rem 1.2rem;
    box-shadow:0 1px 8px rgba(0,0,0,0.07); margin-bottom:0.8rem;
    border-right:4px solid #3b82f6;
  }
  .elev-card.good { border-right-color:#22c55e; }
  .elev-card.fair { border-right-color:#f59e0b; }
  .elev-card.poor { border-right-color:#ef4444; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
TECHNICIANS = ["فيصل", "سيلفوم", "فريتز", "جنيد", "كفاية الله"]
TECHNICIANS_WITH_UNASSIGNED = ["-- غير مكلف --"] + TECHNICIANS

# Role definitions
ROLES = {
    "admin":   "مدير عام",       # ماجد — صلاحيات كاملة
    "manager": "مدير",           # أحمد / طه / علي / أيمن
    "tech":    "فني",            # فيصل / سيلفوم / فريتز / جنيد / كفاية الله
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
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ تعذّر الاتصال بـ Supabase: {e}")
        return None

supabase = init_supabase()

# ─────────────────────────────────────────────
# Authentication  (multi-role)
# ─────────────────────────────────────────────
def check_login():
    if st.session_state.get("logged_in"):
        return True

    st.markdown("""
    <div class="login-container">
      <div style="font-size:3.5rem">🛗</div>
      <h2>LiftTech V5.1</h2>
      <p>نظام إدارة شركة صيانة المصاعد</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            submit   = st.form_submit_button("دخول", use_container_width=True)

        if submit:
            try:
                users = st.secrets["users"]
                if username not in users:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    user_data = users[username]
                    # Support both formats:
                    # New format: users.admin = {password="x", role="admin", name=".."}
                    # Old format: users.admin = "password_string"
                    if isinstance(user_data, str):
                        # Legacy flat format
                        pwd_match = (user_data == password)
                        role_val  = "admin"
                        name_val  = username
                        contract_val = ""
                    else:
                        # New dict format
                        pwd_match    = (user_data.get("password", "") == password)
                        role_val     = user_data.get("role", "admin")
                        name_val     = user_data.get("name", username)
                        contract_val = user_data.get("contract_no", "")

                    if pwd_match:
                        st.session_state.logged_in       = True
                        st.session_state.username        = username
                        st.session_state.role            = role_val
                        st.session_state.display_name    = name_val
                        st.session_state.client_contract = contract_val
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            except Exception:
                st.error("❌ لا توجد بيانات مستخدمين في الإعدادات")
    return False

if not check_login():
    st.stop()

# Role helpers
def get_role():
    return st.session_state.get("role", "admin")

def is_admin():
    return get_role() == "admin"

def is_tech():
    return get_role() == "tech"

def is_manager():
    return get_role() == "manager"

def is_client():
    return get_role() == "client"

# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────
def safe_text(val, default=""):
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default

def safe_number(val, default=0.0):
    try:
        return float(val)
    except Exception:
        return default

def safe_int(val, default=0):
    try:
        return int(val)
    except Exception:
        return default

def parse_date_safe(val):
    if val is None:
        return None
    try:
        return pd.to_datetime(val).date()
    except Exception:
        return None

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

# ─────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────
def metric_card(title, value, icon="📊", variant="info"):
    st.markdown(f"""
    <div class="kpi-card {variant}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def priority_badge(priority):  # available for future use
    labels = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
    label  = labels.get(priority, priority)
    return f'<span class="badge badge-{priority}">{label}</span>'

def status_badge(status):  # available for future use
    labels = {
        "pending": "معلق", "in_progress": "جاري", "completed": "مكتمل",
        "cancelled": "ملغي", "open": "مفتوح", "assigned": "مكلف",
        "resolved": "محلول", "closed": "مغلق",
    }
    label = labels.get(status, status)
    return f'<span class="badge badge-{status}">{label}</span>'

def role_badge(role):  # available for future use
    labels = {"admin": "مدير", "tech": "فني", "client": "عميل"}
    label  = labels.get(role, role)
    return f'<span class="role-{role}">{label}</span>'

# ─────────────────────────────────────────────
# Data loaders
# ─────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_contracts():
    if supabase is None:
        return []
    try:
        resp = supabase.table("contracts").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل العقود: {e}")
        return []

@st.cache_data(ttl=30)
def load_work_orders():
    if supabase is None:
        return []
    try:
        resp = supabase.table("work_orders").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل أوامر العمل: {e}")
        return []

@st.cache_data(ttl=30)
def load_fault_reports():
    if supabase is None:
        return []
    try:
        resp = supabase.table("fault_reports").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل البلاغات: {e}")
        return []

@st.cache_data(ttl=30)
def load_maintenance_logs():
    if supabase is None:
        return []
    try:
        resp = supabase.table("maintenance_logs").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل سجل الصيانة: {e}")
        return []

def prepare_contracts_df(contracts):
    if not contracts:
        return pd.DataFrame()
    df    = pd.DataFrame(contracts)
    today = date.today()

    def compute_days(row):
        d = parse_date_safe(row.get("end_date"))
        return None if d is None else (d - today).days

    df["days_remaining"] = df.apply(compute_days, axis=1)

    def compute_status_display(row):
        cs = safe_text(row.get("contract_status"), "active")
        if cs == "expired":
            return "منتهي"
        dr = row.get("days_remaining")
        if dr is None:
            return "نشط"
        if dr < 0:
            return "منتهي"
        if dr <= 30:
            return "ينتهي قريباً"
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
    """إرسال إشعار واتساب للفني عند تعيين مهمة جديدة."""
    # خريطة اسم الفني → رقم هاتفه (أضف الأرقام هنا)
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
    """يولّد تقرير PDF شهري باستخدام reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
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
    style_title = ParagraphStyle("title", fontSize=16, textColor=colors.HexColor("#0f172a"),
                                  alignment=1, spaceAfter=12)
    style_sub   = ParagraphStyle("sub", fontSize=10, textColor=colors.HexColor("#64748b"),
                                  alignment=1, spaceAfter=20)
    style_h     = ParagraphStyle("h", fontSize=12, textColor=colors.HexColor("#1d4ed8"),
                                  alignment=1, spaceAfter=8, spaceBefore=14)
    style_body  = ParagraphStyle("body", fontSize=9, alignment=1, spaceAfter=4)

    story.append(Paragraph(ar(f"تقرير شركة لفتك للمصاعد"), style_title))
    story.append(Paragraph(ar(f"الفترة: {month_label}"), style_sub))
    story.append(Paragraph(ar(f"تاريخ الإصدار: {date.today().strftime('%Y-%m-%d')}"), style_sub))
    story.append(Spacer(1, 0.3*cm))

    # KPIs
    total      = len(df)
    active     = len(df[df["status_display"] == "نشط"]) if not df.empty else 0
    expiring   = len(df[df["days_remaining"].notna() & (df["days_remaining"] >= 0) & (df["days_remaining"] <= 30)]) if not df.empty else 0
    total_val  = df["contract_value"].apply(safe_number).sum() if not df.empty else 0
    wo_done    = len([w for w in work_orders if w.get("status") == "completed"]) if work_orders else 0

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
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e3a5f")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.5*cm))

    # Expiring contracts table
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
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#ef4444")),
                ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
                ("FONTSIZE",   (0,0), (-1,-1), 8),
                ("ALIGN",      (0,0), (-1,-1), "CENTER"),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fef2f2")]),
                ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ]))
            story.append(t)
        else:
            story.append(Paragraph(ar("لا توجد عقود حرجة"), style_body))
    story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    return buf.getvalue()

# ─────────────────────────────────────────────
# TAB 1: Dashboard
# ─────────────────────────────────────────────
def tab_dashboard():
    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()

    # Filter for client role
    if is_client():
        cc = st.session_state.get("client_contract", "")
        if cc:
            contracts = [c for c in contracts if str(c.get("contract_no","")) == cc]

    df    = prepare_contracts_df(contracts)
    today = date.today()

    total_contracts  = len(df)
    total_value      = df["contract_value"].apply(safe_number).sum() if not df.empty else 0
    active_contracts = len(df[df["status_display"] == "نشط"]) if not df.empty else 0
    unpaid_contracts = len(df[df["payment_display"] == "غير مسدد"]) if not df.empty else 0
    total_elevators  = df["elevator_count"].apply(safe_int).sum() if not df.empty else 0

    # KPIs
    section_header("📊 مؤشرات الأداء الرئيسية")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("إجمالي العقود",    total_contracts,              "📄", "info")
    with c2: metric_card("القيمة الإجمالية", f"{total_value:,.0f} ر.س",   "💰", "success")
    with c3: metric_card("العقود النشطة",    active_contracts,             "✅", "success")
    with c4: metric_card("غير المسددة",      unpaid_contracts,             "⚠️", "danger")
    with c5: metric_card("إجمالي المصاعد",   total_elevators,              "🛗", "warning")

    # Renewal alerts
    section_header("🔔 تنبيهات التجديد")
    if not df.empty and "days_remaining" in df.columns:
        expired = df[df["days_remaining"].notna() & (df["days_remaining"] < 0)]
        exp_30  = df[df["days_remaining"].notna() & (df["days_remaining"] >= 0) & (df["days_remaining"] <= 30)]
        exp_60  = df[df["days_remaining"].notna() & (df["days_remaining"] > 30) & (df["days_remaining"] <= 60)]
        exp_90  = df[df["days_remaining"].notna() & (df["days_remaining"] > 60) & (df["days_remaining"] <= 90)]
        a1, a2, a3, a4 = st.columns(4)
        with a1: st.markdown(f'<div class="alert-expired">❌ منتهية: <strong>{len(expired)}</strong> عقد</div>', unsafe_allow_html=True)
        with a2: st.markdown(f'<div class="alert-30">🔴 خلال 30 يوم: <strong>{len(exp_30)}</strong> عقد</div>', unsafe_allow_html=True)
        with a3: st.markdown(f'<div class="alert-60">🟡 خلال 60 يوم: <strong>{len(exp_60)}</strong> عقد</div>', unsafe_allow_html=True)
        with a4: st.markdown(f'<div class="alert-90">🟢 خلال 90 يوم: <strong>{len(exp_90)}</strong> عقد</div>', unsafe_allow_html=True)

    # Payment cards
    section_header("💳 حالة التحصيل")
    if not df.empty:
        paid    = len(df[df["payment_display"] == "مسدد"])
        partial = len(df[df["payment_display"] == "جزئي"])
        unpaid  = len(df[df["payment_display"] == "غير مسدد"])
        ratio   = round((paid / total_contracts * 100), 1) if total_contracts else 0
        b1, b2, b3, b4 = st.columns(4)
        with b1: metric_card("مسدد",       paid,         "✅", "success")
        with b2: metric_card("جزئي",       partial,      "⚡", "warning")
        with b3: metric_card("غير مسدد",   unpaid,       "❌", "danger")
        with b4: metric_card("نسبة السداد", f"{ratio}%", "📈", "info")

    # Charts
    section_header("📈 المخططات البيانية")
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("**توزيع العقود حسب حالة السداد**")
        if not df.empty:
            st.bar_chart(df["payment_display"].value_counts())
        else:
            st.info("لا توجد بيانات")
    with ch2:
        st.markdown("**توزيع العقود حسب الحي**")
        if not df.empty and "district" in df.columns:
            st.bar_chart(df["district"].fillna("غير محدد").value_counts().head(10))
        else:
            st.info("لا توجد بيانات")

    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown("**أوامر العمل حسب الحالة**")
        if work_orders:
            wo_df = pd.DataFrame(work_orders)
            status_map = {"pending": "معلق", "in_progress": "جاري", "completed": "مكتمل", "cancelled": "ملغي"}
            wo_df["status_ar"] = wo_df["status"].map(status_map).fillna(wo_df["status"])
            st.bar_chart(wo_df["status_ar"].value_counts())
        else:
            st.info("لا توجد أوامر عمل")
    with ch4:
        st.markdown("**الإيرادات الشهرية (قيمة العقود المضافة)**")
        if not df.empty and "created_at" in df.columns:
            df_rev = df.copy()
            df_rev["month"] = pd.to_datetime(df_rev["created_at"], errors="coerce").dt.to_period("M").astype(str)
            df_rev["contract_value_num"] = df_rev["contract_value"].apply(safe_number)
            monthly = df_rev.groupby("month")["contract_value_num"].sum().sort_index().tail(12)
            if not monthly.empty:
                st.bar_chart(monthly)
            else:
                st.info("لا توجد بيانات كافية")
        else:
            st.info("لا توجد بيانات")

    # Critical contracts
    section_header("🚨 العقود الحرجة")
    if not df.empty:
        critical = df[df["days_remaining"].notna() & (df["days_remaining"] <= 90)].sort_values("days_remaining").head(50)
        if not critical.empty:
            display_cols = ["contract_no","customer_name","building_name","district","end_date","days_remaining","payment_display","contract_value"]
            existing_cols = [c for c in display_cols if c in critical.columns]
            col_rename = {
                "contract_no": "رقم العقد", "customer_name": "اسم العميل",
                "building_name": "اسم المبنى", "district": "الحي",
                "end_date": "تاريخ الانتهاء", "days_remaining": "الأيام المتبقية",
                "payment_display": "حالة السداد", "contract_value": "قيمة العقد",
            }
            st.dataframe(critical[existing_cols].rename(columns=col_rename), use_container_width=True, hide_index=True)
        else:
            st.success("✅ لا توجد عقود حرجة حالياً")

    # WhatsApp reminders
    if not is_client():
        section_header("📲 تذكير تجديد العقود عبر واتساب")
        st.markdown("""
        <div style='background:linear-gradient(135deg,#25D366,#128C7E);padding:18px 24px;border-radius:14px;color:white;margin-bottom:16px'>
            <div style='font-size:18px;font-weight:700;margin-bottom:6px'>🛗 إرسال تذكيرات التجديد</div>
            <div style='font-size:14px;opacity:0.9'>يرسل رسائل واتساب تلقائية للعملاء الذين عقودهم تنتهي خلال المدة المحددة</div>
        </div>
        """, unsafe_allow_html=True)

        col_wa1, col_wa2, col_wa3 = st.columns([2, 1, 1])
        with col_wa1:
            days_before = st.slider("إرسال التذكير قبل انتهاء العقد بـ (يوم)", 7, 60, 30, key="wa_days")
        with col_wa2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            send_btn = st.button("📤 إرسال التذكيرات الآن", type="primary", use_container_width=True)
        with col_wa3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if not df.empty and "end_date" in df.columns:
                expiring = df[pd.to_datetime(df["end_date"], errors="coerce") <= (pd.Timestamp.now() + pd.Timedelta(days=days_before))]
                expiring = expiring[pd.to_datetime(expiring["end_date"], errors="coerce") >= pd.Timestamp.now()]
                st.metric("عقود تستحق التذكير", len(expiring))
            else:
                st.metric("عقود تستحق التذكير", 0)

        if send_btn:
            if not df.empty:
                results  = send_renewal_reminders(df, days_before=days_before)
                sent     = [r for r in results if r["status"] == "sent"]
                skipped  = [r for r in results if r["status"] == "skipped"]
                failed   = [r for r in results if r["status"] == "failed"]
                no_phone = [r for r in results if r["status"] == "no_phone"]
                if results:
                    st.success(f"✅ تم الإرسال: {len(sent)} | تم التخطي: {len(skipped)} | لا يوجد رقم: {len(no_phone)} | فشل: {len(failed)}")
                    if sent:
                        with st.expander("📋 تفاصيل الرسائل المرسلة"):
                            for r in sent:
                                st.markdown(f"✅ **{r['customer']}** — {r['contract_no']} — {r['phone']}")
                    if failed:
                        with st.expander("❌ الرسائل الفاشلة"):
                            for r in failed:
                                st.markdown(f"❌ **{r['customer']}** — {r.get('error','خطأ غير معروف')}")
                else:
                    st.info(f"لا توجد عقود تنتهي خلال {days_before} يوماً القادمة.")
            else:
                st.warning("لا توجد بيانات عقود.")

        st.markdown("---")

    # PDF export
    if is_admin():
        section_header("📄 تصدير التقرير الشهري")
        pdf_col1, pdf_col2 = st.columns([2, 1])
        with pdf_col1:
            month_label = st.text_input("الفترة الزمنية للتقرير", value=date.today().strftime("%B %Y"), key="pdf_month")
        with pdf_col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("📥 توليد تقرير PDF", type="primary", use_container_width=True):
                pdf_bytes = generate_monthly_pdf(df, work_orders, month_label)
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ تحميل التقرير",
                        data=pdf_bytes,
                        file_name=f"lifttech_report_{date.today()}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                else:
                    st.warning("⚠️ تعذّر توليد PDF. يرجى التأكد من تثبيت: reportlab, arabic-reshaper, python-bidi")

        st.markdown("---")

    # Last 10 contracts
    section_header("🆕 آخر 10 عقود مضافة")
    if not df.empty:
        last10 = df.head(10)
        display_cols = ["contract_no","customer_name","building_name","elevator_count","contract_value","payment_display","created_at"]
        existing_cols = [c for c in display_cols if c in last10.columns]
        col_rename = {
            "contract_no": "رقم العقد", "customer_name": "اسم العميل",
            "building_name": "اسم المبنى", "elevator_count": "عدد المصاعد",
            "contract_value": "قيمة العقد", "payment_display": "حالة السداد",
            "created_at": "تاريخ الإضافة",
        }
        st.dataframe(last10[existing_cols].rename(columns=col_rename), use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد عقود.")

# ─────────────────────────────────────────────
# TAB 2: Contracts
# ─────────────────────────────────────────────
def tab_contracts():
    if is_client():
        st.info("🔒 هذا القسم متاح للمدير والفنيين فقط.")
        return

    section_header("➕ إضافة عقد جديد")
    with st.form("new_contract_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            contract_no    = st.text_input("رقم العقد *")
            customer_name  = st.text_input("اسم العميل *")
            mobile         = st.text_input("رقم الجوال")
        with col2:
            building_name  = st.text_input("اسم المبنى")
            district       = st.text_input("الحي")
            city           = st.text_input("المدينة")
        with col3:
            elevator_count = st.number_input("عدد المصاعد", min_value=1, value=1)
            elevator_type  = st.selectbox("نوع المصعد", ["ركاب","شحن","بانوراما","خدمة","سلم كهربائي"])
            elevator_brand = st.text_input("ماركة المصعد")

        col4, col5, col6 = st.columns(3)
        with col4:
            contract_value = st.number_input("قيمة العقد (ر.س)", min_value=0.0, step=100.0)
            start_date     = st.date_input("تاريخ البداية", value=date.today())
        with col5:
            end_date       = st.date_input("تاريخ الانتهاء", value=date.today() + timedelta(days=365))
            payment_status = st.selectbox("حالة السداد", ["unpaid","partial","paid"],
                                          format_func=lambda x: {"unpaid":"غير مسدد","partial":"جزئي","paid":"مسدد"}[x])
        with col6:
            contract_status = st.selectbox("حالة العقد", ["active","expired","cancelled"],
                                           format_func=lambda x: {"active":"نشط","expired":"منتهي","cancelled":"ملغي"}[x])
            collector       = st.text_input("المحصل")

        notes  = st.text_area("ملاحظات", height=80)
        submit = st.form_submit_button("💾 حفظ العقد", use_container_width=True)

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

    # View / Search
    section_header("🔍 عرض وبحث العقود")
    contracts = load_contracts()
    df = prepare_contracts_df(contracts)

    if df.empty:
        st.info("لا توجد عقود مسجلة.")
        return

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        search_name = st.text_input("بحث باسم العميل / رقم العقد", key="search_contract")
    with fcol2:
        filter_payment = st.selectbox("حالة السداد", ["الكل","مسدد","جزئي","غير مسدد"], key="fp_contract")
    with fcol3:
        filter_status = st.selectbox("حالة العقد", ["الكل","نشط","ينتهي قريباً","منتهي"], key="fs_contract")

    filtered = df.copy()
    if search_name.strip():
        mask = (filtered["customer_name"].str.contains(search_name.strip(), case=False, na=False) |
                filtered["contract_no"].str.contains(search_name.strip(), case=False, na=False))
        filtered = filtered[mask]
    if filter_payment != "الكل":
        filtered = filtered[filtered["payment_display"] == filter_payment]
    if filter_status != "الكل":
        filtered = filtered[filtered["status_display"] == filter_status]

    st.write(f"عدد النتائج: **{len(filtered)}** عقد")

    _drop = [c for c in ["days_remaining","status_display","payment_display","contract_value_num",
                          "elevator_count_num","start_date_dt","end_date_dt","days_to_end"] if c in filtered.columns]
    csv_bytes = to_csv_bytes(filtered.drop(columns=_drop))
    st.download_button("⬇️ تصدير CSV", data=csv_bytes, file_name="contracts.csv", mime="text/csv")

    display_cols = ["contract_no","customer_name","mobile","building_name","district",
                    "elevator_count","contract_value","payment_display","status_display","end_date","days_remaining"]
    existing = [c for c in display_cols if c in filtered.columns]
    col_rename = {
        "contract_no": "رقم العقد", "customer_name": "اسم العميل", "mobile": "الجوال",
        "building_name": "اسم المبنى", "district": "الحي", "elevator_count": "المصاعد",
        "contract_value": "القيمة", "payment_display": "السداد", "status_display": "الحالة",
        "end_date": "الانتهاء", "days_remaining": "الأيام المتبقية",
    }
    st.dataframe(filtered[existing].rename(columns=col_rename), use_container_width=True, hide_index=True)

    # Edit contract — admin only
    if is_admin():
        section_header("✏️ تعديل عقد")
        edit_opts = {f"{c.get('contract_no','—')} – {c.get('customer_name','—')}": c.get("id") for c in contracts}
        selected_edit_label = st.selectbox("اختر العقد للتعديل", ["-- اختر --"] + list(edit_opts.keys()), key="edit_contract_select")
        if selected_edit_label != "-- اختر --":
            selected_id = edit_opts.get(selected_edit_label)
            matched = [c for c in contracts if c.get("id") == selected_id]
            if matched:
                ec = matched[0]
                with st.form("edit_contract_form"):
                    ec1, ec2, ec3 = st.columns(3)
                    with ec1:
                        e_mobile    = st.text_input("رقم الجوال", value=safe_text(ec.get("mobile")))
                        e_district  = st.text_input("الحي", value=safe_text(ec.get("district")))
                    with ec2:
                        e_end_date  = st.date_input("تاريخ الانتهاء",
                                                     value=parse_date_safe(ec.get("end_date")) or date.today())
                        e_payment   = st.selectbox("حالة السداد", ["unpaid","partial","paid"],
                                                   format_func=lambda x: {"unpaid":"غير مسدد","partial":"جزئي","paid":"مسدد"}[x],
                                                   index=["unpaid","partial","paid"].index(ec.get("payment_status","unpaid"))
                                                         if ec.get("payment_status") in ["unpaid","partial","paid"] else 0)
                    with ec3:
                        e_status    = st.selectbox("حالة العقد", ["active","expired","cancelled"],
                                                   format_func=lambda x: {"active":"نشط","expired":"منتهي","cancelled":"ملغي"}[x],
                                                   index=["active","expired","cancelled"].index(ec.get("contract_status","active"))
                                                         if ec.get("contract_status") in ["active","expired","cancelled"] else 0)
                        e_value     = st.number_input("قيمة العقد", value=safe_number(ec.get("contract_value")), step=100.0)
                    e_notes         = st.text_area("ملاحظات", value=safe_text(ec.get("notes")), height=80)
                    e_submit        = st.form_submit_button("💾 حفظ التعديلات", use_container_width=True)

                if e_submit:
                    try:
                        supabase.table("contracts").update({
                            "mobile": e_mobile.strip(), "district": e_district.strip(),
                            "end_date": str(e_end_date), "payment_status": e_payment,
                            "contract_status": e_status, "contract_value": float(e_value),
                            "notes": e_notes.strip(),
                        }).eq("id", selected_id).execute()
                        load_contracts.clear()
                        st.success("✅ تم حفظ التعديلات")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")

# ─────────────────────────────────────────────
# TAB 3: Work Orders
# ─────────────────────────────────────────────
def tab_work_orders():
    contracts = load_contracts()

    # Filter for tech — show only their orders
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
                wo_description = st.text_area("الوصف التفصيلي", height=100)
                wo_work_type   = st.selectbox("نوع العمل",
                    ["preventive","corrective","emergency","inspection"],
                    format_func=lambda x: {"preventive":"وقائي","corrective":"تصحيحي",
                                            "emergency":"طارئ","inspection":"فحص"}[x])
            with wc2:
                wo_priority = st.selectbox("الأولوية",
                    ["low","medium","high","urgent"],
                    format_func=lambda x: {"low":"منخفضة","medium":"متوسطة","high":"عالية","urgent":"عاجلة"}[x],
                    index=1)
                wo_technician     = st.selectbox("الفني المسؤول", TECHNICIANS)
                wo_scheduled_date = st.date_input("التاريخ المجدول", value=date.today())
                wo_status         = st.selectbox("الحالة الابتدائية", ["pending","in_progress"],
                    format_func=lambda x: {"pending":"معلق","in_progress":"جاري"}[x])

            wo_submit = st.form_submit_button("💾 حفظ أمر العمل", use_container_width=True)

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
                    # Find contract info for WhatsApp
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

                    # WhatsApp notification to technician
                    wa_result = notify_technician_whatsapp(
                        wo_technician, wo_title.strip(), str(wo_scheduled_date),
                        c_no, c_bldg, wo_priority
                    )
                    if wa_result.get("ok"):
                        st.success(f"✅ تم حفظ أمر العمل وإرسال إشعار واتساب للفني {wo_technician}")
                    else:
                        st.success("✅ تم حفظ أمر العمل")
                        if wa_result.get("error") and "لا يوجد رقم" not in wa_result.get("error",""):
                            st.info(f"📱 إشعار واتساب: {wa_result.get('error','')}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    # View work orders
    section_header("📋 عرض أوامر العمل")
    work_orders = load_work_orders()

    if not work_orders:
        st.info("لا توجد أوامر عمل.")
        return

    wo_df = pd.DataFrame(work_orders)

    # Filter for technician role
    if tech_name and tech_name in TECHNICIANS:
        wo_df = wo_df[wo_df["technician"] == tech_name]

    # Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1: metric_card("معلق",   len(wo_df[wo_df["status"] == "pending"]),     "⏳", "warning")
    with s2: metric_card("جاري",   len(wo_df[wo_df["status"] == "in_progress"]), "🔄", "info")
    with s3: metric_card("مكتمل",  len(wo_df[wo_df["status"] == "completed"]),   "✅", "success")
    with s4: metric_card("ملغي",   len(wo_df[wo_df["status"] == "cancelled"]),   "❌", "danger")

    # Filters
    wf1, wf2, wf3 = st.columns(3)
    with wf1:
        filter_wo_status = st.selectbox("فلترة بالحالة",
            ["الكل","معلق","جاري","مكتمل","ملغي"], key="wo_status_filter")
    with wf2:
        filter_wo_priority = st.selectbox("فلترة بالأولوية",
            ["الكل","عاجلة","عالية","متوسطة","منخفضة"], key="wo_priority_filter")
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

    # Update status
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
                            format_func=lambda x: {"pending":"معلق","in_progress":"جاري",
                                                    "completed":"مكتمل","cancelled":"ملغي"}[x])
                    with u2:
                        wo_notes = st.text_area("ملاحظات الإغلاق", height=80)
                    wo_update_submit = st.form_submit_button("💾 تحديث", use_container_width=True)

                if wo_update_submit and supabase:
                    try:
                        upd = {"status": new_wo_status}
                        if wo_notes.strip():
                            upd["notes"] = wo_notes.strip()
                        if new_wo_status == "completed":
                            upd["completed_at"] = datetime.now().isoformat()
                        supabase.table("work_orders").update(upd).eq("id", selected_wo_id).execute()
                        load_work_orders.clear()
                        st.success("✅ تم التحديث")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")

# ─────────────────────────────────────────────
# TAB 4: Fault Reports
# ─────────────────────────────────────────────
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
            fr_submit = st.form_submit_button("💾 حفظ البلاغ", use_container_width=True)

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
                        "contract_id": contract_id, "customer_name": fr_customer_name.strip(),
                        "mobile": fr_mobile.strip(), "building_name": fr_building_name.strip(),
                        "fault_description": fr_fault_description.strip(),
                        "priority": fr_priority, "status": status_val, "assigned_technician": tech_val,
                    }
                    supabase.table("fault_reports").insert(payload).execute()
                    load_fault_reports.clear()

                    # Notify tech
                    if tech_val:
                        _c_no  = contract_id and [c.get("contract_no","—") for c in contracts if c.get("id")==contract_id]
                        notify_technician_whatsapp(
                            tech_val, f"بلاغ عطل: {fr_fault_description.strip()[:60]}",
                            str(date.today()),
                            _c_no[0] if _c_no else "—", fr_building_name.strip(), fr_priority
                        )
                    st.success("✅ تم حفظ البلاغ بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    section_header("📋 عرض البلاغات")
    fault_reports = load_fault_reports()
    if not fault_reports:
        st.info("لا توجد بلاغات.")
        return

    fr_df = pd.DataFrame(fault_reports)

    # Filter for client
    if is_client():
        cc = st.session_state.get("client_contract","")
        if cc:
            _id_to_cno = id_to_contract_no_map(contracts)
            fr_df["_cno"] = fr_df["contract_id"].astype(str).map(_id_to_cno).fillna("")
            fr_df = fr_df[fr_df["_cno"] == cc]

    # Filter for tech
    if is_tech():
        tn = st.session_state.get("display_name","")
        if tn:
            fr_df = fr_df[fr_df["assigned_technician"] == tn]

    s1, s2, s3, s4 = st.columns(4)
    with s1: metric_card("مفتوح",  len(fr_df[fr_df["status"]=="open"]),        "🔴","danger")
    with s2: metric_card("مكلف",   len(fr_df[fr_df["status"]=="assigned"]),     "🟡","warning")
    with s3: metric_card("جاري",   len(fr_df[fr_df["status"]=="in_progress"]),  "🔵","info")
    with s4: metric_card("محلول",  len(fr_df[fr_df["status"]=="resolved"]),     "🟢","success")

    ff1, ff2 = st.columns(2)
    with ff1:
        filter_fr_status = st.selectbox("فلترة بالحالة",
            ["الكل","مفتوح","مكلف","جاري","محلول","مغلق"], key="fr_status_filter")
    with ff2:
        filter_fr_priority = st.selectbox("فلترة بالأولوية",
            ["الكل","عاجلة","عالية","متوسطة","منخفضة"], key="fr_priority_filter")

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
        show_cols = ["customer_name","building_name","fault_description","الأولوية","الحالة","assigned_technician","created_at"]
        existing_show = [c for c in show_cols if c in display_fr.columns]
        col_rename_fr = {"customer_name":"اسم العميل","building_name":"اسم المبنى",
                         "fault_description":"وصف العطل","assigned_technician":"الفني المكلف","created_at":"تاريخ البلاغ"}
        st.dataframe(display_fr[existing_show].rename(columns=col_rename_fr), use_container_width=True, hide_index=True)

    if not is_client():
        section_header("🔄 تحديث حالة البلاغ")
        if not fr_filtered.empty:
            fr_opts = {
                f"{row.get('customer_name','—')} – {str(row.get('fault_description',''))[:40]} (#{row.get('id','')})": row.get("id")
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
                            format_func=lambda x: {"open":"مفتوح","assigned":"مكلف",
                                                    "in_progress":"جاري","resolved":"محلول","closed":"مغلق"}[x])
                        new_fr_tech = st.text_input("الفني المكلف")
                    with uc2:
                        resolution_notes = st.text_area("ملاحظات الحل", height=80)
                    fr_update_submit = st.form_submit_button("💾 تحديث البلاغ", use_container_width=True)

                if fr_update_submit and supabase:
                    try:
                        upd = {"status": new_fr_status, "resolution_notes": resolution_notes.strip()}
                        if new_fr_tech.strip(): upd["assigned_technician"] = new_fr_tech.strip()
                        if new_fr_status in ("resolved","closed"): upd["resolved_at"] = datetime.now().isoformat()
                        supabase.table("fault_reports").update(upd).eq("id", selected_fr_id).execute()
                        load_fault_reports.clear()
                        st.success("✅ تم تحديث البلاغ")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء التحديث: {e}")

# ─────────────────────────────────────────────
# TAB 5: Maintenance Logs
# ─────────────────────────────────────────────
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
            ml_submit = st.form_submit_button("💾 حفظ سجل الصيانة", use_container_width=True)

        if ml_submit:
            if not ml_work_done.strip():
                st.error("❌ الأعمال المنجزة مطلوبة")
            elif supabase is None:
                st.error("❌ لا يوجد اتصال بقاعدة البيانات")
            else:
                try:
                    payload = {
                        "contract_id": contract_options.get(selected_contract_label),
                        "elevator_no": ml_elevator_no.strip(), "visit_date": str(ml_visit_date),
                        "technician": ml_technician, "work_done": ml_work_done.strip(),
                        "parts_replaced": ml_parts.strip(), "next_visit_date": str(ml_next_visit),
                        "condition": ml_condition, "notes": ml_notes.strip(),
                    }
                    supabase.table("maintenance_logs").insert(payload).execute()
                    load_maintenance_logs.clear()
                    st.success("✅ تم حفظ سجل الصيانة بنجاح")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ أثناء الحفظ: {e}")

    section_header("📋 عرض سجل الصيانة")
    maintenance_logs = load_maintenance_logs()
    if not maintenance_logs:
        st.info("لا توجد سجلات صيانة.")
        return

    ml_df = pd.DataFrame(maintenance_logs)

    mf1, mf2, mf3 = st.columns(3)
    with mf1:
        tech_list_ml = ["الكل"] + sorted(ml_df["technician"].dropna().unique().tolist())
        filter_ml_tech = st.selectbox("فلترة بالفني", tech_list_ml, key="ml_tech_filter")
    with mf2:
        filter_ml_condition = st.selectbox("فلترة بحالة المصعد",
            ["الكل","جيد","متوسط","سيء"], key="ml_condition_filter")
    with mf3:
        search_ml_contract = st.text_input("بحث برقم العقد", key="ml_contract_search")

    filtered_ml = ml_df.copy()
    condition_reverse = {"جيد":"good","متوسط":"fair","سيء":"poor"}
    if filter_ml_tech != "الكل":
        filtered_ml = filtered_ml[filtered_ml["technician"] == filter_ml_tech]
    if filter_ml_condition != "الكل":
        filtered_ml = filtered_ml[filtered_ml["condition"] == condition_reverse.get(filter_ml_condition,"")]
    if search_ml_contract.strip():
        _id_to_cno = id_to_contract_no_map(contracts)
        filtered_ml["_cno"] = filtered_ml["contract_id"].astype(str).map(_id_to_cno).fillna("")
        filtered_ml = filtered_ml[
            filtered_ml["_cno"].str.contains(search_ml_contract.strip(), case=False, na=False)
        ]

    st.write(f"عدد السجلات: **{len(filtered_ml)}**")
    if not filtered_ml.empty:
        display_ml = filtered_ml.copy()
        cond_map = {"good":"جيد","fair":"متوسط","poor":"سيء"}
        display_ml["حالة المصعد"] = display_ml["condition"].map(cond_map).fillna(display_ml["condition"])
        _id_to_cno2 = id_to_contract_no_map(contracts)
        display_ml["رقم العقد"] = display_ml["contract_id"].astype(str).map(_id_to_cno2).fillna("—")
        show_cols = ["رقم العقد","elevator_no","visit_date","technician","work_done","parts_replaced","حالة المصعد","next_visit_date"]
        existing_show = [c for c in show_cols if c in display_ml.columns]
        col_rename_ml = {"elevator_no":"رقم المصعد","visit_date":"تاريخ الزيارة",
                         "technician":"الفني","work_done":"الأعمال المنجزة",
                         "parts_replaced":"قطع الغيار","next_visit_date":"الزيارة القادمة"}
        st.dataframe(display_ml[existing_show].rename(columns=col_rename_ml), use_container_width=True, hide_index=True)

        section_header("🔍 تفاصيل الزيارات")
        for _, row in filtered_ml.head(20).iterrows():
            visit_date_str = safe_text(row.get("visit_date"), "—")
            tech_str       = safe_text(row.get("technician"), "—")
            cond_str       = cond_map.get(safe_text(row.get("condition")), "—")
            with st.expander(f"زيارة {visit_date_str} – فني: {tech_str} – الحالة: {cond_str}"):
                d1, d2 = st.columns(2)
                with d1:
                    st.write(f"**رقم المصعد:** {safe_text(row.get('elevator_no'),'—')}")
                    st.write(f"**الأعمال المنجزة:** {safe_text(row.get('work_done'),'—')}")
                    st.write(f"**قطع الغيار:** {safe_text(row.get('parts_replaced'),'—')}")
                with d2:
                    st.write(f"**الزيارة القادمة:** {safe_text(row.get('next_visit_date'),'—')}")
                    st.write(f"**ملاحظات:** {safe_text(row.get('notes'),'—')}")

# ─────────────────────────────────────────────
# TAB 6: Elevators
# ─────────────────────────────────────────────
def tab_elevators():
    contracts = load_contracts()
    maintenance_logs = load_maintenance_logs()

    section_header("🛗 إدارة المصاعد")
    st.markdown("""
    <div style='background:#dbeafe;border-right:4px solid #3b82f6;padding:10px 16px;border-radius:8px;margin-bottom:16px;color:#1e3a5f'>
        يعرض هذا القسم جميع المصاعد المرتبطة بالعقود مع آخر سجل صيانة وحالتها الحالية.
    </div>
    """, unsafe_allow_html=True)

    if not contracts:
        st.info("لا توجد عقود.")
        return

    # Build elevators list from contracts
    elevators = []
    for c in contracts:
        count      = safe_int(c.get("elevator_count"), 1)
        c_no       = safe_text(c.get("contract_no"), "—")
        c_id       = c.get("id")
        customer   = safe_text(c.get("customer_name"), "—")
        building   = safe_text(c.get("building_name"), "—")
        e_type     = safe_text(c.get("elevator_type"), "—")
        e_brand    = safe_text(c.get("elevator_brand"), "—")
        for i in range(1, count + 1):
            elevators.append({
                "contract_id": c_id, "contract_no": c_no,
                "customer": customer, "building": building,
                "elevator_no": str(i), "type": e_type, "brand": e_brand,
            })

    # Build last maintenance map: (contract_id, elevator_no) → last log
    ml_map = {}
    for log in maintenance_logs:
        key = (str(log.get("contract_id","")), str(log.get("elevator_no","")))
        existing = ml_map.get(key)
        if existing is None:
            ml_map[key] = log
        else:
            # Keep most recent
            try:
                if log.get("visit_date","") > existing.get("visit_date",""):
                    ml_map[key] = log
            except Exception:
                pass

    # Filters
    ef1, ef2, ef3 = st.columns(3)
    with ef1:
        search_elev = st.text_input("بحث بالعقد أو المبنى أو العميل", key="elev_search")
    with ef2:
        filter_elev_condition = st.selectbox("فلترة بحالة المصعد",
            ["الكل","جيد","متوسط","سيء","لم يُصان"], key="elev_condition")
    with ef3:
        filter_elev_type = st.selectbox("فلترة بنوع المصعد",
            ["الكل"] + sorted(list({e["type"] for e in elevators if e["type"] != "—"})), key="elev_type")

    cond_map = {"good":"جيد","fair":"متوسط","poor":"سيء"}

    # Display
    filtered_elev = elevators
    if search_elev.strip():
        q = search_elev.strip().lower()
        filtered_elev = [e for e in filtered_elev if
            q in e["contract_no"].lower() or q in e["building"].lower() or q in e["customer"].lower()]
    if filter_elev_type != "الكل":
        filtered_elev = [e for e in filtered_elev if e["type"] == filter_elev_type]

    cond_filter_val = {"جيد":"good","متوسط":"fair","سيء":"poor"}.get(filter_elev_condition)

    # Apply condition filter BEFORE render loop (fixes col_idx misalignment bug)
    if filter_elev_condition != "الكل":
        def _cond_match(e):
            key = (str(e["contract_id"]), e["elevator_no"])
            log = ml_map.get(key)
            cond = log.get("condition", "") if log else ""
            if filter_elev_condition == "لم يُصان":
                return not log
            return cond == cond_filter_val
        filtered_elev = [e for e in filtered_elev if _cond_match(e)]

    st.markdown(f"**إجمالي المصاعد: {len(filtered_elev)}**")
    st.markdown("---")

    # Stats cards
    total_elev  = len(filtered_elev)
    good_count  = 0
    fair_count  = 0
    poor_count  = 0
    no_maint    = 0

    for e in filtered_elev:
        key  = (str(e["contract_id"]), e["elevator_no"])
        log  = ml_map.get(key)
        cond = log.get("condition","") if log else ""
        if not log: no_maint += 1
        elif cond == "good":  good_count += 1
        elif cond == "fair":  fair_count += 1
        elif cond == "poor":  poor_count += 1

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1: metric_card("حالة جيدة",   good_count, "🟢", "success")
    with sc2: metric_card("حالة متوسطة", fair_count, "🟡", "warning")
    with sc3: metric_card("حالة سيئة",   poor_count, "🔴", "danger")
    with sc4: metric_card("لم يُصان",    no_maint,   "⚪", "info")

    st.markdown("---")

    # Cards display
    cols_per_row = 3
    col_list = st.columns(cols_per_row)
    col_idx  = 0

    for e in filtered_elev:
        key  = (str(e["contract_id"]), e["elevator_no"])
        log  = ml_map.get(key)
        cond = log.get("condition","") if log else ""
        cond_ar = cond_map.get(cond, "لم يُصان بعد")

        last_visit   = safe_text(log.get("visit_date"), "—") if log else "لا يوجد"
        next_visit   = safe_text(log.get("next_visit_date"), "—") if log else "—"
        technician   = safe_text(log.get("technician"), "—") if log else "—"
        cond_class   = cond if cond in ("good","fair","poor") else "fair"

        # Days until next visit
        next_dt = parse_date_safe(next_visit) if log else None
        days_next = (next_dt - date.today()).days if next_dt else None
        next_label = f"{days_next} يوم" if days_next is not None else "—"
        next_color = "#ef4444" if days_next is not None and days_next <= 7 else ("#f59e0b" if days_next is not None and days_next <= 30 else "#22c55e")

        with col_list[col_idx % cols_per_row]:
            st.markdown(f"""
            <div class="elev-card {cond_class}">
                <div style="font-weight:700;font-size:1rem;margin-bottom:6px">
                    🛗 مصعد #{e['elevator_no']} — {e['building']}
                </div>
                <div style="font-size:0.82rem;color:#475569;margin-bottom:4px">
                    📋 {e['contract_no']} | 👤 {e['customer']}
                </div>
                <div style="font-size:0.82rem;color:#475569;margin-bottom:4px">
                    نوع: {e['type']} | ماركة: {e['brand']}
                </div>
                <div style="font-size:0.82rem;margin-bottom:2px">
                    الحالة: <strong>{cond_ar}</strong>
                </div>
                <div style="font-size:0.82rem;margin-bottom:2px">
                    آخر صيانة: <strong>{last_visit}</strong> | الفني: {technician}
                </div>
                <div style="font-size:0.82rem">
                    الزيارة القادمة: <strong style="color:{next_color}">{next_visit}</strong>
                    {"(" + next_label + ")" if days_next is not None else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
        col_idx += 1

# ─────────────────────────────────────────────
# TAB 7: Maintenance Calendar
# ─────────────────────────────────────────────
def tab_calendar():
    maintenance_logs = load_maintenance_logs()
    work_orders      = load_work_orders()
    contracts        = load_contracts()

    section_header("📅 تقويم الصيانة الدورية")

    today      = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday

    # Navigation
    nav1, nav2, nav3 = st.columns([1, 4, 1])
    with nav1:
        if st.button("◀ الأسبوع السابق", key="cal_prev"):
            if "cal_offset" not in st.session_state:
                st.session_state.cal_offset = 0
            st.session_state.cal_offset -= 7
    with nav3:
        if st.button("الأسبوع التالي ▶", key="cal_next"):
            if "cal_offset" not in st.session_state:
                st.session_state.cal_offset = 0
            st.session_state.cal_offset += 7

    offset     = st.session_state.get("cal_offset", 0)
    week_start = week_start + timedelta(days=offset)
    week_end   = week_start + timedelta(days=6)

    with nav2:
        st.markdown(f"<div style='text-align:center;font-weight:700;font-size:1.1rem;padding:8px'>"
                    f"الأسبوع: {week_start.strftime('%Y-%m-%d')} → {week_end.strftime('%Y-%m-%d')}"
                    f"</div>", unsafe_allow_html=True)

    # Build events
    id_to_cno = id_to_contract_no_map(contracts)

    events_by_day = {week_start + timedelta(days=i): [] for i in range(7)}

    # Next visit dates from maintenance logs
    for log in maintenance_logs:
        nv = parse_date_safe(log.get("next_visit_date"))
        if nv and week_start <= nv <= week_end:
            c_no = id_to_cno.get(str(log.get("contract_id","")), "—")
            events_by_day[nv].append({
                "label": f"🔧 صيانة دورية – {c_no} – مصعد {safe_text(log.get('elevator_no'),'—')}",
                "type": "preventive", "tech": safe_text(log.get("technician"),"—"),
            })

    # Work orders scheduled dates
    for wo in work_orders:
        sd = parse_date_safe(wo.get("scheduled_date"))
        if sd and week_start <= sd <= week_end and wo.get("status") not in ("completed","cancelled"):
            c_no = id_to_cno.get(str(wo.get("contract_id","")), "—")
            evt_type = "urgent" if wo.get("priority") in ("urgent","high") else "preventive"
            events_by_day[sd].append({
                "label": f"⚙️ {safe_text(wo.get('title'),'أمر عمل')} – {c_no}",
                "type": evt_type, "tech": safe_text(wo.get("technician"),"—"),
            })

    # Display 7 columns
    day_names_ar = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    cols = st.columns(7)
    for i, (day, events) in enumerate(events_by_day.items()):
        with cols[i]:
            is_today = (day == today)
            header_color = "#3b82f6" if is_today else "#64748b"
            bg_color     = "#eff6ff" if is_today else "white"
            st.markdown(f"""
            <div class="cal-day" style="background:{bg_color}">
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
                st.markdown('<div style="color:#cbd5e1;font-size:0.78rem;text-align:center;padding-top:10px">لا توجد مهام</div>',
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Upcoming next visits table
    st.markdown("---")
    section_header("📋 الزيارات القادمة خلال 30 يوماً")
    upcoming = []
    for log in maintenance_logs:
        nv = parse_date_safe(log.get("next_visit_date"))
        if nv and today <= nv <= today + timedelta(days=30):
            c_no = id_to_cno.get(str(log.get("contract_id","")), "—")
            days_left = (nv - today).days
            upcoming.append({
                "رقم العقد": c_no,
                "رقم المصعد": safe_text(log.get("elevator_no"),"—"),
                "تاريخ الزيارة": str(nv),
                "الأيام المتبقية": days_left,
                "الفني": safe_text(log.get("technician"),"—"),
            })

    if upcoming:
        upcoming_df = pd.DataFrame(upcoming).sort_values("الأيام المتبقية")
        st.dataframe(upcoming_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ لا توجد زيارات صيانة مجدولة خلال 30 يوماً")

# ─────────────────────────────────────────────
# TAB 8: Technicians & Scheduling
# ─────────────────────────────────────────────
def tab_technicians():
    if is_client():
        st.info("🔒 هذا القسم متاح للمدير والفنيين فقط.")
        return

    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    contracts     = load_contracts()

    technicians = TECHNICIANS

    section_header("👷 إحصائيات الفنيين")

    wo_df = pd.DataFrame(work_orders) if work_orders else pd.DataFrame(columns=["technician","status","scheduled_date"])
    fr_df = pd.DataFrame(fault_reports) if fault_reports else pd.DataFrame(columns=["assigned_technician","status"])

    today       = date.today()
    month_start = today.replace(day=1)

    tech_cols = st.columns(len(technicians))
    for idx, tech in enumerate(technicians):
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

            tech_fr = fr_df[fr_df["assigned_technician"] == tech] if not fr_df.empty else pd.DataFrame()
            assigned_faults = len(tech_fr[tech_fr["status"].isin(["assigned","in_progress"])]) if not tech_fr.empty else 0

            st.markdown(f"""
            <div class="tech-card">
              <h3>👷 {tech}</h3>
              <div class="tech-stat"><span>أوامر العمل المعلقة</span><span>{pending_count}</span></div>
              <div class="tech-stat"><span>مكتملة هذا الشهر</span><span>{completed_this_month}</span></div>
              <div class="tech-stat"><span>بلاغات مكلف بها</span><span>{assigned_faults}</span></div>
            </div>
            """, unsafe_allow_html=True)

    # Next week schedule
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

    # Quick add task
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
        qt_submit = st.form_submit_button("⚡ إضافة المهمة", use_container_width=True)

    if qt_submit:
        if not qt_description.strip():
            st.error("❌ وصف المهمة مطلوب")
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                c_id = contract_options.get(qt_contract)
                matched_c = [c for c in contracts if c.get("id") == c_id]
                c_no   = matched_c[0].get("contract_no","—") if matched_c else "—"
                c_bldg = matched_c[0].get("building_name","—") if matched_c else "—"

                payload = {
                    "contract_id": c_id, "title": qt_description.strip()[:100],
                    "description": qt_description.strip(), "technician": qt_tech,
                    "scheduled_date": str(qt_date), "status": "pending",
                    "priority": qt_priority, "work_type": "preventive",
                }
                supabase.table("work_orders").insert(payload).execute()
                load_work_orders.clear()

                notify_technician_whatsapp(qt_tech, qt_description.strip()[:60],
                                           str(qt_date), c_no, c_bldg, qt_priority)
                st.success("✅ تمت إضافة المهمة بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الإضافة: {e}")

# ─────────────────────────────────────────────
# Main app
# ─────────────────────────────────────────────
def main():
    role = get_role()

    # Header
    role_ar  = {"admin":"مدير عام","manager":"مدير","tech":"فني","client":"عميل"}.get(role, role)
    role_cls = f"role-{role}"
    st.markdown(f"""
    <div class="app-header">
      <div>
        <h1>🛗 LiftTech V5.1</h1>
        <p>نظام إدارة شركة صيانة المصاعد – مرحباً {st.session_state.get('display_name', st.session_state.username)}</p>
      </div>
      <div style="text-align:left; display:flex; flex-direction:column; align-items:flex-end; gap:6px">
        <span class="{role_cls}">{role_ar}</span>
        <span style="opacity:0.7; font-size:0.82rem;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_spacer, col_logout = st.columns([10, 1])
    with col_logout:
        if st.button("خروج", type="secondary"):
            for key in ["logged_in","username","role","display_name","client_contract"]:
                st.session_state.pop(key, None)
            st.rerun()

    # Tabs based on role
    if is_admin() or is_manager():
        tab_labels = ["📊 لوحة التحكم","📋 العقود","🔧 أوامر العمل",
                      "🚨 البلاغات","📝 سجل الصيانة","🛗 المصاعد","📅 التقويم","👷 الفنيون"]
        tabs = st.tabs(tab_labels)
        with tabs[0]: tab_dashboard()
        with tabs[1]: tab_contracts()
        with tabs[2]: tab_work_orders()
        with tabs[3]: tab_fault_reports()
        with tabs[4]: tab_maintenance_logs()
        with tabs[5]: tab_elevators()
        with tabs[6]: tab_calendar()
        with tabs[7]: tab_technicians()

    elif is_tech():
        tab_labels = ["📊 لوحتي","🔧 أوامر عملي","🚨 بلاغاتي","📝 سجل الصيانة","📅 التقويم"]
        tabs = st.tabs(tab_labels)
        with tabs[0]: tab_dashboard()
        with tabs[1]: tab_work_orders()
        with tabs[2]: tab_fault_reports()
        with tabs[3]: tab_maintenance_logs()
        with tabs[4]: tab_calendar()

    elif is_client():
        tab_labels = ["📊 عقدي","🚨 بلاغاتي","📝 سجل الصيانة","🛗 مصاعدي"]
        tabs = st.tabs(tab_labels)
        with tabs[0]: tab_dashboard()
        with tabs[1]: tab_fault_reports()
        with tabs[2]: tab_maintenance_logs()
        with tabs[3]: tab_elevators()

if __name__ == "__main__":
    main()

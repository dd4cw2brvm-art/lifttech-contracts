import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import io

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LiftTech V4.0",
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

  /* hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 1400px !important; }

  /* ── App header ── */
  .app-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    color: white;
    padding: 1.2rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(15,23,42,0.25);
  }
  .app-header h1 { margin: 0; font-size: 1.8rem; font-weight: 800; }
  .app-header p  { margin: 0; font-size: 0.9rem; opacity: 0.75; }

  /* ── KPI cards ── */
  .kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-right: 5px solid #3b82f6;
    margin-bottom: 1rem;
    transition: transform 0.2s;
  }
  .kpi-card:hover { transform: translateY(-3px); }
  .kpi-card.danger  { border-right-color: #ef4444; }
  .kpi-card.success { border-right-color: #22c55e; }
  .kpi-card.warning { border-right-color: #f59e0b; }
  .kpi-card.info    { border-right-color: #3b82f6; }
  .kpi-card .kpi-icon { font-size: 2rem; float: left; }
  .kpi-card .kpi-value { font-size: 2rem; font-weight: 800; color: #0f172a; }
  .kpi-card .kpi-title { font-size: 0.85rem; color: #64748b; margin-top: 0.2rem; }

  /* ── Section header ── */
  .section-header {
    background: white;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    margin: 1.2rem 0 0.8rem 0;
    border-right: 4px solid #3b82f6;
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  }

  /* ── Alert banners ── */
  .alert-expired { background:#fef2f2; border-right:4px solid #ef4444; color:#991b1b; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-30      { background:#fff7ed; border-right:4px solid #f97316; color:#9a3412; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-60      { background:#fefce8; border-right:4px solid #eab308; color:#713f12; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }
  .alert-90      { background:#f0fdf4; border-right:4px solid #22c55e; color:#14532d; padding:0.6rem 1rem; border-radius:8px; margin-bottom:0.5rem; }

  /* ── Badges ── */
  .badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.78rem;
    font-weight: 700;
    white-space: nowrap;
  }
  /* Priority badges */
  .badge-urgent  { background:#fee2e2; color:#dc2626; }
  .badge-high    { background:#ffedd5; color:#ea580c; }
  .badge-medium  { background:#fef9c3; color:#ca8a04; }
  .badge-low     { background:#dcfce7; color:#16a34a; }
  /* Status badges */
  .badge-pending     { background:#f1f5f9; color:#475569; }
  .badge-in_progress { background:#dbeafe; color:#1d4ed8; }
  .badge-completed   { background:#dcfce7; color:#15803d; }
  .badge-cancelled   { background:#fee2e2; color:#b91c1c; }
  .badge-open        { background:#f1f5f9; color:#475569; }
  .badge-assigned    { background:#fef9c3; color:#92400e; }
  .badge-resolved    { background:#dcfce7; color:#15803d; }
  .badge-closed      { background:#e2e8f0; color:#334155; }

  /* ── Forms ── */
  .stTextInput > div > div > input,
  .stTextArea  > div > div > textarea,
  .stSelectbox > div > div > div,
  .stNumberInput > div > div > input,
  .stDateInput   > div > div > input {
    border-radius: 8px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
  }
  .stButton > button {
    border-radius: 8px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 10px;
    padding: 4px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    gap: 4px;
    flex-wrap: wrap;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    color: #475569 !important;
  }
  .stTabs [aria-selected="true"] {
    background: #3b82f6 !important;
    color: white !important;
  }

  /* ── Table improvements ── */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* ── Technician card ── */
  .tech-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 1rem;
    border-top: 4px solid #3b82f6;
  }
  .tech-card h3 { margin: 0 0 0.8rem 0; font-size: 1.1rem; color: #0f172a; }
  .tech-stat    { display: flex; justify-content: space-between; margin-bottom: 0.4rem; font-size: 0.9rem; }
  .tech-stat span { font-weight: 700; color: #3b82f6; }

  /* ── Login ── */
  .login-container {
    max-width: 420px;
    margin: 5rem auto;
    background: white;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    text-align: center;
  }
  .login-container h2 { color: #0f172a; margin-bottom: 0.4rem; }
  .login-container p  { color: #64748b; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Supabase init
# ─────────────────────────────────────────────
# ── قائمة الفنيين المركزية ──
TECHNICIANS = ["طه", "أحمد", "آخر"]
TECHNICIANS_WITH_UNASSIGNED = ["-- غير مكلف --"] + TECHNICIANS

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
# Authentication
# ─────────────────────────────────────────────
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        return True

    st.markdown("""
    <div class="login-container">
      <div style="font-size:3.5rem">🛗</div>
      <h2>LiftTech V4.0</h2>
      <p>نظام إدارة شركة صيانة المصاعد</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            submit = st.form_submit_button("دخول", use_container_width=True)

        if submit:
            try:
                users = st.secrets["users"]
                if username in users and users[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            except Exception:
                st.error("❌ لا توجد بيانات مستخدمين في الإعدادات")
    return False

if not check_login():
    st.stop()

# ─────────────────────────────────────────────
# Helper functions – text / number safety
# ─────────────────────────────────────────────
def safe_text(val, default=""):
    if val is None:
        return default
    return str(val).strip()

def safe_number(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default

def safe_int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

def parse_date_safe(val):
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val if isinstance(val, date) else val.date()
    try:
        return datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
    except Exception:
        return None

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    return buffer.getvalue()

# ─────────────────────────────────────────────
# Helper functions – UI components
# ─────────────────────────────────────────────
def metric_card(title, value, icon="📊", variant="info"):
    st.markdown(f"""
    <div class="kpi-card {variant}">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-value">{value}</div>
      <div class="kpi-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def priority_badge(priority):
    mapping = {
        "urgent": ("badge-urgent", "عاجلة"),
        "high":   ("badge-high",   "عالية"),
        "medium": ("badge-medium", "متوسطة"),
        "low":    ("badge-low",    "منخفضة"),
    }
    cls, label = mapping.get(priority, ("badge-low", priority or "—"))
    return f'<span class="badge {cls}">{label}</span>'

def status_badge(status):
    mapping = {
        "pending":     ("badge-pending",     "معلق"),
        "in_progress": ("badge-in_progress", "جاري"),
        "completed":   ("badge-completed",   "مكتمل"),
        "cancelled":   ("badge-cancelled",   "ملغي"),
        "open":        ("badge-open",        "مفتوح"),
        "assigned":    ("badge-assigned",    "مكلف"),
        "resolved":    ("badge-resolved",    "محلول"),
        "closed":      ("badge-closed",      "مغلق"),
    }
    cls, label = mapping.get(status, ("badge-pending", status or "—"))
    return f'<span class="badge {cls}">{label}</span>'

# ─────────────────────────────────────────────
# Data loaders
# ─────────────────────────────────────────────
def load_contracts():
    if supabase is None:
        return []
    try:
        resp = supabase.table("contracts").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل العقود: {e}")
        return []

def load_work_orders():
    if supabase is None:
        return []
    try:
        resp = supabase.table("work_orders").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل أوامر العمل: {e}")
        return []

def load_fault_reports():
    if supabase is None:
        return []
    try:
        resp = supabase.table("fault_reports").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل البلاغات: {e}")
        return []

def load_maintenance_logs():
    if supabase is None:
        return []
    try:
        resp = supabase.table("maintenance_logs").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل سجل الصيانة: {e}")
        return []

# ─────────────────────────────────────────────
# DataFrame preparation
# ─────────────────────────────────────────────
def prepare_contracts_df(contracts):
    if not contracts:
        return pd.DataFrame()
    df = pd.DataFrame(contracts)
    today = date.today()

    def compute_days(row):
        d = parse_date_safe(row.get("end_date"))
        if d is None:
            return None
        return (d - today).days

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

    df["status_display"] = df.apply(compute_status_display, axis=1)

    payment_map = {"paid": "مسدد", "partial": "جزئي", "unpaid": "غير مسدد"}
    df["payment_display"] = df["payment_status"].map(payment_map).fillna(df["payment_status"].fillna("—"))

    return df

# ─────────────────────────────────────────────
# Contract label helper
# ─────────────────────────────────────────────
def contract_label(c):
    no   = safe_text(c.get("contract_no"), "—")
    name = safe_text(c.get("customer_name"), "—")
    bldg = safe_text(c.get("building_name"), "")
    return f"{no} – {name}" + (f" ({bldg})" if bldg else "")

# ─────────────────────────────────────────────
# TAB 1: Dashboard
# ─────────────────────────────────────────────
def tab_dashboard():
    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()

    df = prepare_contracts_df(contracts)
    today = date.today()

    total_contracts   = len(df)
    total_value       = df["contract_value"].apply(safe_number).sum() if not df.empty else 0
    active_contracts  = len(df[df["status_display"] == "نشط"]) if not df.empty else 0
    unpaid_contracts  = len(df[df["payment_display"] == "غير مسدد"]) if not df.empty else 0
    total_elevators   = df["elevator_count"].apply(safe_int).sum() if not df.empty else 0

    # KPI row
    section_header("📊 مؤشرات الأداء الرئيسية")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("إجمالي العقود",    total_contracts,                "📄", "info")
    with c2:
        metric_card("القيمة الإجمالية", f"{total_value:,.0f} ر.س",     "💰", "success")
    with c3:
        metric_card("العقود النشطة",    active_contracts,               "✅", "success")
    with c4:
        metric_card("غير المسددة",      unpaid_contracts,               "⚠️", "danger")
    with c5:
        metric_card("إجمالي المصاعد",   total_elevators,                "🛗", "warning")

    # ── Renewal alerts ──
    section_header("🔔 تنبيهات التجديد")
    if not df.empty and "days_remaining" in df.columns:
        expired = df[df["days_remaining"].notna() & (df["days_remaining"] < 0)]
        exp_30  = df[df["days_remaining"].notna() & (df["days_remaining"] >= 0)  & (df["days_remaining"] <= 30)]
        exp_60  = df[df["days_remaining"].notna() & (df["days_remaining"] > 30)  & (df["days_remaining"] <= 60)]
        exp_90  = df[df["days_remaining"].notna() & (df["days_remaining"] > 60)  & (df["days_remaining"] <= 90)]

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.markdown(f'<div class="alert-expired">❌ منتهية: <strong>{len(expired)}</strong> عقد</div>', unsafe_allow_html=True)
        with a2:
            st.markdown(f'<div class="alert-30">🔴 خلال 30 يوم: <strong>{len(exp_30)}</strong> عقد</div>', unsafe_allow_html=True)
        with a3:
            st.markdown(f'<div class="alert-60">🟡 خلال 60 يوم: <strong>{len(exp_60)}</strong> عقد</div>', unsafe_allow_html=True)
        with a4:
            st.markdown(f'<div class="alert-90">🟢 خلال 90 يوم: <strong>{len(exp_90)}</strong> عقد</div>', unsafe_allow_html=True)
    else:
        st.info("لا توجد بيانات عقود.")

    # ── Collection cards ──
    section_header("💳 حالة التحصيل")
    if not df.empty:
        paid    = len(df[df["payment_display"] == "مسدد"])
        partial = len(df[df["payment_display"] == "جزئي"])
        unpaid  = len(df[df["payment_display"] == "غير مسدد"])
        ratio   = round((paid / total_contracts * 100), 1) if total_contracts else 0
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            metric_card("مسدد",       paid,          "✅", "success")
        with b2:
            metric_card("جزئي",       partial,       "⚡", "warning")
        with b3:
            metric_card("غير مسدد",   unpaid,        "❌", "danger")
        with b4:
            metric_card("نسبة السداد", f"{ratio}%",  "📈", "info")
    else:
        st.info("لا توجد بيانات تحصيل.")

    # ── Charts ──
    section_header("📈 المخططات البيانية")
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("**توزيع العقود حسب حالة السداد**")
        if not df.empty:
            payment_counts = df["payment_display"].value_counts()
            st.bar_chart(payment_counts)
        else:
            st.info("لا توجد بيانات")

    with ch2:
        st.markdown("**توزيع العقود حسب الحي**")
        if not df.empty and "district" in df.columns:
            district_counts = df["district"].fillna("غير محدد").value_counts().head(10)
            st.bar_chart(district_counts)
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
        st.markdown("**البلاغات حسب الأولوية**")
        if fault_reports:
            fr_df = pd.DataFrame(fault_reports)
            priority_map = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
            fr_df["priority_ar"] = fr_df["priority"].map(priority_map).fillna(fr_df["priority"])
            st.bar_chart(fr_df["priority_ar"].value_counts())
        else:
            st.info("لا توجد بلاغات")

    # ── Critical contracts table ──
    section_header("🚨 العقود الحرجة")
    if not df.empty:
        critical = df[
            df["days_remaining"].notna() & (df["days_remaining"] <= 90)
        ].sort_values("days_remaining").head(50)
        if not critical.empty:
            display_cols = ["contract_no", "customer_name", "building_name", "district", "end_date", "days_remaining", "payment_display", "contract_value"]
            existing_cols = [c for c in display_cols if c in critical.columns]
            col_rename = {
                "contract_no": "رقم العقد",
                "customer_name": "اسم العميل",
                "building_name": "اسم المبنى",
                "district": "الحي",
                "end_date": "تاريخ الانتهاء",
                "days_remaining": "الأيام المتبقية",
                "payment_display": "حالة السداد",
                "contract_value": "قيمة العقد",
            }
            st.dataframe(
                critical[existing_cols].rename(columns=col_rename),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("✅ لا توجد عقود حرجة حالياً")
    else:
        st.info("لا توجد عقود.")

    # ── Last 10 contracts ──
    section_header("🆕 آخر 10 عقود مضافة")
    if not df.empty:
        last10 = df.head(10)
        display_cols = ["contract_no", "customer_name", "building_name", "elevator_count", "contract_value", "payment_display", "created_at"]
        existing_cols = [c for c in display_cols if c in last10.columns]
        col_rename = {
            "contract_no": "رقم العقد",
            "customer_name": "اسم العميل",
            "building_name": "اسم المبنى",
            "elevator_count": "عدد المصاعد",
            "contract_value": "قيمة العقد",
            "payment_display": "حالة السداد",
            "created_at": "تاريخ الإضافة",
        }
        st.dataframe(
            last10[existing_cols].rename(columns=col_rename),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("لا توجد عقود.")

# ─────────────────────────────────────────────
# TAB 2: Contracts
# ─────────────────────────────────────────────
def tab_contracts():
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
            elevator_type  = st.selectbox("نوع المصعد", ["ركاب", "شحن", "بانوراما", "خدمة", "سلم كهربائي"])
            elevator_brand = st.text_input("ماركة المصعد")

        col4, col5, col6 = st.columns(3)
        with col4:
            contract_value = st.number_input("قيمة العقد (ر.س)", min_value=0.0, step=100.0)
            start_date     = st.date_input("تاريخ البداية", value=date.today())
        with col5:
            end_date       = st.date_input("تاريخ الانتهاء", value=date.today() + timedelta(days=365))
            payment_status = st.selectbox("حالة السداد", ["unpaid", "partial", "paid"],
                                          format_func=lambda x: {"unpaid": "غير مسدد", "partial": "جزئي", "paid": "مسدد"}[x])
        with col6:
            contract_status = st.selectbox("حالة العقد", ["active", "expired", "cancelled"],
                                           format_func=lambda x: {"active": "نشط", "expired": "منتهي", "cancelled": "ملغي"}[x])
            collector       = st.text_input("المحصل")

        notes   = st.text_area("ملاحظات", height=80)
        submit  = st.form_submit_button("💾 حفظ العقد", use_container_width=True)

    if submit:
        if not contract_no.strip() or not customer_name.strip():
            st.error("❌ رقم العقد واسم العميل مطلوبان")
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                payload = {
                    "contract_no":     contract_no.strip(),
                    "customer_name":   customer_name.strip(),
                    "mobile":          mobile.strip(),
                    "building_name":   building_name.strip(),
                    "district":        district.strip(),
                    "city":            city.strip(),
                    "elevator_count":  int(elevator_count),
                    "elevator_type":   elevator_type,
                    "elevator_brand":  elevator_brand.strip(),
                    "contract_value":  float(contract_value),
                    "start_date":      str(start_date),
                    "end_date":        str(end_date),
                    "payment_status":  payment_status,
                    "contract_status": contract_status,
                    "collector":       collector.strip(),
                    "notes":           notes.strip(),
                }
                supabase.table("contracts").insert(payload).execute()
                st.success("✅ تم حفظ العقد بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الحفظ: {e}")

    # ── View / Search / Edit ──
    section_header("🔍 عرض وبحث العقود")
    contracts = load_contracts()
    df = prepare_contracts_df(contracts)

    if df.empty:
        st.info("لا توجد عقود مسجلة.")
        return

    # Search filters
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        search_name = st.text_input("بحث باسم العميل / رقم العقد", key="search_contract")
    with fcol2:
        filter_payment = st.selectbox("حالة السداد", ["الكل", "مسدد", "جزئي", "غير مسدد"], key="fp_contract")
    with fcol3:
        filter_status = st.selectbox("حالة العقد", ["الكل", "نشط", "ينتهي قريباً", "منتهي"], key="fs_contract")

    filtered = df.copy()
    if search_name.strip():
        mask = (
            filtered["customer_name"].str.contains(search_name.strip(), case=False, na=False) |
            filtered["contract_no"].str.contains(search_name.strip(), case=False, na=False)
        )
        filtered = filtered[mask]
    if filter_payment != "الكل":
        filtered = filtered[filtered["payment_display"] == filter_payment]
    if filter_status != "الكل":
        filtered = filtered[filtered["status_display"] == filter_status]

    st.write(f"عدد النتائج: **{len(filtered)}** عقد")

    # Export
    _cols_drop = [c for c in ["days_remaining","status_display","payment_display","contract_value_num","elevator_count_num","start_date_dt","end_date_dt","days_to_end"] if c in filtered.columns]
    export_df = filtered.drop(columns=_cols_drop)
    csv_bytes = to_csv_bytes(export_df)
    st.download_button("⬇️ تصدير CSV", data=csv_bytes, file_name="contracts.csv", mime="text/csv")

    display_cols = ["contract_no", "customer_name", "mobile", "building_name", "district",
                    "elevator_count", "contract_value", "payment_display", "status_display", "end_date", "days_remaining"]
    existing = [c for c in display_cols if c in filtered.columns]
    col_rename = {
        "contract_no":     "رقم العقد",
        "customer_name":   "اسم العميل",
        "mobile":          "الجوال",
        "building_name":   "اسم المبنى",
        "district":        "الحي",
        "elevator_count":  "عدد المصاعد",
        "contract_value":  "القيمة",
        "payment_display": "السداد",
        "status_display":  "الحالة",
        "end_date":        "نهاية العقد",
        "days_remaining":  "الأيام المتبقية",
    }
    st.dataframe(filtered[existing].rename(columns=col_rename), use_container_width=True, hide_index=True)

    # Edit section
    section_header("✏️ تعديل عقد")
    if not filtered.empty:
        contract_options = {contract_label(row): row["id"] for _, row in filtered.iterrows() if "id" in row}
        selected_label = st.selectbox("اختر العقد للتعديل", list(contract_options.keys()), key="edit_contract_select")
        selected_id = contract_options.get(selected_label)

        if selected_id:
            row_data = filtered[filtered["id"] == selected_id].iloc[0].to_dict()
            with st.form("edit_contract_form"):
                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    e_contract_no    = st.text_input("رقم العقد",  value=safe_text(row_data.get("contract_no")))
                    e_customer_name  = st.text_input("اسم العميل", value=safe_text(row_data.get("customer_name")))
                    e_mobile         = st.text_input("رقم الجوال", value=safe_text(row_data.get("mobile")))
                with ec2:
                    e_building_name  = st.text_input("اسم المبنى", value=safe_text(row_data.get("building_name")))
                    e_district       = st.text_input("الحي",        value=safe_text(row_data.get("district")))
                    e_city           = st.text_input("المدينة",     value=safe_text(row_data.get("city")))
                with ec3:
                    e_elevator_count = st.number_input("عدد المصاعد", min_value=1,
                                                        value=safe_int(row_data.get("elevator_count"), 1))
                    e_elevator_type  = st.text_input("نوع المصعد",  value=safe_text(row_data.get("elevator_type")))
                    e_elevator_brand = st.text_input("ماركة المصعد", value=safe_text(row_data.get("elevator_brand")))

                ec4, ec5, ec6 = st.columns(3)
                with ec4:
                    e_contract_value = st.number_input("قيمة العقد", min_value=0.0, step=100.0,
                                                        value=safe_number(row_data.get("contract_value")))
                    e_start_date_raw = parse_date_safe(row_data.get("start_date")) or date.today()
                    e_start_date     = st.date_input("تاريخ البداية", value=e_start_date_raw)
                with ec5:
                    e_end_date_raw   = parse_date_safe(row_data.get("end_date")) or date.today()
                    e_end_date       = st.date_input("تاريخ الانتهاء", value=e_end_date_raw)
                    pay_options      = ["unpaid", "partial", "paid"]
                    pay_idx          = pay_options.index(row_data.get("payment_status", "unpaid")) if row_data.get("payment_status") in pay_options else 0
                    e_payment_status = st.selectbox("حالة السداد", pay_options,
                                                     format_func=lambda x: {"unpaid": "غير مسدد", "partial": "جزئي", "paid": "مسدد"}[x],
                                                     index=pay_idx)
                with ec6:
                    cs_options  = ["active", "expired", "cancelled"]
                    cs_idx      = cs_options.index(row_data.get("contract_status", "active")) if row_data.get("contract_status") in cs_options else 0
                    e_contract_status = st.selectbox("حالة العقد", cs_options,
                                                      format_func=lambda x: {"active": "نشط", "expired": "منتهي", "cancelled": "ملغي"}[x],
                                                      index=cs_idx)
                    e_collector = st.text_input("المحصل", value=safe_text(row_data.get("collector")))

                e_notes  = st.text_area("ملاحظات", value=safe_text(row_data.get("notes")), height=80)
                save_edit = st.form_submit_button("💾 حفظ التعديلات", use_container_width=True)

            if save_edit:
                if not e_contract_no.strip() or not e_customer_name.strip():
                    st.error("❌ رقم العقد واسم العميل حقول إلزامية")
                elif supabase is None:
                    st.error("❌ لا يوجد اتصال بقاعدة البيانات")
                else:
                    try:
                        payload = {
                            "contract_no":     e_contract_no.strip(),
                            "customer_name":   e_customer_name.strip(),
                            "mobile":          e_mobile.strip(),
                            "building_name":   e_building_name.strip(),
                            "district":        e_district.strip(),
                            "city":            e_city.strip(),
                            "elevator_count":  int(e_elevator_count),
                            "elevator_type":   e_elevator_type.strip(),
                            "elevator_brand":  e_elevator_brand.strip(),
                            "contract_value":  float(e_contract_value),
                            "start_date":      str(e_start_date),
                            "end_date":        str(e_end_date),
                            "payment_status":  e_payment_status,
                            "contract_status": e_contract_status,
                            "collector":       e_collector.strip(),
                            "notes":           e_notes.strip(),
                        }
                        supabase.table("contracts").update(payload).eq("id", selected_id).execute()
                        st.success("✅ تم تحديث العقد بنجاح")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء التحديث: {e}")

# ─────────────────────────────────────────────
# TAB 3: Work Orders
# ─────────────────────────────────────────────
def tab_work_orders():
    contracts = load_contracts()

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
            wo_work_type   = st.selectbox(
                "نوع العمل",
                ["preventive", "corrective", "emergency", "inspection"],
                format_func=lambda x: {"preventive": "وقائي", "corrective": "تصحيحي",
                                        "emergency": "طارئ", "inspection": "فحص"}[x]
            )
        with wc2:
            wo_priority = st.selectbox(
                "الأولوية",
                ["low", "medium", "high", "urgent"],
                format_func=lambda x: {"low": "منخفضة", "medium": "متوسطة",
                                        "high": "عالية", "urgent": "عاجلة"}[x],
                index=1
            )
            wo_technician      = st.selectbox("الفني المسؤول", TECHNICIANS)
            wo_scheduled_date  = st.date_input("التاريخ المجدول", value=date.today())
            wo_status          = st.selectbox(
                "الحالة الابتدائية",
                ["pending", "in_progress"],
                format_func=lambda x: {"pending": "معلق", "in_progress": "جاري"}[x]
            )

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
                contract_id = contract_options.get(selected_contract_label)
                payload = {
                    "contract_id":     contract_id,
                    "title":           wo_title.strip(),
                    "description":     wo_description.strip(),
                    "technician":      wo_technician,
                    "scheduled_date":  str(wo_scheduled_date),
                    "status":          wo_status,
                    "priority":        wo_priority,
                    "work_type":       wo_work_type,
                }
                supabase.table("work_orders").insert(payload).execute()
                st.success("✅ تم حفظ أمر العمل بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الحفظ: {e}")

    # ── View work orders ──
    section_header("📋 عرض أوامر العمل")
    work_orders = load_work_orders()

    if not work_orders:
        st.info("لا توجد أوامر عمل.")
        return

    wo_df = pd.DataFrame(work_orders)

    # Stats row
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        metric_card("معلق",   len(wo_df[wo_df["status"] == "pending"]),     "⏳", "warning")
    with s2:
        metric_card("جاري",   len(wo_df[wo_df["status"] == "in_progress"]), "🔄", "info")
    with s3:
        metric_card("مكتمل",  len(wo_df[wo_df["status"] == "completed"]),   "✅", "success")
    with s4:
        metric_card("ملغي",   len(wo_df[wo_df["status"] == "cancelled"]),   "❌", "danger")

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_wo_status = st.selectbox(
            "فلترة بالحالة",
            ["الكل", "معلق", "جاري", "مكتمل", "ملغي"],
            key="wo_status_filter"
        )
    with fc2:
        tech_list = ["الكل"] + sorted(wo_df["technician"].dropna().unique().tolist())
        filter_wo_tech = st.selectbox("فلترة بالفني", tech_list, key="wo_tech_filter")
    with fc3:
        filter_wo_priority = st.selectbox(
            "فلترة بالأولوية",
            ["الكل", "عاجلة", "عالية", "متوسطة", "منخفضة"],
            key="wo_priority_filter"
        )

    filtered_wo = wo_df.copy()
    status_reverse = {"معلق": "pending", "جاري": "in_progress", "مكتمل": "completed", "ملغي": "cancelled"}
    priority_reverse = {"عاجلة": "urgent", "عالية": "high", "متوسطة": "medium", "منخفضة": "low"}

    if filter_wo_status != "الكل":
        filtered_wo = filtered_wo[filtered_wo["status"] == status_reverse.get(filter_wo_status, "")]
    if filter_wo_tech != "الكل":
        filtered_wo = filtered_wo[filtered_wo["technician"] == filter_wo_tech]
    if filter_wo_priority != "الكل":
        filtered_wo = filtered_wo[filtered_wo["priority"] == priority_reverse.get(filter_wo_priority, "")]

    st.write(f"عدد النتائج: **{len(filtered_wo)}**")

    # Display with Arabic labels
    if not filtered_wo.empty:
        display_wo = filtered_wo.copy()
        status_map   = {"pending": "معلق", "in_progress": "جاري", "completed": "مكتمل", "cancelled": "ملغي"}
        priority_map = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
        work_type_map = {"preventive": "وقائي", "corrective": "تصحيحي", "emergency": "طارئ", "inspection": "فحص"}

        display_wo["الحالة"]      = display_wo["status"].map(status_map).fillna(display_wo["status"])
        display_wo["الأولوية"]    = display_wo["priority"].map(priority_map).fillna(display_wo["priority"])
        display_wo["نوع العمل"]   = display_wo["work_type"].map(work_type_map).fillna(display_wo.get("work_type", ""))

        # بناء قاموس id → contract_no لعرض رقم العقد المقروء
        contracts_raw = load_contracts()
        id_to_contract_no = {str(c.get("id","")): c.get("contract_no","—") for c in contracts_raw}
        display_wo["رقم العقد"] = display_wo["contract_id"].astype(str).map(id_to_contract_no).fillna("—")

        show_cols = ["رقم العقد", "title", "الحالة", "الأولوية", "نوع العمل", "technician", "scheduled_date"]
        existing_show = [c for c in show_cols if c in display_wo.columns]
        col_rename_wo = {
            "title":          "العنوان",
            "technician":     "الفني",
            "scheduled_date": "التاريخ المجدول",
        }
        st.dataframe(
            display_wo[existing_show].rename(columns=col_rename_wo),
            use_container_width=True,
            hide_index=True,
        )

    # Update status
    section_header("🔄 تحديث حالة أمر العمل")
    if not filtered_wo.empty:
        wo_options = {f"{row.get('title','—')} (#{row.get('id','')})": row.get("id") for _, row in filtered_wo.iterrows()}
        selected_wo_label = st.selectbox("اختر أمر العمل", list(wo_options.keys()), key="update_wo_select")
        selected_wo_id = wo_options.get(selected_wo_label)

        if selected_wo_id:
            with st.form("update_wo_form"):
                uc1, uc2 = st.columns(2)
                with uc1:
                    new_status = st.selectbox(
                        "الحالة الجديدة",
                        ["pending", "in_progress", "completed", "cancelled"],
                        format_func=lambda x: {"pending": "معلق", "in_progress": "جاري",
                                                "completed": "مكتمل", "cancelled": "ملغي"}[x]
                    )
                with uc2:
                    completion_notes = st.text_area("ملاحظات الإتمام", height=80)
                update_submit = st.form_submit_button("💾 تحديث", use_container_width=True)

            if update_submit:
                if supabase is None:
                    st.error("❌ لا يوجد اتصال بقاعدة البيانات")
                else:
                    try:
                        supabase.table("work_orders").update({
                            "status": new_status,
                            "completion_notes": completion_notes.strip(),
                        }).eq("id", selected_wo_id).execute()
                        st.success("✅ تم تحديث أمر العمل")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء التحديث: {e}")

# ─────────────────────────────────────────────
# TAB 4: Fault Reports
# ─────────────────────────────────────────────
def tab_fault_reports():
    contracts = load_contracts()

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
            fr_priority = st.selectbox(
                "الأولوية",
                ["low", "medium", "high", "urgent"],
                format_func=lambda x: {"low": "منخفضة", "medium": "متوسطة",
                                        "high": "عالية", "urgent": "عاجلة"}[x],
                index=2
            )
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
                # Auto-fill from contract if selected
                if contract_id:
                    matched = [c for c in contracts if c.get("id") == contract_id]
                    if matched:
                        c = matched[0]
                        if not fr_customer_name.strip():
                            fr_customer_name = safe_text(c.get("customer_name"))
                        if not fr_mobile.strip():
                            fr_mobile = safe_text(c.get("mobile"))
                        if not fr_building_name.strip():
                            fr_building_name = safe_text(c.get("building_name"))

                tech_val = fr_technician if fr_technician != "-- غير مكلف --" else None
                status_val = "assigned" if tech_val else "open"

                payload = {
                    "contract_id":         contract_id,
                    "customer_name":       fr_customer_name.strip(),
                    "mobile":              fr_mobile.strip(),
                    "building_name":       fr_building_name.strip(),
                    "fault_description":   fr_fault_description.strip(),
                    "priority":            fr_priority,
                    "status":              status_val,
                    "assigned_technician": tech_val,
                }
                supabase.table("fault_reports").insert(payload).execute()
                st.success("✅ تم حفظ البلاغ بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الحفظ: {e}")

    # ── View fault reports ──
    section_header("📋 عرض البلاغات")
    fault_reports = load_fault_reports()

    if not fault_reports:
        st.info("لا توجد بلاغات.")
        return

    fr_df = pd.DataFrame(fault_reports)

    # Stats
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        metric_card("مفتوح",  len(fr_df[fr_df["status"] == "open"]),        "🔴", "danger")
    with s2:
        metric_card("مكلف",   len(fr_df[fr_df["status"] == "assigned"]),     "🟡", "warning")
    with s3:
        metric_card("جاري",   len(fr_df[fr_df["status"] == "in_progress"]),  "🔵", "info")
    with s4:
        metric_card("محلول",  len(fr_df[fr_df["status"] == "resolved"]),     "🟢", "success")

    # Filters
    ff1, ff2 = st.columns(2)
    with ff1:
        filter_fr_status = st.selectbox(
            "فلترة بالحالة",
            ["الكل", "مفتوح", "مكلف", "جاري", "محلول", "مغلق"],
            key="fr_status_filter"
        )
    with ff2:
        filter_fr_priority = st.selectbox(
            "فلترة بالأولوية",
            ["الكل", "عاجلة", "عالية", "متوسطة", "منخفضة"],
            key="fr_priority_filter"
        )

    fr_filtered = fr_df.copy()
    fr_status_reverse   = {"مفتوح": "open", "مكلف": "assigned", "جاري": "in_progress", "محلول": "resolved", "مغلق": "closed"}
    fr_priority_reverse = {"عاجلة": "urgent", "عالية": "high", "متوسطة": "medium", "منخفضة": "low"}

    if filter_fr_status != "الكل":
        fr_filtered = fr_filtered[fr_filtered["status"] == fr_status_reverse.get(filter_fr_status, "")]
    if filter_fr_priority != "الكل":
        fr_filtered = fr_filtered[fr_filtered["priority"] == fr_priority_reverse.get(filter_fr_priority, "")]

    st.write(f"عدد النتائج: **{len(fr_filtered)}**")

    if not fr_filtered.empty:
        display_fr = fr_filtered.copy()
        fr_status_map   = {"open": "مفتوح", "assigned": "مكلف", "in_progress": "جاري",
                            "resolved": "محلول", "closed": "مغلق"}
        fr_priority_map = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
        display_fr["الحالة"]   = display_fr["status"].map(fr_status_map).fillna(display_fr["status"])
        display_fr["الأولوية"] = display_fr["priority"].map(fr_priority_map).fillna(display_fr["priority"])

        show_cols = ["customer_name", "building_name", "fault_description", "الأولوية",
                     "الحالة", "assigned_technician", "created_at"]
        existing_show = [c for c in show_cols if c in display_fr.columns]
        col_rename_fr = {
            "customer_name":      "اسم العميل",
            "building_name":      "اسم المبنى",
            "fault_description":  "وصف العطل",
            "assigned_technician": "الفني المكلف",
            "created_at":         "تاريخ البلاغ",
        }
        st.dataframe(
            display_fr[existing_show].rename(columns=col_rename_fr),
            use_container_width=True,
            hide_index=True,
        )

    # Update fault report status
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
                    new_fr_status = st.selectbox(
                        "الحالة الجديدة",
                        ["open", "assigned", "in_progress", "resolved", "closed"],
                        format_func=lambda x: {
                            "open": "مفتوح", "assigned": "مكلف",
                            "in_progress": "جاري", "resolved": "محلول", "closed": "مغلق"
                        }[x]
                    )
                    new_fr_tech = st.text_input("الفني المكلف")
                with uc2:
                    resolution_notes = st.text_area("ملاحظات الحل", height=80)

                fr_update_submit = st.form_submit_button("💾 تحديث البلاغ", use_container_width=True)

            if fr_update_submit:
                if supabase is None:
                    st.error("❌ لا يوجد اتصال بقاعدة البيانات")
                else:
                    try:
                        update_payload = {
                            "status":           new_fr_status,
                            "resolution_notes": resolution_notes.strip(),
                        }
                        if new_fr_tech.strip():
                            update_payload["assigned_technician"] = new_fr_tech.strip()
                        if new_fr_status in ("resolved", "closed"):
                            update_payload["resolved_at"] = datetime.now().isoformat()
                        supabase.table("fault_reports").update(update_payload).eq("id", selected_fr_id).execute()
                        st.success("✅ تم تحديث البلاغ")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء التحديث: {e}")

# ─────────────────────────────────────────────
# TAB 5: Maintenance Logs
# ─────────────────────────────────────────────
def tab_maintenance_logs():
    contracts = load_contracts()

    section_header("➕ إضافة سجل زيارة صيانة")

    contract_options = {"-- اختر العقد --": None}
    for c in contracts:
        contract_options[contract_label(c)] = c.get("id")

    with st.form("new_maintenance_log_form", clear_on_submit=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            selected_contract_label = st.selectbox("العقد المرتبط *", list(contract_options.keys()))
            ml_elevator_no   = st.text_input("رقم المصعد في المبنى")
            ml_visit_date    = st.date_input("تاريخ الزيارة", value=date.today())
            ml_technician    = st.selectbox("الفني", TECHNICIANS)
            ml_condition     = st.selectbox(
                "حالة المصعد",
                ["good", "fair", "poor"],
                format_func=lambda x: {"good": "جيد", "fair": "متوسط", "poor": "سيء"}[x]
            )
        with mc2:
            ml_work_done     = st.text_area("الأعمال المنجزة *", height=100)
            ml_parts         = st.text_area("قطع الغيار المستبدلة", height=80)
            ml_next_visit    = st.date_input("تاريخ الزيارة القادمة",
                                              value=date.today() + timedelta(days=90))
            ml_notes         = st.text_area("ملاحظات", height=60)

        ml_submit = st.form_submit_button("💾 حفظ سجل الصيانة", use_container_width=True)

    if ml_submit:
        if not ml_work_done.strip():
            st.error("❌ الأعمال المنجزة مطلوبة")
        elif supabase is None:
            st.error("❌ لا يوجد اتصال بقاعدة البيانات")
        else:
            try:
                contract_id = contract_options.get(selected_contract_label)
                payload = {
                    "contract_id":     contract_id,
                    "elevator_no":     ml_elevator_no.strip(),
                    "visit_date":      str(ml_visit_date),
                    "technician":      ml_technician,
                    "work_done":       ml_work_done.strip(),
                    "parts_replaced":  ml_parts.strip(),
                    "next_visit_date": str(ml_next_visit),
                    "condition":       ml_condition,
                    "notes":           ml_notes.strip(),
                }
                supabase.table("maintenance_logs").insert(payload).execute()
                st.success("✅ تم حفظ سجل الصيانة بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الحفظ: {e}")

    # ── View maintenance logs ──
    section_header("📋 عرض سجل الصيانة")
    maintenance_logs = load_maintenance_logs()

    if not maintenance_logs:
        st.info("لا توجد سجلات صيانة.")
        return

    ml_df = pd.DataFrame(maintenance_logs)

    # Filters
    mf1, mf2, mf3 = st.columns(3)
    with mf1:
        tech_list_ml = ["الكل"] + sorted(ml_df["technician"].dropna().unique().tolist())
        filter_ml_tech = st.selectbox("فلترة بالفني", tech_list_ml, key="ml_tech_filter")
    with mf2:
        filter_ml_condition = st.selectbox(
            "فلترة بحالة المصعد",
            ["الكل", "جيد", "متوسط", "سيء"],
            key="ml_condition_filter"
        )
    with mf3:
        search_ml_contract = st.text_input("بحث برقم العقد", key="ml_contract_search")

    filtered_ml = ml_df.copy()
    condition_reverse = {"جيد": "good", "متوسط": "fair", "سيء": "poor"}
    if filter_ml_tech != "الكل":
        filtered_ml = filtered_ml[filtered_ml["technician"] == filter_ml_tech]
    if filter_ml_condition != "الكل":
        filtered_ml = filtered_ml[filtered_ml["condition"] == condition_reverse.get(filter_ml_condition, "")]
    if search_ml_contract.strip():
        # بناء قاموس id → contract_no للبحث بالرقم المقروء
        _contracts_raw = load_contracts()
        _id_to_cno = {str(c.get("id","")): str(c.get("contract_no","")) for c in _contracts_raw}
        filtered_ml["_contract_no_lookup"] = filtered_ml["contract_id"].astype(str).map(_id_to_cno).fillna("")
        filtered_ml = filtered_ml[
            filtered_ml["_contract_no_lookup"].str.contains(search_ml_contract.strip(), case=False, na=False) |
            filtered_ml["contract_id"].astype(str).str.contains(search_ml_contract.strip(), case=False, na=False)
        ]

    st.write(f"عدد السجلات: **{len(filtered_ml)}**")

    if not filtered_ml.empty:
        display_ml = filtered_ml.copy()
        cond_map = {"good": "جيد", "fair": "متوسط", "poor": "سيء"}
        display_ml["حالة المصعد"] = display_ml["condition"].map(cond_map).fillna(display_ml["condition"])

        # إضافة رقم العقد المقروء
        _contracts_raw2 = load_contracts()
        _id_to_cno2 = {str(c.get("id","")): c.get("contract_no","—") for c in _contracts_raw2}
        display_ml["رقم العقد"] = display_ml["contract_id"].astype(str).map(_id_to_cno2).fillna("—")

        show_cols = ["رقم العقد", "elevator_no", "visit_date", "technician", "work_done",
                     "parts_replaced", "حالة المصعد", "next_visit_date"]
        existing_show = [c for c in show_cols if c in display_ml.columns]
        col_rename_ml = {
            "contract_id":   "رقم العقد",
            "elevator_no":   "رقم المصعد",
            "visit_date":    "تاريخ الزيارة",
            "technician":    "الفني",
            "work_done":     "الأعمال المنجزة",
            "parts_replaced": "قطع الغيار",
            "next_visit_date": "الزيارة القادمة",
        }
        st.dataframe(
            display_ml[existing_show].rename(columns=col_rename_ml),
            use_container_width=True,
            hide_index=True,
        )

        # Detail expanders
        section_header("🔍 تفاصيل الزيارات")
        for idx, row in filtered_ml.head(20).iterrows():
            visit_date_str = safe_text(row.get("visit_date"), "—")
            tech_str       = safe_text(row.get("technician"), "—")
            cond_str       = cond_map.get(safe_text(row.get("condition")), "—")
            with st.expander(f"زيارة {visit_date_str} – فني: {tech_str} – الحالة: {cond_str}"):
                d1, d2 = st.columns(2)
                with d1:
                    st.write(f"**رقم المصعد:** {safe_text(row.get('elevator_no'), '—')}")
                    st.write(f"**الأعمال المنجزة:** {safe_text(row.get('work_done'), '—')}")
                    st.write(f"**قطع الغيار المستبدلة:** {safe_text(row.get('parts_replaced'), '—')}")
                with d2:
                    st.write(f"**الزيارة القادمة:** {safe_text(row.get('next_visit_date'), '—')}")
                    st.write(f"**ملاحظات:** {safe_text(row.get('notes'), '—')}")

# ─────────────────────────────────────────────
# TAB 6: Technicians & Scheduling
# ─────────────────────────────────────────────
def tab_technicians():
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    contracts     = load_contracts()

    technicians = ["طه", "أحمد"]

    section_header("👷 إحصائيات الفنيين")

    wo_df = pd.DataFrame(work_orders) if work_orders else pd.DataFrame(columns=["technician", "status", "scheduled_date"])
    fr_df = pd.DataFrame(fault_reports) if fault_reports else pd.DataFrame(columns=["assigned_technician", "status"])

    today      = date.today()
    month_start = today.replace(day=1)

    tech_cols = st.columns(len(technicians))
    for idx, tech in enumerate(technicians):
        with tech_cols[idx]:
            # Work orders stats
            tech_wo = wo_df[wo_df["technician"] == tech] if not wo_df.empty else pd.DataFrame()
            pending_count = len(tech_wo[tech_wo["status"] == "pending"]) if not tech_wo.empty else 0

            # Completed this month
            completed_this_month = 0
            if not tech_wo.empty and "scheduled_date" in tech_wo.columns:
                tech_wo_copy = tech_wo.copy()
                tech_wo_copy["sched_date_parsed"] = pd.to_datetime(tech_wo_copy["scheduled_date"], errors="coerce").dt.date
                completed_this_month = len(
                    tech_wo_copy[
                        (tech_wo_copy["status"] == "completed") &
                        (tech_wo_copy["sched_date_parsed"] >= month_start)
                    ]
                )

            # Fault reports assigned
            tech_fr = fr_df[fr_df["assigned_technician"] == tech] if not fr_df.empty else pd.DataFrame()
            assigned_faults = len(tech_fr[tech_fr["status"].isin(["assigned", "in_progress"])]) if not tech_fr.empty else 0

            st.markdown(f"""
            <div class="tech-card">
              <h3>👷 {tech}</h3>
              <div class="tech-stat"><span>أوامر العمل المعلقة</span><span>{pending_count}</span></div>
              <div class="tech-stat"><span>مكتملة هذا الشهر</span><span>{completed_this_month}</span></div>
              <div class="tech-stat"><span>بلاغات مكلف بها</span><span>{assigned_faults}</span></div>
            </div>
            """, unsafe_allow_html=True)

    # ── Next week schedule ──
    section_header("📅 جدول مهام الأسبوع القادم")
    next_week_start = today + timedelta(days=1)
    next_week_end   = today + timedelta(days=7)

    if not wo_df.empty and "scheduled_date" in wo_df.columns:
        wo_schedule = wo_df.copy()
        wo_schedule["sched_parsed"] = pd.to_datetime(wo_schedule["scheduled_date"], errors="coerce").dt.date
        week_orders = wo_schedule[
            (wo_schedule["sched_parsed"] >= next_week_start) &
            (wo_schedule["sched_parsed"] <= next_week_end)
        ].sort_values(["sched_parsed", "technician"])

        if not week_orders.empty:
            status_map   = {"pending": "معلق", "in_progress": "جاري", "completed": "مكتمل", "cancelled": "ملغي"}
            priority_map = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
            work_type_map = {"preventive": "وقائي", "corrective": "تصحيحي", "emergency": "طارئ", "inspection": "فحص"}

            week_orders["الحالة"]    = week_orders["status"].map(status_map).fillna(week_orders["status"])
            week_orders["الأولوية"] = week_orders["priority"].map(priority_map).fillna(week_orders["priority"])
            week_orders["نوع العمل"] = week_orders["work_type"].map(work_type_map).fillna(week_orders.get("work_type", ""))

            show_week = ["scheduled_date", "technician", "title", "الأولوية", "الحالة", "نوع العمل"]
            existing_week = [c for c in show_week if c in week_orders.columns]
            col_rename_week = {
                "scheduled_date": "التاريخ",
                "technician":     "الفني",
                "title":          "العنوان",
            }
            st.dataframe(
                week_orders[existing_week].rename(columns=col_rename_week),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("لا توجد مهام مجدولة للأسبوع القادم.")
    else:
        st.info("لا توجد أوامر عمل.")

    # ── Quick add task ──
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
            qt_priority = st.selectbox(
                "الأولوية",
                ["low", "medium", "high", "urgent"],
                format_func=lambda x: {"low": "منخفضة", "medium": "متوسطة",
                                        "high": "عالية", "urgent": "عاجلة"}[x],
                index=1,
                key="qt_priority"
            )
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
                contract_id = contract_options.get(qt_contract)
                payload = {
                    "contract_id":    contract_id,
                    "title":          qt_description.strip()[:100],
                    "description":    qt_description.strip(),
                    "technician":     qt_tech,
                    "scheduled_date": str(qt_date),
                    "status":         "pending",
                    "priority":       qt_priority,
                    "work_type":      "preventive",
                }
                supabase.table("work_orders").insert(payload).execute()
                st.success("✅ تمت إضافة المهمة بنجاح")
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ أثناء الإضافة: {e}")

# ─────────────────────────────────────────────
# Main app
# ─────────────────────────────────────────────
def main():
    if not check_login():
        return

    # App header
    st.markdown(f"""
    <div class="app-header">
      <div>
        <h1>🛗 LiftTech V4.0</h1>
        <p>نظام إدارة شركة صيانة المصاعد – مرحباً {st.session_state.username}</p>
      </div>
      <div style="text-align:left; opacity:0.7; font-size:0.85rem;">
        {datetime.now().strftime("%Y-%m-%d %H:%M")}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Logout button
    col_spacer, col_logout = st.columns([10, 1])
    with col_logout:
        if st.button("خروج", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username  = ""
            st.rerun()

    # Tabs
    tabs = st.tabs([
        "📊 لوحة التحكم",
        "📋 العقود",
        "🔧 أوامر العمل",
        "🚨 بلاغات الأعطال",
        "📝 سجل الصيانة",
        "👷 الفنيون والجدولة",
    ])

    with tabs[0]:
        tab_dashboard()
    with tabs[1]:
        tab_contracts()
    with tabs[2]:
        tab_work_orders()
    with tabs[3]:
        tab_fault_reports()
    with tabs[4]:
        tab_maintenance_logs()
    with tabs[5]:
        tab_technicians()

if __name__ == "__main__":
    main()

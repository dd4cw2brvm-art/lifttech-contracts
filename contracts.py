import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date, datetime
from io import BytesIO

# =========================================================
# LIFTTECH CONTRACTS SYSTEM - V3.0
# نظام إدارة عقود صيانة لفتك - V3.0
# =========================================================

st.set_page_config(
    page_title="LiftTech | نظام عقود الصيانة",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS - Enhanced UI V3.0
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}

/* ===== Global Background ===== */
.stApp {
    background: #f1f5f9;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1.5rem;
    max-width: 1300px;
}

/* ===== Hide Streamlit Branding ===== */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* ===== Login Page ===== */
.login-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
}

.login-card {
    background: white;
    border-radius: 24px;
    padding: 48px 40px;
    box-shadow: 0 20px 60px rgba(15,23,42,0.12);
    width: 100%;
    max-width: 420px;
    text-align: center;
}

.login-logo {
    font-size: 52px;
    margin-bottom: 8px;
}

.login-brand {
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
    letter-spacing: 2px;
    margin-bottom: 4px;
}

.login-tagline {
    font-size: 14px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid #f1f5f9;
}

/* ===== Main Header ===== */
.lift-header {
    padding: 20px 28px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #7f1d1d 100%);
    color: white;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 8px 32px rgba(15,23,42,0.2);
}

.lift-header-text h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 900;
    letter-spacing: 0.5px;
}

.lift-header-text p {
    margin: 4px 0 0 0;
    color: #94a3b8;
    font-size: 12px;
}

.lift-header-badge {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 8px 16px;
    text-align: center;
}

.lift-header-badge span {
    display: block;
    font-size: 11px;
    color: #94a3b8;
}

.lift-header-badge strong {
    font-size: 18px;
    font-weight: 800;
    color: white;
}

/* ===== Metric Cards ===== */
.metric-card {
    padding: 20px 16px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 16px rgba(15,23,42,0.06);
    text-align: center;
    min-height: 110px;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 18px 18px 0 0;
}

.metric-card-danger::before { background: linear-gradient(90deg, #ef4444, #f97316); }
.metric-card-success::before { background: linear-gradient(90deg, #22c55e, #10b981); }
.metric-card-warning::before { background: linear-gradient(90deg, #f59e0b, #eab308); }
.metric-card-purple::before { background: linear-gradient(90deg, #8b5cf6, #6366f1); }
.metric-card-blue::before { background: linear-gradient(90deg, #3b82f6, #0ea5e9); }

.metric-icon {
    font-size: 22px;
    margin-bottom: 6px;
}

.metric-title {
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.metric-value {
    color: #0f172a;
    font-size: 26px;
    font-weight: 900;
    margin-top: 6px;
    line-height: 1;
}

/* ===== Section Headers ===== */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 12px 0;
}

.section-header-line {
    flex: 1;
    height: 1px;
    background: #e2e8f0;
}

.section-header-text {
    color: #0f172a;
    font-size: 16px;
    font-weight: 800;
    white-space: nowrap;
    padding: 0 8px;
}

/* ===== Alert Cards ===== */
.alert-card {
    padding: 16px;
    border-radius: 16px;
    font-weight: 700;
    text-align: center;
    font-size: 14px;
}

.alert-red {
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border: 1px solid #fca5a5;
    color: #991b1b;
}

.alert-orange {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border: 1px solid #fdba74;
    color: #9a3412;
}

.alert-yellow {
    background: linear-gradient(135deg, #fefce8, #fef9c3);
    border: 1px solid #fde047;
    color: #713f12;
}

.alert-green {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #86efac;
    color: #14532d;
}

.alert-number {
    font-size: 32px;
    font-weight: 900;
    display: block;
    margin-top: 4px;
}

.alert-label {
    font-size: 12px;
    opacity: 0.85;
}

/* ===== Tabs ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: white;
    padding: 6px;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(15,23,42,0.06);
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 700;
    font-size: 14px;
    color: #64748b;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0f172a, #1e3a5f) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(15,23,42,0.25);
}

/* ===== Dataframe ===== */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(15,23,42,0.06);
}

/* ===== Buttons ===== */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Cairo', sans-serif !important;
    transition: all 0.2s !important;
    border: none !important;
    padding: 10px 20px !important;
}

.stButton > button[kind="primary"],
.stButton > button:not([kind]) {
    background: linear-gradient(135deg, #0f172a, #1e3a5f) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(15,23,42,0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(15,23,42,0.35) !important;
}

/* ===== Inputs ===== */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}

/* ===== Form Sections ===== */
.form-section {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
}

.form-section-title {
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f1f5f9;
}

/* ===== Download Button ===== */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Cairo', sans-serif !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(5,150,105,0.3) !important;
}

/* ===== Sidebar ===== */
.css-1d391kg, [data-testid="stSidebar"] {
    background: white;
    border-left: 1px solid #e2e8f0;
}

/* ===== Success / Error Messages ===== */
.stSuccess, .stError, .stInfo {
    border-radius: 12px !important;
    font-family: 'Cairo', sans-serif !important;
}

/* ===== Divider ===== */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 16px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# Supabase Connection
# =========================================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================================================
# Helper Functions
# =========================================================
def safe_text(value):
    if value is None or pd.isna(value):
        return ""
    return str(value)


def safe_number(value, default=0.0):
    try:
        if value is None or pd.isna(value):
            return default
        value = str(value).replace(",", "").replace("ريال", "").strip()
        return float(value)
    except Exception:
        return default


def safe_int(value, default=1):
    try:
        if value is None or pd.isna(value):
            return default
        return int(float(value))
    except Exception:
        return default


def parse_date_safe(value):
    try:
        if value is None or pd.isna(value) or str(value).strip() == "":
            return date.today()
        parsed = pd.to_datetime(value, errors="coerce")
        if pd.isna(parsed):
            return date.today()
        return parsed.date()
    except Exception:
        return date.today()


def load_contracts():
    response = supabase.table("contracts").select("*").order("id", desc=True).execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()


def prepare_contracts_df(df):
    if df.empty:
        return df

    df = df.copy()

    required_cols = [
        "id", "created_at", "contract_no", "customer_name", "mobile",
        "building_name", "district", "city", "elevator_count",
        "elevator_type", "elevator_brand", "contract_value",
        "start_date", "end_date", "payment_status", "contract_status",
        "collector", "notes"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    df["contract_value_num"] = pd.to_numeric(
        df["contract_value"].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    ).fillna(0)

    df["elevator_count_num"] = pd.to_numeric(
        df["elevator_count"], errors="coerce"
    ).fillna(0)

    df["start_date_dt"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date_dt"] = pd.to_datetime(df["end_date"], errors="coerce")

    today_ts = pd.Timestamp(date.today())
    df["days_to_end"] = (df["end_date_dt"] - today_ts).dt.days

    df["renewal_status"] = "غير محدد"
    df.loc[df["days_to_end"].notna() & (df["days_to_end"] < 0), "renewal_status"] = "منتهي"
    df.loc[df["days_to_end"].between(0, 30, inclusive="both"), "renewal_status"] = "ينتهي خلال 30 يوم"
    df.loc[df["days_to_end"].between(31, 60, inclusive="both"), "renewal_status"] = "ينتهي خلال 60 يوم"
    df.loc[df["days_to_end"].between(61, 90, inclusive="both"), "renewal_status"] = "ينتهي خلال 90 يوم"
    df.loc[df["days_to_end"] > 90, "renewal_status"] = "ساري"

    return df


def to_csv_bytes(df):
    export_df = df.copy()
    internal_cols = ["contract_value_num", "elevator_count_num", "start_date_dt", "end_date_dt", "days_to_end"]
    for col in internal_cols:
        if col in export_df.columns:
            export_df = export_df.drop(columns=[col])
    return export_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def metric_card(title, value, icon="", variant=""):
    variant_class = f"metric-card-{variant}" if variant else ""
    st.markdown(
        f"""
        <div class="metric-card {variant_class}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(text):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-header-text">{text}</div>
            <div class="section-header-line"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Login Page
# =========================================================
def login():
    left, center, right = st.columns([1.4, 1, 1.4])
    with center:
        st.markdown('<div style="height: 6vh"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom: 8px;">
            <div style="font-size: 52px;">🛗</div>
            <div style="font-size: 38px; font-weight: 900; color: #0f172a; letter-spacing: 2px;">LIFT TECH</div>
            <div style="font-size: 14px; color: #64748b; font-weight: 600; margin-bottom: 28px;">مركز إدارة وتشغيل المصاعد</div>
            <div style="width: 40px; height: 3px; background: linear-gradient(90deg,#3b82f6,#6366f1); border-radius: 2px; margin: 0 auto 28px;"></div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("اسم المستخدم", key="login_username", placeholder="أدخل اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password", key="login_password", placeholder="أدخل كلمة المرور")

        st.markdown('<div style="height: 8px"></div>', unsafe_allow_html=True)

        if st.button("دخول النظام 🔐", use_container_width=True, key="login_btn"):
            users = st.secrets["users"]
            if username in users and password == users[username]:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("⚠️ بيانات الدخول غير صحيحة")

        st.markdown("""
        <div style="text-align:center; margin-top: 20px; color: #94a3b8; font-size: 12px;">
            النظام مخصص للاستخدام الداخلي فقط
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# Authentication
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 16px; background: #f8fafc; border-radius: 14px; border: 1px solid #e2e8f0; margin-bottom: 12px;">
        <div style="font-size: 12px; color: #64748b; font-weight: 600;">المستخدم الحالي</div>
        <div style="font-size: 18px; font-weight: 800; color: #0f172a; margin-top: 4px;">👤 {st.session_state['username']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("تسجيل خروج 🚪", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 11px; color: #94a3b8; text-align: center;">
        LiftTech V3.0<br>نظام إدارة العقود
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# Main Header
# =========================================================
today_str = datetime.now().strftime('%Y/%m/%d')
time_str = datetime.now().strftime('%H:%M')

st.markdown(
    f"""
    <div class="lift-header">
        <div class="lift-header-text">
            <h1>🛗 نظام إدارة عقود صيانة لفتك</h1>
            <p>LiftTech Maintenance Command Center &nbsp;|&nbsp; V3.0</p>
        </div>
        <div class="lift-header-badge">
            <span>آخر تحديث</span>
            <strong>{today_str}</strong>
            <span>{time_str}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["📊  لوحة التحكم", "➕  إضافة عقد", "🔍  عرض وتعديل العقود"])


# =========================================================
# Dashboard Tab
# =========================================================
with tab1:
    df = prepare_contracts_df(load_contracts())

    if df.empty:
        st.info("لا توجد عقود حتى الآن")
    else:
        total_contracts = len(df)
        total_value = df["contract_value_num"].sum()
        active_count = len(df[df["contract_status"] == "نشط"])
        expired_count = len(df[df["renewal_status"] == "منتهي"])
        unpaid_count = len(df[df["payment_status"] == "غير مسدد"])
        partial_paid_count = len(df[df["payment_status"] == "مسدد جزئياً"])
        paid_count = len(df[df["payment_status"] == "مسدد"])
        elevator_total = int(df["elevator_count_num"].sum())
        avg_contract_value = total_value / total_contracts if total_contracts else 0

        # ── KPI Cards ──
        section_header("المؤشرات الرئيسية")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            metric_card("إجمالي العقود", f"{total_contracts:,}", "📋", "blue")
        with c2:
            metric_card("إجمالي القيمة (ر.س)", f"{total_value:,.0f}", "💰", "purple")
        with c3:
            metric_card("العقود النشطة", f"{active_count:,}", "✅", "success")
        with c4:
            metric_card("غير المسددة", f"{unpaid_count:,}", "⚠️", "danger")
        with c5:
            metric_card("عدد المصاعد", f"{elevator_total:,}", "🛗", "blue")

        # ── Renewal Alerts ──
        section_header("تنبيهات التجديد")
        end_30 = len(df[df["renewal_status"] == "ينتهي خلال 30 يوم"])
        end_60 = len(df[df["renewal_status"] == "ينتهي خلال 60 يوم"])
        end_90 = len(df[df["renewal_status"] == "ينتهي خلال 90 يوم"])
        active_safe = len(df[df["renewal_status"] == "ساري"])

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f"""
            <div class="alert-card alert-red">
                <div class="alert-label">🔴 منتهي بالفعل</div>
                <span class="alert-number">{expired_count}</span>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class="alert-card alert-orange">
                <div class="alert-label">🟠 ينتهي خلال 30 يوم</div>
                <span class="alert-number">{end_30}</span>
            </div>""", unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class="alert-card alert-yellow">
                <div class="alert-label">🟡 ينتهي خلال 60 يوم</div>
                <span class="alert-number">{end_60}</span>
            </div>""", unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div class="alert-card alert-green">
                <div class="alert-label">🟢 ساري وآمن</div>
                <span class="alert-number">{active_safe}</span>
            </div>""", unsafe_allow_html=True)

        # ── Payment Collection ──
        section_header("حالة التحصيل")
        collection_rate = (paid_count / total_contracts * 100) if total_contracts else 0

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            metric_card("مسدد بالكامل", f"{paid_count:,}", "✅", "success")
        with p2:
            metric_card("مسدد جزئياً", f"{partial_paid_count:,}", "🔶", "warning")
        with p3:
            metric_card("غير مسدد", f"{unpaid_count:,}", "❌", "danger")
        with p4:
            metric_card("نسبة السداد", f"{collection_rate:.1f}%", "📈", "purple")

        # ── Operational Insights ──
        section_header("مؤشرات تشغيلية")
        top_district = df["district"].value_counts().idxmax() if "district" in df.columns and not df["district"].dropna().empty else "-"
        top_brand = df["elevator_brand"].value_counts().idxmax() if "elevator_brand" in df.columns and not df["elevator_brand"].dropna().empty else "-"
        top_customer_row = df.sort_values("contract_value_num", ascending=False).head(1)
        top_customer = safe_text(top_customer_row["customer_name"].iloc[0]) if not top_customer_row.empty else "-"

        o1, o2, o3, o4 = st.columns(4)
        with o1:
            metric_card("أكثر حي", top_district, "📍", "blue")
        with o2:
            metric_card("أكثر ماركة", top_brand, "🏷️", "purple")
        with o3:
            metric_card("أكبر عميل", top_customer, "🏆", "warning")
        with o4:
            metric_card("متوسط قيمة العقد", f"{avg_contract_value:,.0f}", "📊", "blue")

        # ── Critical Contracts ──
        section_header("⚠️ العقود الحرجة")
        critical_df = df[
            (df["renewal_status"].isin(["منتهي", "ينتهي خلال 30 يوم", "ينتهي خلال 60 يوم", "ينتهي خلال 90 يوم"]))
            | (df["payment_status"].isin(["غير مسدد", "مسدد جزئياً"]))
        ].copy()

        display_cols = [
            "contract_no", "customer_name", "mobile", "district", "city",
            "contract_value", "end_date", "payment_status", "contract_status",
            "renewal_status", "collector"
        ]

        st.dataframe(
            critical_df[[c for c in display_cols if c in critical_df.columns]].head(50),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 تصدير العقود الحرجة CSV",
            data=to_csv_bytes(critical_df),
            file_name=f"LIFTTECH_CRITICAL_{date.today()}.csv",
            mime="text/csv"
        )

        # ── Recent Contracts ──
        section_header("🕐 آخر 10 عقود مضافة")
        st.dataframe(
            df[[c for c in display_cols if c in df.columns]].head(10),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# Add Contract Tab
# =========================================================
with tab2:
    st.markdown('<div style="height: 4px"></div>', unsafe_allow_html=True)

    # Section: Customer
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-section-title">👤 بيانات العميل والموقع</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        contract_no = st.text_input("رقم العقد *", key="add_contract_no", placeholder="مثال: LT-2025-001")
    with a2:
        customer_name = st.text_input("اسم العميل *", key="add_customer_name", placeholder="الاسم الكامل")
    with a3:
        mobile = st.text_input("رقم الجوال *", key="add_mobile", placeholder="05XXXXXXXX")

    a4, a5, a6 = st.columns(3)
    with a4:
        building_name = st.text_input("اسم المبنى / الموقع", key="add_building_name", placeholder="اسم البرج أو المجمع")
    with a5:
        district = st.text_input("الحي", key="add_district", placeholder="الحي")
    with a6:
        city = st.text_input("المدينة", value="الرياض", key="add_city")

    st.markdown('</div>', unsafe_allow_html=True)

    # Section: Elevator Details
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-section-title">🛗 تفاصيل المصعد</div>', unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        elevator_count = st.number_input("عدد المصاعد", min_value=1, step=1, key="add_elevator_count")
    with b2:
        elevator_type = st.selectbox("نوع المصعد", ["ركاب", "خدمة", "بانوراما", "بضائع", "أخرى"], key="add_elevator_type")
    with b3:
        elevator_brand = st.text_input("ماركة المصعد", key="add_elevator_brand", placeholder="مثال: OTIS, Kone...")

    st.markdown('</div>', unsafe_allow_html=True)

    # Section: Contract Financials
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-section-title">📋 بيانات العقد المالية</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        contract_value = st.number_input("قيمة العقد (ر.س)", min_value=0.0, step=100.0, key="add_contract_value")
    with c2:
        start_date = st.date_input("تاريخ بداية العقد", key="add_start_date")
    with c3:
        end_date = st.date_input("تاريخ نهاية العقد", key="add_end_date")

    d1, d2, d3 = st.columns(3)
    with d1:
        payment_status = st.selectbox("حالة السداد", ["مسدد", "مسدد جزئياً", "غير مسدد"], key="add_payment_status")
    with d2:
        contract_status = st.selectbox("حالة العقد", ["نشط", "قريب الانتهاء", "منتهي", "موقوف"], key="add_contract_status")
    with d3:
        collector = st.selectbox("مسؤول التحصيل", ["طه", "أحمد", "آخر"], key="add_collector")

    notes = st.text_area("ملاحظات إضافية", key="add_notes", placeholder="أي ملاحظات خاصة بالعقد...")
    st.markdown('</div>', unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("💾 حفظ العقد", key="save_contract", use_container_width=True):
            if not contract_no.strip() or not customer_name.strip() or not mobile.strip():
                st.error("⚠️ رقم العقد، اسم العميل، ورقم الجوال حقول إلزامية.")
            else:
                data = {
                    "contract_no": contract_no.strip(),
                    "customer_name": customer_name.strip(),
                    "mobile": mobile.strip(),
                    "building_name": building_name.strip(),
                    "district": district.strip(),
                    "city": city.strip(),
                    "elevator_count": str(elevator_count),
                    "elevator_type": elevator_type,
                    "elevator_brand": elevator_brand.strip(),
                    "contract_value": str(contract_value),
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "payment_status": payment_status,
                    "contract_status": contract_status,
                    "collector": collector,
                    "notes": notes.strip(),
                }
                supabase.table("contracts").insert(data).execute()
                st.success("✅ تم حفظ العقد في قاعدة البيانات بنجاح!")
                st.rerun()


# =========================================================
# View / Edit Tab
# =========================================================
with tab3:
    df = prepare_contracts_df(load_contracts())

    if df.empty:
        st.info("لا توجد عقود مسجلة")
    else:
        # ── Search ──
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">🔍 البحث والتصفية</div>', unsafe_allow_html=True)

        search_query = st.text_input(
            "بحث موحد",
            placeholder="ابحث برقم العقد، اسم العميل، الجوال، المبنى، الحي، المدينة، الماركة، المحصل...",
            key="unified_search"
        )

        date_col1, date_col2 = st.columns(2)
        with date_col1:
            from_date = st.date_input("من تاريخ نهاية العقد", value=None, key="filter_end_from")
        with date_col2:
            to_date = st.date_input("إلى تاريخ نهاية العقد", value=None, key="filter_end_to")

        st.markdown('</div>', unsafe_allow_html=True)

        filtered_df = df.copy()

        if search_query:
            search_cols = [
                "contract_no", "customer_name", "mobile", "building_name",
                "district", "city", "elevator_brand", "collector",
                "payment_status", "contract_status", "elevator_type", "notes"
            ]
            mask = pd.Series(False, index=filtered_df.index)
            for col in search_cols:
                if col in filtered_df.columns:
                    mask = mask | filtered_df[col].astype(str).str.contains(search_query, case=False, na=False)
            filtered_df = filtered_df[mask]

        if from_date is not None:
            filtered_df = filtered_df[
                filtered_df["end_date_dt"].notna() & (filtered_df["end_date_dt"].dt.date >= from_date)
            ]
        if to_date is not None:
            filtered_df = filtered_df[
                filtered_df["end_date_dt"].notna() & (filtered_df["end_date_dt"].dt.date <= to_date)
            ]

        # ── Results Summary ──
        section_header("نتائج البحث")
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            metric_card("عدد النتائج", f"{len(filtered_df):,}", "📋", "blue")
        with r2:
            metric_card("إجمالي القيمة", f"{filtered_df['contract_value_num'].sum():,.0f}", "💰", "purple")
        with r3:
            metric_card("غير مسدد", f"{len(filtered_df[filtered_df['payment_status'] == 'غير مسدد']):,}", "⚠️", "danger")
        with r4:
            near_count = len(filtered_df[
                filtered_df["renewal_status"].isin(["منتهي", "ينتهي خلال 30 يوم", "ينتهي خلال 60 يوم", "ينتهي خلال 90 يوم"])
            ])
            metric_card("منتهي / قريب", f"{near_count:,}", "🔔", "warning")

        display_cols = [
            "id", "contract_no", "customer_name", "mobile", "building_name",
            "district", "city", "elevator_count", "elevator_type", "elevator_brand",
            "contract_value", "start_date", "end_date", "payment_status",
            "contract_status", "renewal_status", "collector", "notes"
        ]

        st.dataframe(
            filtered_df[[c for c in display_cols if c in filtered_df.columns]],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 تصدير النتائج CSV",
            data=to_csv_bytes(filtered_df),
            file_name=f"LIFTTECH_RESULTS_{date.today()}.csv",
            mime="text/csv"
        )

        # ── Edit Section ──
        if len(filtered_df) > 0:
            section_header("✏️ تعديل عقد")

            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            options = (
                filtered_df["id"].astype(str) + " - " +
                filtered_df["contract_no"].astype(str) + " - " +
                filtered_df["customer_name"].astype(str)
            )

            selected = st.selectbox("اختر العقد للتعديل", options, key="edit_selected_contract")
            selected_id = int(selected.split(" - ")[0])
            row = filtered_df[filtered_df["id"] == selected_id].iloc[0]
            st.markdown('</div>', unsafe_allow_html=True)

            # Customer info
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">👤 بيانات العميل والموقع</div>', unsafe_allow_html=True)

            e1, e2, e3 = st.columns(3)
            with e1:
                new_contract_no = st.text_input("رقم العقد", safe_text(row.get("contract_no")), key="edit_contract_no")
            with e2:
                new_customer_name = st.text_input("اسم العميل", safe_text(row.get("customer_name")), key="edit_customer_name")
            with e3:
                new_mobile = st.text_input("رقم الجوال", safe_text(row.get("mobile")), key="edit_mobile")

            e4, e5, e6 = st.columns(3)
            with e4:
                new_building_name = st.text_input("اسم المبنى / الموقع", safe_text(row.get("building_name")), key="edit_building_name")
            with e5:
                new_district = st.text_input("الحي", safe_text(row.get("district")), key="edit_district")
            with e6:
                new_city = st.text_input("المدينة", safe_text(row.get("city")), key="edit_city")

            st.markdown('</div>', unsafe_allow_html=True)

            # Elevator
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">🛗 تفاصيل المصعد</div>', unsafe_allow_html=True)

            elevator_type_options = ["ركاب", "خدمة", "بانوراما", "بضائع", "أخرى"]
            current_elevator_type = safe_text(row.get("elevator_type"))
            elevator_type_index = elevator_type_options.index(current_elevator_type) if current_elevator_type in elevator_type_options else 0

            e7, e8, e9 = st.columns(3)
            with e7:
                new_elevator_count = st.number_input("عدد المصاعد", min_value=1, step=1, value=safe_int(row.get("elevator_count"), 1), key="edit_elevator_count")
            with e8:
                new_elevator_type = st.selectbox("نوع المصعد", elevator_type_options, index=elevator_type_index, key="edit_elevator_type")
            with e9:
                new_elevator_brand = st.text_input("ماركة المصعد", safe_text(row.get("elevator_brand")), key="edit_elevator_brand")

            st.markdown('</div>', unsafe_allow_html=True)

            # Financials
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">📋 بيانات العقد المالية</div>', unsafe_allow_html=True)

            payment_options = ["مسدد", "مسدد جزئياً", "غير مسدد"]
            contract_options = ["نشط", "قريب الانتهاء", "منتهي", "موقوف"]
            collector_options = ["طه", "أحمد", "آخر"]

            current_payment_status = safe_text(row.get("payment_status"))
            payment_index = payment_options.index(current_payment_status) if current_payment_status in payment_options else 0
            current_contract_status = safe_text(row.get("contract_status"))
            contract_index = contract_options.index(current_contract_status) if current_contract_status in contract_options else 0
            current_collector = safe_text(row.get("collector"))
            collector_index = collector_options.index(current_collector) if current_collector in collector_options else 0

            e10, e11, e12 = st.columns(3)
            with e10:
                new_contract_value = st.number_input("قيمة العقد (ر.س)", min_value=0.0, step=100.0, value=safe_number(row.get("contract_value"), 0.0), key="edit_contract_value")
            with e11:
                new_start_date = st.date_input("تاريخ بداية العقد", value=parse_date_safe(row.get("start_date")), key="edit_start_date")
            with e12:
                new_end_date = st.date_input("تاريخ نهاية العقد", value=parse_date_safe(row.get("end_date")), key="edit_end_date")

            e13, e14, e15 = st.columns(3)
            with e13:
                new_payment_status = st.selectbox("حالة السداد", payment_options, index=payment_index, key="edit_payment_status")
            with e14:
                new_contract_status = st.selectbox("حالة العقد", contract_options, index=contract_index, key="edit_contract_status")
            with e15:
                new_collector = st.selectbox("مسؤول التحصيل", collector_options, index=collector_index, key="edit_collector")

            new_notes = st.text_area("ملاحظات", safe_text(row.get("notes")), key="edit_notes")
            st.markdown('</div>', unsafe_allow_html=True)

            col_save, _ = st.columns([1, 3])
            with col_save:
                if st.button("💾 حفظ التعديلات", key="save_edit", use_container_width=True):
                    update_data = {
                        "contract_no": new_contract_no.strip(),
                        "customer_name": new_customer_name.strip(),
                        "mobile": new_mobile.strip(),
                        "building_name": new_building_name.strip(),
                        "district": new_district.strip(),
                        "city": new_city.strip(),
                        "elevator_count": str(new_elevator_count),
                        "elevator_type": new_elevator_type,
                        "elevator_brand": new_elevator_brand.strip(),
                        "contract_value": str(new_contract_value),
                        "start_date": str(new_start_date),
                        "end_date": str(new_end_date),
                        "payment_status": new_payment_status,
                        "contract_status": new_contract_status,
                        "collector": new_collector,
                        "notes": new_notes.strip(),
                    }
                    supabase.table("contracts").update(update_data).eq("id", selected_id).execute()
                    st.success("✅ تم تعديل العقد بنجاح!")
                    st.rerun()

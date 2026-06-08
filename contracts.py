import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date, datetime
from io import BytesIO

# =========================================================
# LIFTTECH CONTRACTS SYSTEM - V2.2 CLEAN
# نظام إدارة عقود صيانة لفتك
# =========================================================

st.set_page_config(
    page_title="LiftTech | نظام عقود الصيانة",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

/* ===== Compact Login Page ===== */
.login-wrapper {
    min-height: 70vh;
    display: flex;
    align-items: center;
    justify-content: center;
    direction: rtl;
}

.login-card {
    width: 390px;
    padding: 28px 30px;
    border-radius: 22px;
    background: #ffffff;
    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.14);
    border: 1px solid #e5e7eb;
    text-align: center;
}

.brand-title {
    font-size: 34px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 2px;
}

.brand-subtitle {
    font-size: 17px;
    font-weight: 700;
    color: #dc2626;
    margin-bottom: 6px;
}

.version-badge {
    display: inline-block;
    padding: 5px 13px;
    border-radius: 999px;
    background: #0f172a;
    color: white;
    font-size: 12px;
    margin-bottom: 14px;
}

.footer-note {
    text-align:center;
    color:#64748b;
    font-size:12px;
    margin-top:12px;
}

/* ===== App UI ===== */
.metric-card {
    padding: 18px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 24px rgba(15,23,42,0.05);
    text-align: center;
    min-height: 100px;
}

.metric-title {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #0f172a;
    font-size: 24px;
    font-weight: 800;
    margin-top: 8px;
}

.section-title {
    color: #0f172a;
    font-size: 22px;
    font-weight: 800;
    margin-top: 8px;
    margin-bottom: 10px;
}

.alert-red {
    padding: 14px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    border-radius: 14px;
    font-weight: 700;
    text-align: center;
}

.alert-orange {
    padding: 14px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
    color: #9a3412;
    border-radius: 14px;
    font-weight: 700;
    text-align: center;
}

.alert-yellow {
    padding: 14px;
    background: #fefce8;
    border: 1px solid #fde68a;
    color: #854d0e;
    border-radius: 14px;
    font-weight: 700;
    text-align: center;
}

.alert-green {
    padding: 14px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
    border-radius: 14px;
    font-weight: 700;
    text-align: center;
}

.lift-header {
    padding: 18px 22px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 65%, #7f1d1d 100%);
    color: white;
    margin-bottom: 16px;
}

.lift-header h1 {
    margin: 0;
    font-size: 26px;
    font-weight: 800;
}

.lift-header p {
    margin: 5px 0 0 0;
    color: #cbd5e1;
    font-size: 13px;
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
        df["elevator_count"],
        errors="coerce"
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

    internal_cols = [
        "contract_value_num",
        "elevator_count_num",
        "start_date_dt",
        "end_date_dt",
        "days_to_end"
    ]

    for col in internal_cols:
        if col in export_df.columns:
            export_df = export_df.drop(columns=[col])

    return export_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def metric_card(title, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_unique_options(df, column):
    if df.empty or column not in df.columns:
        return ["الكل"]
    values = sorted([
        str(x).strip()
        for x in df[column].dropna().unique()
        if str(x).strip() != ""
    ])
    return ["الكل"] + values


# =========================================================
# Login Page
# =========================================================
def login():
    st.markdown('<div class="login-wrapper"><div class="login-card">', unsafe_allow_html=True)

    st.markdown('<div class="brand-title">LIFT TECH</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">مركز عمليات لفتك</div>', unsafe_allow_html=True)
    st.markdown('<div class="version-badge">عقود صيانة المصاعد | V2.2</div>', unsafe_allow_html=True)

    username = st.text_input("اسم المستخدم", key="login_username")
    password = st.text_input("كلمة المرور", type="password", key="login_password")

    if st.button("تسجيل الدخول", width="stretch"):
        users = st.secrets["users"]

        if username in users and password == users[username]:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

    st.markdown('<div class="footer-note">© 2026 LiftTech</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# =========================================================
# Authentication
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.sidebar.success(f"المستخدم: {st.session_state['username']}")

if st.sidebar.button("تسجيل خروج"):
    st.session_state["logged_in"] = False
    st.rerun()


# =========================================================
# Main Header
# =========================================================
st.markdown(
    f"""
    <div class="lift-header">
        <h1>نظام إدارة عقود صيانة لفتك</h1>
        <p>LiftTech Maintenance Command Center | آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["لوحة التحكم", "إضافة عقد", "عرض وتعديل العقود"])


# =========================================================
# Dashboard
# =========================================================
with tab1:
    st.markdown('<div class="section-title">مركز القيادة التشغيلي</div>', unsafe_allow_html=True)

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

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            metric_card("إجمالي العقود", f"{total_contracts:,}")
        with c2:
            metric_card("إجمالي قيمة العقود", f"{total_value:,.0f}")
        with c3:
            metric_card("العقود النشطة", f"{active_count:,}")
        with c4:
            metric_card("غير المسددة", f"{unpaid_count:,}")
        with c5:
            metric_card("عدد المصاعد", f"{elevator_total:,}")

        st.markdown("### تنبيهات التجديد")
        end_30 = len(df[df["renewal_status"] == "ينتهي خلال 30 يوم"])
        end_60 = len(df[df["renewal_status"] == "ينتهي خلال 60 يوم"])
        end_90 = len(df[df["renewal_status"] == "ينتهي خلال 90 يوم"])

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f'<div class="alert-red">منتهي بالفعل<br><b>{expired_count}</b></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="alert-orange">ينتهي خلال 30 يوم<br><b>{end_30}</b></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="alert-yellow">ينتهي خلال 60 يوم<br><b>{end_60}</b></div>', unsafe_allow_html=True)
        with r4:
            st.markdown(f'<div class="alert-green">ينتهي خلال 90 يوم<br><b>{end_90}</b></div>', unsafe_allow_html=True)

        st.markdown("### التحصيل")
        collection_rate = (paid_count / total_contracts * 100) if total_contracts else 0

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            metric_card("مسدد", f"{paid_count:,}")
        with p2:
            metric_card("مسدد جزئياً", f"{partial_paid_count:,}")
        with p3:
            metric_card("غير مسدد", f"{unpaid_count:,}")
        with p4:
            metric_card("نسبة السداد", f"{collection_rate:.1f}%")

        st.markdown("### مؤشرات تشغيلية")
        top_district = df["district"].value_counts().idxmax() if "district" in df.columns and not df["district"].dropna().empty else "-"
        top_brand = df["elevator_brand"].value_counts().idxmax() if "elevator_brand" in df.columns and not df["elevator_brand"].dropna().empty else "-"
        top_customer_row = df.sort_values("contract_value_num", ascending=False).head(1)
        top_customer = safe_text(top_customer_row["customer_name"].iloc[0]) if not top_customer_row.empty else "-"

        o1, o2, o3, o4 = st.columns(4)
        with o1:
            metric_card("أكثر حي", top_district)
        with o2:
            metric_card("أكثر ماركة", top_brand)
        with o3:
            metric_card("أكبر عميل", top_customer)
        with o4:
            metric_card("متوسط قيمة العقد", f"{avg_contract_value:,.0f}")

        st.markdown("### عقود حرجة")
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
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "تصدير العقود الحرجة CSV",
            data=to_csv_bytes(critical_df),
            file_name=f"LIFTTECH_CRITICAL_CONTRACTS_{date.today()}.csv",
            mime="text/csv"
        )

        st.markdown("### آخر 10 عقود مضافة")
        st.dataframe(
            df[[c for c in display_cols if c in df.columns]].head(10),
            width="stretch",
            hide_index=True
        )


# =========================================================
# Add Contract
# =========================================================
with tab2:
    st.subheader("إضافة عقد جديد")

    contract_no = st.text_input("رقم العقد", key="add_contract_no")
    customer_name = st.text_input("اسم العميل", key="add_customer_name")
    mobile = st.text_input("رقم الجوال", key="add_mobile")
    building_name = st.text_input("اسم المبنى / الموقع", key="add_building_name")
    district = st.text_input("الحي", key="add_district")
    city = st.text_input("المدينة", value="الرياض", key="add_city")

    c1, c2, c3 = st.columns(3)
    with c1:
        elevator_count = st.number_input("عدد المصاعد", min_value=1, step=1, key="add_elevator_count")
    with c2:
        elevator_type = st.selectbox("نوع المصعد", ["ركاب", "خدمة", "بانوراما", "بضائع", "أخرى"], key="add_elevator_type")
    with c3:
        elevator_brand = st.text_input("ماركة المصعد", key="add_elevator_brand")

    c4, c5, c6 = st.columns(3)
    with c4:
        contract_value = st.number_input("قيمة العقد", min_value=0.0, step=100.0, key="add_contract_value")
    with c5:
        start_date = st.date_input("تاريخ بداية العقد", key="add_start_date")
    with c6:
        end_date = st.date_input("تاريخ نهاية العقد", key="add_end_date")

    c7, c8, c9 = st.columns(3)
    with c7:
        payment_status = st.selectbox("حالة السداد", ["مسدد", "مسدد جزئياً", "غير مسدد"], key="add_payment_status")
    with c8:
        contract_status = st.selectbox("حالة العقد", ["نشط", "قريب الانتهاء", "منتهي", "موقوف"], key="add_contract_status")
    with c9:
        collector = st.selectbox("مسؤول التحصيل", ["طه", "أحمد", "آخر"], key="add_collector")

    notes = st.text_area("ملاحظات", key="add_notes")

    if st.button("حفظ العقد", key="save_contract"):
        if not contract_no.strip() or not customer_name.strip() or not mobile.strip():
            st.error("رقم العقد، اسم العميل، ورقم الجوال حقول إلزامية.")
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
            st.success("تم حفظ العقد في قاعدة البيانات السحابية بنجاح")
            st.rerun()


# =========================================================
# View / Edit
# =========================================================
with tab3:
    st.subheader("عرض وتعديل العقود")

    df = prepare_contracts_df(load_contracts())

    if df.empty:
        st.info("لا توجد عقود مسجلة")
    else:
        st.markdown("### أدوات البحث والفلاتر")

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            search_customer = st.text_input("اسم العميل", key="search_customer")
        with s2:
            search_contract = st.text_input("رقم العقد", key="search_contract")
        with s3:
            search_mobile = st.text_input("رقم الجوال", key="search_mobile")
        with s4:
            search_district = st.text_input("الحي", key="search_district")

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            filter_contract_status = st.selectbox("حالة العقد", get_unique_options(df, "contract_status"), key="filter_contract_status")
        with f2:
            filter_payment_status = st.selectbox("حالة السداد", get_unique_options(df, "payment_status"), key="filter_payment_status")
        with f3:
            filter_collector = st.selectbox("مسؤول التحصيل", get_unique_options(df, "collector"), key="filter_collector")
        with f4:
            filter_city = st.selectbox("المدينة", get_unique_options(df, "city"), key="filter_city")

        f5, f6 = st.columns(2)
        with f5:
            filter_renewal = st.selectbox(
                "حالة التجديد",
                ["الكل", "منتهي", "ينتهي خلال 30 يوم", "ينتهي خلال 60 يوم", "ينتهي خلال 90 يوم", "ساري", "غير محدد"],
                key="filter_renewal"
            )
        with f6:
            search_building = st.text_input("اسم المبنى / الموقع", key="search_building")

        filtered_df = df.copy()

        if search_customer:
            filtered_df = filtered_df[filtered_df["customer_name"].astype(str).str.contains(search_customer, case=False, na=False)]
        if search_contract:
            filtered_df = filtered_df[filtered_df["contract_no"].astype(str).str.contains(search_contract, case=False, na=False)]
        if search_mobile:
            filtered_df = filtered_df[filtered_df["mobile"].astype(str).str.contains(search_mobile, case=False, na=False)]
        if search_district:
            filtered_df = filtered_df[filtered_df["district"].astype(str).str.contains(search_district, case=False, na=False)]
        if search_building:
            filtered_df = filtered_df[filtered_df["building_name"].astype(str).str.contains(search_building, case=False, na=False)]

        if filter_contract_status != "الكل":
            filtered_df = filtered_df[filtered_df["contract_status"] == filter_contract_status]
        if filter_payment_status != "الكل":
            filtered_df = filtered_df[filtered_df["payment_status"] == filter_payment_status]
        if filter_collector != "الكل":
            filtered_df = filtered_df[filtered_df["collector"] == filter_collector]
        if filter_city != "الكل":
            filtered_df = filtered_df[filtered_df["city"] == filter_city]
        if filter_renewal != "الكل":
            filtered_df = filtered_df[filtered_df["renewal_status"] == filter_renewal]

        st.markdown("### نتائج البحث")

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            metric_card("عدد النتائج", f"{len(filtered_df):,}")
        with r2:
            metric_card("قيمة النتائج", f"{filtered_df['contract_value_num'].sum():,.0f}")
        with r3:
            metric_card("غير مسدد", f"{len(filtered_df[filtered_df['payment_status'] == 'غير مسدد']):,}")
        with r4:
            near_count = len(filtered_df[
                filtered_df["renewal_status"].isin(["منتهي", "ينتهي خلال 30 يوم", "ينتهي خلال 60 يوم", "ينتهي خلال 90 يوم"])
            ])
            metric_card("منتهي / قريب", f"{near_count:,}")

        display_cols = [
            "id", "contract_no", "customer_name", "mobile", "building_name",
            "district", "city", "elevator_count", "elevator_type", "elevator_brand",
            "contract_value", "start_date", "end_date", "payment_status",
            "contract_status", "renewal_status", "collector", "notes"
        ]

        st.dataframe(
            filtered_df[[c for c in display_cols if c in filtered_df.columns]],
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "تصدير النتائج CSV",
            data=to_csv_bytes(filtered_df),
            file_name=f"LIFTTECH_FILTERED_CONTRACTS_{date.today()}.csv",
            mime="text/csv"
        )

        if len(filtered_df) > 0:
            st.subheader("تعديل عقد")

            options = (
                filtered_df["id"].astype(str)
                + " - "
                + filtered_df["contract_no"].astype(str)
                + " - "
                + filtered_df["customer_name"].astype(str)
            )

            selected = st.selectbox("اختر العقد", options, key="edit_selected_contract")
            selected_id = int(selected.split(" - ")[0])
            row = filtered_df[filtered_df["id"] == selected_id].iloc[0]

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

            elevator_type_options = ["ركاب", "خدمة", "بانوراما", "بضائع", "أخرى"]
            current_elevator_type = safe_text(row.get("elevator_type"))
            elevator_type_index = elevator_type_options.index(current_elevator_type) if current_elevator_type in elevator_type_options else 0

            e7, e8, e9 = st.columns(3)
            with e7:
                new_elevator_count = st.number_input(
                    "عدد المصاعد",
                    min_value=1,
                    step=1,
                    value=safe_int(row.get("elevator_count"), 1),
                    key="edit_elevator_count"
                )
            with e8:
                new_elevator_type = st.selectbox(
                    "نوع المصعد",
                    elevator_type_options,
                    index=elevator_type_index,
                    key="edit_elevator_type"
                )
            with e9:
                new_elevator_brand = st.text_input("ماركة المصعد", safe_text(row.get("elevator_brand")), key="edit_elevator_brand")

            e10, e11, e12 = st.columns(3)
            with e10:
                new_contract_value = st.number_input(
                    "قيمة العقد",
                    min_value=0.0,
                    step=100.0,
                    value=safe_number(row.get("contract_value"), 0.0),
                    key="edit_contract_value"
                )
            with e11:
                new_start_date = st.date_input(
                    "تاريخ بداية العقد",
                    value=parse_date_safe(row.get("start_date")),
                    key="edit_start_date"
                )
            with e12:
                new_end_date = st.date_input(
                    "تاريخ نهاية العقد",
                    value=parse_date_safe(row.get("end_date")),
                    key="edit_end_date"
                )

            payment_options = ["مسدد", "مسدد جزئياً", "غير مسدد"]
            contract_options = ["نشط", "قريب الانتهاء", "منتهي", "موقوف"]
            collector_options = ["طه", "أحمد", "آخر"]

            current_payment_status = safe_text(row.get("payment_status"))
            payment_index = payment_options.index(current_payment_status) if current_payment_status in payment_options else 0

            current_contract_status = safe_text(row.get("contract_status"))
            contract_index = contract_options.index(current_contract_status) if current_contract_status in contract_options else 0

            current_collector = safe_text(row.get("collector"))
            collector_index = collector_options.index(current_collector) if current_collector in collector_options else 0

            e13, e14, e15 = st.columns(3)
            with e13:
                new_payment_status = st.selectbox("حالة السداد", payment_options, index=payment_index, key="edit_payment_status")
            with e14:
                new_contract_status = st.selectbox("حالة العقد", contract_options, index=contract_index, key="edit_contract_status")
            with e15:
                new_collector = st.selectbox("مسؤول التحصيل", collector_options, index=collector_index, key="edit_collector")

            new_notes = st.text_area("ملاحظات", safe_text(row.get("notes")), key="edit_notes")

            if st.button("حفظ التعديلات", key="save_edit"):
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
                st.success("تم تعديل العقد بنجاح")
                st.rerun()

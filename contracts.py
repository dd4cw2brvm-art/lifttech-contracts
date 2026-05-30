import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="نظام عقود صيانة لفتك", layout="wide")

def login():
    st.title("تسجيل الدخول - لفتك")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        users = st.secrets["users"]
        if username in users and password == users[username]:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.sidebar.success(f"المستخدم: {st.session_state['username']}")

if st.sidebar.button("تسجيل خروج"):
    st.session_state["logged_in"] = False
    st.rerun()

def load_contracts():
    response = supabase.table("contracts").select("*").order("id", desc=True).execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

st.title("نظام إدارة عقود صيانة لفتك")

tab1, tab2, tab3 = st.tabs(["لوحة التحكم", "إضافة عقد", "عرض وتعديل العقود"])

with tab1:
    st.subheader("لوحة التحكم")

    df = load_contracts()

    if len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("إجمالي العقود", len(df))
        total_value = pd.to_numeric(df["contract_value"], errors="coerce").fillna(0).sum()

col2.metric(
    "إجمالي قيمة العقود",
    f"{total_value:,.0f} ريال"
)
        col3.metric("العقود النشطة", len(df[df["contract_status"] == "نشط"]))
        col4.metric("غير المسددة", len(df[df["payment_status"] == "غير مسدد"]))

        st.subheader("آخر العقود")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("لا توجد عقود حتى الآن")

with tab2:
    st.subheader("إضافة عقد جديد")

    contract_no = st.text_input("رقم العقد", key="add_contract_no")
    customer_name = st.text_input("اسم العميل", key="add_customer_name")
    mobile = st.text_input("رقم الجوال", key="add_mobile")
    building_name = st.text_input("اسم المبنى / الموقع", key="add_building_name")
    district = st.text_input("الحي", key="add_district")
    city = st.text_input("المدينة", key="add_city")

    elevator_count = st.number_input("عدد المصاعد", min_value=1, step=1, key="add_elevator_count")
    elevator_type = st.selectbox("نوع المصعد", ["ركاب", "خدمة", "بانوراما", "أخرى"], key="add_elevator_type")
    elevator_brand = st.text_input("ماركة المصعد", key="add_elevator_brand")

    contract_value = st.number_input("قيمة العقد", min_value=0.0, step=100.0, key="add_contract_value")
    start_date = st.date_input("تاريخ بداية العقد", key="add_start_date")
    end_date = st.date_input("تاريخ نهاية العقد", key="add_end_date")

    payment_status = st.selectbox("حالة السداد", ["مسدد", "مسدد جزئياً", "غير مسدد"], key="add_payment_status")
    contract_status = st.selectbox("حالة العقد", ["نشط", "قريب الانتهاء", "منتهي", "موقوف"], key="add_contract_status")
    collector = st.selectbox("مسؤول التحصيل", ["طه", "أحمد", "آخر"], key="add_collector")
    notes = st.text_area("ملاحظات", key="add_notes")

    if st.button("حفظ العقد", key="save_contract"):
        data = {
            "contract_no": contract_no,
            "customer_name": customer_name,
            "mobile": mobile,
            "building_name": building_name,
            "district": district,
            "city": city,
            "elevator_count": elevator_count,
            "elevator_type": elevator_type,
            "elevator_brand": elevator_brand,
            "contract_value": contract_value,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "payment_status": payment_status,
            "contract_status": contract_status,
            "collector": collector,
            "notes": notes,
        }

        supabase.table("contracts").insert(data).execute()
        st.success("تم حفظ العقد في قاعدة البيانات السحابية بنجاح")

with tab3:
    st.subheader("عرض وتعديل العقود")

    df = load_contracts()

    if len(df) == 0:
        st.info("لا توجد عقود مسجلة")
        st.stop()

    st.markdown("### أدوات البحث")

    search = st.text_input("بحث عام: اسم العميل / الجوال / رقم العقد / اسم المبنى", key="search_all")

    col1, col2, col3 = st.columns(3)

    with col1:
        filter_contract_status = st.selectbox("حالة العقد", ["الكل", "نشط", "قريب الانتهاء", "منتهي", "موقوف"])

    with col2:
        filter_payment_status = st.selectbox("حالة السداد", ["الكل", "مسدد", "مسدد جزئياً", "غير مسدد"])

    with col3:
        filter_city = st.text_input("المدينة")

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["customer_name"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["mobile"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["contract_no"].astype(str).str.contains(search, case=False, na=False)
            | filtered_df["building_name"].astype(str).str.contains(search, case=False, na=False)
        ]

    if filter_contract_status != "الكل":
        filtered_df = filtered_df[filtered_df["contract_status"] == filter_contract_status]

    if filter_payment_status != "الكل":
        filtered_df = filtered_df[filtered_df["payment_status"] == filter_payment_status]

    if filter_city:
        filtered_df = filtered_df[
            filtered_df["city"].astype(str).str.contains(filter_city, case=False, na=False)
        ]

    st.markdown("### نتائج البحث")
    st.dataframe(filtered_df, use_container_width=True)
    st.metric("عدد النتائج", len(filtered_df))

    if len(filtered_df) > 0:
        st.subheader("تعديل عقد")

        options = filtered_df["id"].astype(str) + " - " + filtered_df["customer_name"].astype(str)
        selected = st.selectbox("اختر العقد", options, key="edit_selected_contract")

        selected_id = int(selected.split(" - ")[0])
        row = filtered_df[filtered_df["id"] == selected_id].iloc[0]

        new_customer_name = st.text_input("اسم العميل", row["customer_name"], key="edit_customer_name")
        new_mobile = st.text_input("رقم الجوال", row["mobile"], key="edit_mobile")
        new_building_name = st.text_input("اسم المبنى / الموقع", row["building_name"], key="edit_building_name")
        new_district = st.text_input("الحي", row["district"], key="edit_district")
        new_city = st.text_input("المدينة", row["city"], key="edit_city")

        new_elevator_count = st.number_input(
            "عدد المصاعد",
            min_value=1,
            step=1,
            value=int(row["elevator_count"]) if pd.notna(row["elevator_count"]) else 1,
            key="edit_elevator_count"
        )

        new_elevator_brand = st.text_input("ماركة المصعد", row["elevator_brand"], key="edit_elevator_brand")

        new_contract_value = st.number_input(
            "قيمة العقد",
            min_value=0.0,
            step=100.0,
            value=float(row["contract_value"]) if pd.notna(row["contract_value"]) else 0.0,
            key="edit_contract_value"
        )

        payment_options = ["مسدد", "مسدد جزئياً", "غير مسدد"]
        contract_options = ["نشط", "قريب الانتهاء", "منتهي", "موقوف"]

        new_payment_status = st.selectbox(
            "حالة السداد",
            payment_options,
            index=payment_options.index(row["payment_status"]) if row["payment_status"] in payment_options else 0,
            key="edit_payment_status"
        )

        new_contract_status = st.selectbox(
            "حالة العقد",
            contract_options,
            index=contract_options.index(row["contract_status"]) if row["contract_status"] in contract_options else 0,
            key="edit_contract_status"
        )

        new_notes = st.text_area("ملاحظات", row["notes"], key="edit_notes")

        if st.button("حفظ التعديلات", key="save_edit"):
            update_data = {
                "customer_name": new_customer_name,
                "mobile": new_mobile,
                "building_name": new_building_name,
                "district": new_district,
                "city": new_city,
                "elevator_count": new_elevator_count,
                "elevator_brand": new_elevator_brand,
                "contract_value": new_contract_value,
                "payment_status": new_payment_status,
                "contract_status": new_contract_status,
                "notes": new_notes,
            }

            supabase.table("contracts").update(update_data).eq("id", selected_id).execute()
            st.success("تم تعديل العقد بنجاح")
            st.rerun()

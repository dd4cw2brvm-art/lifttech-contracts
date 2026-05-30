import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("lifttech.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contracts_full (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_no TEXT,
    customer_name TEXT,
    mobile TEXT,
    building_name TEXT,
    district TEXT,
    city TEXT,
    elevator_count INTEGER,
    elevator_type TEXT,
    elevator_brand TEXT,
    contract_value REAL,
    start_date TEXT,
    end_date TEXT,
    billing_cycle TEXT,
    payment_status TEXT,
    contract_status TEXT,
    collector TEXT,
    notes TEXT
)
""")
conn.commit()

st.title("نظام إدارة عقود صيانة لفتك")

tab1, tab2, tab3 = st.tabs(["لوحة التحكم", "إضافة عقد", "عرض وتعديل العقود"])

with tab1:
    st.subheader("لوحة التحكم")
    df = pd.read_sql_query("SELECT * FROM contracts_full", conn)

    if len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("إجمالي العقود", len(df))
        col2.metric("إجمالي قيمة العقود", f"{df['contract_value'].sum():,.0f} ريال")
        col3.metric("العقود النشطة", len(df[df["contract_status"] == "نشط"]))
        col4.metric("غير المسددة", len(df[df["payment_status"] == "غير مسدد"]))

        st.subheader("آخر العقود")
        st.dataframe(df.tail(5))
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

    billing_cycle = st.selectbox("دورة الفوترة", ["شهري", "ربع سنوي", "نصف سنوي", "سنوي"], key="add_billing_cycle")
    payment_status = st.selectbox("حالة السداد", ["مسدد", "مسدد جزئياً", "غير مسدد"], key="add_payment_status")
    contract_status = st.selectbox("حالة العقد", ["نشط", "قريب الانتهاء", "منتهي", "موقوف"], key="add_contract_status")
    collector = st.selectbox("مسؤول التحصيل", ["طه", "أحمد", "آخر"], key="add_collector")

    notes = st.text_area("ملاحظات", key="add_notes")

    if st.button("حفظ العقد", key="save_contract"):
        cursor.execute("""
        INSERT INTO contracts_full (
            contract_no, customer_name, mobile, building_name, district, city,
            elevator_count, elevator_type, elevator_brand, contract_value,
            start_date, end_date, billing_cycle, payment_status,
            contract_status, collector, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contract_no, customer_name, mobile, building_name, district, city,
            elevator_count, elevator_type, elevator_brand, contract_value,
            str(start_date), str(end_date), billing_cycle, payment_status,
            contract_status, collector, notes
        ))

        conn.commit()
        st.success("تم حفظ العقد بنجاح")

with tab3:
    st.subheader("عرض وتعديل العقود")

    df = pd.read_sql_query("SELECT * FROM contracts_full", conn)

    st.markdown("### أدوات البحث")

    كلمة_البحث = st.text_input("بحث عام: اسم العميل / الجوال / رقم العقد / اسم المبنى", key="search_all")

    col_search1, col_search2, col_search3 = st.columns(3)

    with col_search1:
        فلتر_حالة_العقد = st.selectbox(
            "حالة العقد",
            ["الكل", "نشط", "قريب الانتهاء", "منتهي", "موقوف"],
            key="filter_contract_status"
        )

    with col_search2:
        فلتر_حالة_السداد = st.selectbox(
            "حالة السداد",
            ["الكل", "مسدد", "مسدد جزئياً", "غير مسدد"],
            key="filter_payment_status"
        )

    with col_search3:
        فلتر_المدينة = st.text_input("المدينة", key="filter_city")

    if كلمة_البحث:
        df = df[
            df["customer_name"].astype(str).str.contains(كلمة_البحث, case=False, na=False)
            |
            df["mobile"].astype(str).str.contains(كلمة_البحث, case=False, na=False)
            |
            df["contract_no"].astype(str).str.contains(كلمة_البحث, case=False, na=False)
            |
            df["building_name"].astype(str).str.contains(كلمة_البحث, case=False, na=False)
        ]

    if فلتر_حالة_العقد != "الكل":
        df = df[df["contract_status"] == فلتر_حالة_العقد]

    if فلتر_حالة_السداد != "الكل":
        df = df[df["payment_status"] == فلتر_حالة_السداد]

    if فلتر_المدينة:
        df = df[df["city"].astype(str).str.contains(فلتر_المدينة, case=False, na=False)]

    st.markdown("### نتائج البحث")
    st.dataframe(df)

    st.metric("عدد النتائج", len(df))

    if len(df) > 0:
        st.subheader("تعديل عقد")

        options = df["id"].astype(str) + " - " + df["customer_name"]
        selected = st.selectbox("اختر العقد", options, key="edit_selected_contract")

        selected_id = int(selected.split(" - ")[0])
        row = df[df["id"] == selected_id].iloc[0]

        new_customer_name = st.text_input("اسم العميل", row["customer_name"], key="edit_customer_name")
        new_mobile = st.text_input("رقم الجوال", row["mobile"], key="edit_mobile")
        new_building_name = st.text_input("اسم المبنى / الموقع", row["building_name"], key="edit_building_name")
        new_district = st.text_input("الحي", row["district"], key="edit_district")
        new_city = st.text_input("المدينة", row["city"], key="edit_city")

        new_elevator_count = st.number_input("عدد المصاعد", min_value=1, step=1, value=int(row["elevator_count"]), key="edit_elevator_count")
        new_elevator_brand = st.text_input("ماركة المصعد", row["elevator_brand"], key="edit_elevator_brand")
        new_contract_value = st.number_input("قيمة العقد", min_value=0.0, step=100.0, value=float(row["contract_value"]), key="edit_contract_value")

        new_payment_status = st.selectbox(
            "حالة السداد",
            ["مسدد", "مسدد جزئياً", "غير مسدد"],
            index=["مسدد", "مسدد جزئياً", "غير مسدد"].index(row["payment_status"]),
            key="edit_payment_status"
        )

        new_contract_status = st.selectbox(
            "حالة العقد",
            ["نشط", "قريب الانتهاء", "منتهي", "موقوف"],
            index=["نشط", "قريب الانتهاء", "منتهي", "موقوف"].index(row["contract_status"]),
            key="edit_contract_status"
        )

        new_notes = st.text_area("ملاحظات", row["notes"], key="edit_notes")

        if st.button("حفظ التعديلات", key="save_edit"):
            cursor.execute("""
            UPDATE contracts_full
            SET customer_name = ?,
                mobile = ?,
                building_name = ?,
                district = ?,
                city = ?,
                elevator_count = ?,
                elevator_brand = ?,
                contract_value = ?,
                payment_status = ?,
                contract_status = ?,
                notes = ?
            WHERE id = ?
            """, (
                new_customer_name, new_mobile, new_building_name,
                new_district, new_city, new_elevator_count,
                new_elevator_brand, new_contract_value,
                new_payment_status, new_contract_status,
                new_notes, selected_id
            ))

            conn.commit()
            st.success("تم تعديل العقد بنجاح")
            st.rerun()
    else:
        st.info("لا توجد نتائج مطابقة للبحث")
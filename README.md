# lifttech-contracts
LIFTTECH Maintenance Contracts System

## العملاء المتواصلون اليوم (لوحة مستقلة)

```powershell
streamlit run customers_today_dashboard.py
```

### النشر على Streamlit Cloud

1. أنشئ تطبيقاً جديداً من نفس المستودع.
2. اجعل **Main file path** = `customers_today_dashboard.py`
3. انسخ الأسرار من `.streamlit/secrets.toml.example` إلى Streamlit Secrets.
4. نفّذ `daily_contact_counts.sql` مرة واحدة في Supabase.

### السلوك

- سجل واحد لكل تاريخ بتوقيت الرياض
- أي تعديل يحدّث نفس السجل
- Supabase في الإنتاج، JSON محلي عند غياب Supabase

# SECURITY HOTFIX V18.1 — تقرير احتواء عاجل

| الحقل | القيمة |
|-------|--------|
| الفرع | `security-hotfix-v18-1` |
| المستودع | `dd4cw2brvm-art/lifttech-contracts` |
| التاريخ | 2026-07-10 |
| الحالة | **جاهز للمراجعة — لم يُدمج main ولم يُنشر** |
| المرحلة B | مؤجّلة حتى اعتماد Hotfix |

---

## ملخص تنفيذي

تم تطبيق **احتواء أمني فقط** على `contracts.py` دون إضافة ميزات CMMS ودون توسيع وظيفي للتطبيق.

---

## Before / After

| # | الثغرة / السلوك | قبل (V18) | بعد (V18.1) |
|---|-----------------|-----------|-------------|
| 1 | مصادقة من URL | `u/r/tk/cc/pg` تُستعاد وتُكتب في `query_params` | **محذوف بالكامل** — تُمسح معاملات الجلسة القديمة من الرابط |
| 2 | الدور الافتراضي | `admin` / `client` | **`deny`** — لا جلسة إلا بعد تحقق خادمي |
| 3 | دخول العملاء | مفعّل | **معطّل مؤقتاً** حتى RLS |
| 4 | UltraMsg | fallback ثابت في الكود عند غياب secrets | **secrets فقط** — فشل آمن بدون قيم افتراضية |
| 5 | audit_logs SQL | `ALTER ... DISABLE ROW LEVEL SECURITY` | **محذوف** — تعليق يوجّه لتفعيل RLS في Foundation |
| 6 | كلمة المرور | حد 6 أحرف، افتراضي 12345 مسموح | **حد 10 أحرف**، افتراضي محظور، forced reset مفعّل، إعادة تعيين 12345 معطّلة |
| 7 | الجلسات القديمة | بلا epoch | **`auth_epoch = v18.1-hotfix`** — إلغاء تلقائي للجلسات السابقة |
| 8 | إنشاء أمر العمل | استدعاء دوال بمعاملات خاطئة | **مصحّح** + حالة `assigned` في `WO_STATUSES` وانتقالاتها |
| 9 | عزل العميل | جزئي | `scope_by_client` في fault_reports / elevators / maintenance_logs / dashboard |
| 10 | plaintext auth | — | **ملاحظة صريحة**: سيُستبدل نهائياً في Foundation (Supabase Auth + JWT) |

---

## الملفات المتغيّرة

| ملف | نوع التغيير |
|-----|-------------|
| `contracts.py` | إصلاحات أمنية + عزل + WO fix |
| `security_hotfix.py` | **جديد** — دوال أمنية قابلة للاختبار |
| `tests/test_security_hotfix_v18_1.py` | **جديد** — 17 اختبار |
| `requirements.txt` | إضافة `pytest` |

---

## نتائج الاختبارات

```
17 passed in 0.04s
```

| الاختبار | النتيجة |
|----------|---------|
| رابط URL مصطنع لا يسجّل الدخول | PASS |
| لا يمكن تزوير admin role (دور غير معروف → deny) | PASS |
| الفني يرى مهامه فقط | PASS |
| العميل لا يرى بيانات عميل آخر | PASS |
| إنشاء أمر العمل (validate + duplicate) | PASS |
| غياب Secret لا يستخدم قيمة افتراضية | PASS |
| كلمة مرور افتراضية / حد 10 أحرف | PASS |
| بوابة العميل معطّلة | PASS |
| session epoch | PASS |

---

## Diff (ملخص)

```
 contracts.py     | 258 ++++++++++++++++++++++++++++++++-----------------------
 requirements.txt |   1 +
 security_hotfix.py (new)
 tests/test_security_hotfix_v18_1.py (new)
 2 files changed, 150 insertions(+), 109 deletions(-)
```

للـ diff الكامل من جذر المستودع:

```powershell
cd C:\Users\D\google-ads-integration\lifttech-contracts
git diff
```

---

## ما لم يُنفَّذ (عمداً)

- ❌ دمج `main`
- ❌ نشر Streamlit Cloud
- ❌ تنفيذ `ALTER TABLE audit_logs DISABLE ROW LEVEL SECURITY`
- ❌ بدء CMMS / المرحلة B (Supabase Auth + RLS كامل)

---

## المرحلة B (بعد اعتماد Hotfix)

1. Supabase Auth + JWT لكل مستخدم
2. RLS لكل جدول + Storage RLS
3. Audit triggers
4. staging مستقل
5. **ممنوع** توسيع `contracts.py` وظيفياً

---

## تحقق يدوي موصى به قبل النشر

1. تسجيل دخول staff صالح (غير عميل)
2. محاولة `?u=admin&r=admin&tk=...` — يجب ألا تُنشأ جلسة
3. محاولة دخول حساب `client` — رسالة تعطيل
4. إنشاء أمر عمل مع فني — حالة `مكلف`
5. إرسال WhatsApp بدون secrets — فشل آمن بدون تسريب

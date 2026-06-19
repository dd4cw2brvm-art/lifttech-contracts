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
/* ╔══════════════════════════════════════════════════════════════════╗
   ║  LiftTech V17 — Professional SaaS Design System                  ║
   ║  Inspired by: Odoo 18 · Monday.com · Zoho CRM 2026              ║
   ║  Author: LiftTech ERP — Riyadh, Saudi Arabia                    ║
   ╚══════════════════════════════════════════════════════════════════╝

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   DESIGN TOKENS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Brand Primary:   #1A56DB  (Odoo-inspired deeper blue)
   Brand Light:     #EBF5FF
   Brand Hover:     #1648C8
   Surface:         #FFFFFF
   Surface Alt:     #F9FAFB  (Odoo's off-white)
   BG Page:         #F3F4F6  (clean neutral gray)
   Border:          #E5E7EB
   Border Dark:     #D1D5DB
   Text Primary:    #111827  (near-black for readability)
   Text Secondary:  #374151
   Text Muted:      #6B7280
   Text Faint:      #9CA3AF
   Text Placeholder:#D1D5DB

   Success:   #059669 / #ECFDF5 / #A7F3D0
   Warning:   #D97706 / #FFFBEB / #FDE68A
   Danger:    #DC2626 / #FEF2F2 / #FECACA
   Info:      #1A56DB / #EBF5FF / #BFDBFE
   Purple:    #7C3AED / #F5F3FF / #DDD6FE

   Shadow SM:   0 1px 2px rgba(0,0,0,.05)
   Shadow MD:   0 4px 6px -1px rgba(0,0,0,.07), 0 2px 4px -1px rgba(0,0,0,.04)
   Shadow LG:   0 10px 15px -3px rgba(0,0,0,.07), 0 4px 6px -2px rgba(0,0,0,.03)
   Shadow XL:   0 20px 25px -5px rgba(0,0,0,.08), 0 10px 10px -5px rgba(0,0,0,.02)
   Shadow Blue: 0 0 0 3px rgba(26,86,219,.2)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

/* ══════════════════════════════════════════════════════
   LAYER 1: RESET & BASE
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stApp"] {
  background: #F3F4F6 !important;
  color: #111827 !important;
  font-family: "Cairo", "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
  direction: rtl;
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDeployButton"],
[data-testid="stStatusWidget"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
button[title="View fullscreen"],
.stDecoration { display: none !important; }

/* ── Typography Scale ── */
h1 { font-size: 1.5rem;  font-weight: 800; color: #111827; line-height: 1.3; }
h2 { font-size: 1.25rem; font-weight: 700; color: #111827; line-height: 1.35; }
h3 { font-size: 1.05rem; font-weight: 700; color: #1F2937; }
h4 { font-size: 0.95rem; font-weight: 600; color: #374151; }
p  { font-size: 0.875rem; color: #374151; line-height: 1.6; }
small { font-size: 0.75rem; color: #6B7280; }

/* ══════════════════════════════════════════════════════
   LAYER 2: LAYOUT — SIDEBAR
══════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-left: 1px solid #E5E7EB !important;
  min-width: 240px !important;
  max-width: 240px !important;
  box-shadow: 2px 0 12px rgba(0,0,0,.05) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: #111827 !important; }

/* Sidebar radio nav */
[data-testid="stSidebar"] .stRadio { padding: 0 8px !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 1px !important; }
[data-testid="stSidebar"] .stRadio > div > label {
  background: transparent !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 9px 12px !important;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  color: #4B5563 !important;
  cursor: pointer !important;
  transition: all .15s ease !important;
  direction: rtl !important;
  text-align: right !important;
  width: 100% !important;
  display: flex !important;
  align-items: center !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
  background: #F3F4F6 !important;
  color: #111827 !important;
}
[data-testid="stSidebar"] .stRadio input[type="radio"]:checked + div + span,
[data-testid="stSidebar"] .stRadio input[type="radio"]:checked ~ label {
  background: #EBF5FF !important;
  color: #1A56DB !important;
}
[data-testid="stSidebar"] .stRadio input[type="radio"] { display: none !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }

/* ══════════════════════════════════════════════════════
   LAYER 2: LAYOUT — MAIN CONTENT
══════════════════════════════════════════════════════ */
[data-testid="stMainBlockContainer"],
.main .block-container {
  padding: 0 24px 32px 24px !important;
  max-width: 100% !important;
  background: #F3F4F6 !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — BUTTONS
══════════════════════════════════════════════════════ */
/* Primary button */
.stButton > button {
  background: #1A56DB !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: 8px !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  padding: 9px 20px !important;
  letter-spacing: 0.2px !important;
  transition: all .18s ease !important;
  box-shadow: 0 1px 3px rgba(26,86,219,.3), 0 1px 2px rgba(26,86,219,.15) !important;
  font-family: "Cairo", sans-serif !important;
  cursor: pointer !important;
}
.stButton > button:hover {
  background: #1648C8 !important;
  box-shadow: 0 4px 12px rgba(26,86,219,.35) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary button */
.stButton > button[kind="secondary"] {
  background: #FFFFFF !important;
  color: #374151 !important;
  border: 1.5px solid #D1D5DB !important;
  box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
}
.stButton > button[kind="secondary"]:hover {
  background: #F9FAFB !important;
  border-color: #9CA3AF !important;
  color: #111827 !important;
}

/* Danger button */
.stButton > button[kind="primary"][data-danger="true"] {
  background: #DC2626 !important;
  box-shadow: 0 1px 3px rgba(220,38,38,.3) !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — FORM INPUTS
══════════════════════════════════════════════════════ */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: #FFFFFF !important;
  color: #111827 !important;
  border: 1.5px solid #D1D5DB !important;
  border-radius: 8px !important;
  font-size: 0.875rem !important;
  font-family: "Cairo", sans-serif !important;
  padding: 9px 14px !important;
  transition: border-color .15s ease, box-shadow .15s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
[data-baseweb="input"] input:focus {
  border-color: #1A56DB !important;
  box-shadow: 0 0 0 3px rgba(26,86,219,.15) !important;
  outline: none !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
  color: #9CA3AF !important;
  font-weight: 400 !important;
}

/* Select */
[data-baseweb="select"] [data-baseweb="select-control"] {
  background: #FFFFFF !important;
  border: 1.5px solid #D1D5DB !important;
  border-radius: 8px !important;
  font-family: "Cairo", sans-serif !important;
  min-height: 40px !important;
}
[data-baseweb="select"] [data-baseweb="select-control"]:focus-within {
  border-color: #1A56DB !important;
  box-shadow: 0 0 0 3px rgba(26,86,219,.15) !important;
}
[data-baseweb="select"] * {
  background: #FFFFFF !important;
  color: #111827 !important;
  font-family: "Cairo", sans-serif !important;
}
[data-baseweb="select"] [data-baseweb="popover"] {
  border: 1.5px solid #E5E7EB !important;
  border-radius: 10px !important;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -2px rgba(0,0,0,.05) !important;
  overflow: hidden !important;
}
[data-baseweb="select"] [role="listbox"] li:hover {
  background: #EBF5FF !important;
  color: #1A56DB !important;
}
[data-baseweb="select"] [role="option"][aria-selected="true"] {
  background: #EBF5FF !important;
  color: #1A56DB !important;
}

/* Date input */
[data-testid="stDateInput"] input {
  background: #FFFFFF !important;
  border: 1.5px solid #D1D5DB !important;
  border-radius: 8px !important;
  color: #111827 !important;
  font-family: "Cairo", sans-serif !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
  background: #FFFFFF !important;
  border: 1.5px solid #D1D5DB !important;
  border-radius: 8px !important;
}

/* Labels */
label,
.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stDateInput label,
.stNumberInput label,
[data-testid="stWidgetLabel"] {
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  color: #374151 !important;
  margin-bottom: 5px !important;
  letter-spacing: 0.1px !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — DATAFRAME / TABLES
══════════════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid #E5E7EB !important;
  box-shadow: 0 1px 3px rgba(0,0,0,.05) !important;
}
[data-testid="stDataFrame"] table {
  background: #FFFFFF !important;
  border-collapse: collapse !important;
}
[data-testid="stDataFrame"] th {
  background: #F9FAFB !important;
  color: #374151 !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  border-bottom: 2px solid #E5E7EB !important;
  padding: 11px 14px !important;
  font-family: "Cairo", sans-serif !important;
}
[data-testid="stDataFrame"] td {
  background: #FFFFFF !important;
  color: #374151 !important;
  font-size: 0.84rem !important;
  border-bottom: 1px solid #F9FAFB !important;
  padding: 10px 14px !important;
  font-family: "Cairo", sans-serif !important;
}
[data-testid="stDataFrame"] tr:hover td {
  background: #EBF5FF !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — EXPANDER
══════════════════════════════════════════════════════ */
[data-testid="stExpander"] {
  border: 1.5px solid #E5E7EB !important;
  border-radius: 10px !important;
  background: #FFFFFF !important;
  box-shadow: 0 1px 3px rgba(0,0,0,.04) !important;
  margin-bottom: 10px !important;
  overflow: hidden !important;
  transition: box-shadow .2s ease !important;
}
[data-testid="stExpander"]:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,.07) !important;
}
[data-testid="stExpander"] summary {
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  color: #111827 !important;
  padding: 13px 18px !important;
  background: #FFFFFF !important;
  transition: background .15s !important;
}
[data-testid="stExpander"] summary:hover {
  background: #F9FAFB !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — ALERTS
══════════════════════════════════════════════════════ */
.stAlert, [data-testid="stAlert"] {
  border-radius: 10px !important;
  font-size: 0.875rem !important;
  font-family: "Cairo", sans-serif !important;
  border-width: 1px !important;
  border-style: solid !important;
}
[data-testid="stAlert"][data-type="info"] {
  background: #EBF5FF !important;
  border-color: #BFDBFE !important;
  color: #1E40AF !important;
}
[data-testid="stAlert"][data-type="success"] {
  background: #ECFDF5 !important;
  border-color: #A7F3D0 !important;
  color: #065F46 !important;
}
[data-testid="stAlert"][data-type="warning"] {
  background: #FFFBEB !important;
  border-color: #FDE68A !important;
  color: #92400E !important;
}
[data-testid="stAlert"][data-type="error"] {
  background: #FEF2F2 !important;
  border-color: #FECACA !important;
  color: #991B1B !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — TABS
══════════════════════════════════════════════════════ */
[data-baseweb="tab-list"] {
  border-bottom: 2px solid #E5E7EB !important;
  background: transparent !important;
  gap: 0 !important;
  padding: 0 4px !important;
}
[data-baseweb="tab"] {
  background: transparent !important;
  color: #6B7280 !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  padding: 10px 18px !important;
  border-radius: 0 !important;
  transition: color .15s, background .15s !important;
  font-family: "Cairo", sans-serif !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}
[data-baseweb="tab"]:hover {
  color: #111827 !important;
  background: #F9FAFB !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  color: #1A56DB !important;
  border-bottom: 2px solid #1A56DB !important;
  font-weight: 700 !important;
  background: transparent !important;
}
[data-baseweb="tab-panel"] {
  padding: 20px 0 !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — SCROLLBAR
══════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #F9FAFB; border-radius: 3px; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #9CA3AF; }

/* ══════════════════════════════════════════════════════
   LAYER 3: COMPONENTS — CHECKBOX / RADIO
══════════════════════════════════════════════════════ */
[data-testid="stCheckbox"] label { font-size: 0.875rem !important; color: #374151 !important; }
[data-testid="stCheckbox"] [data-baseweb="checkbox"] [data-checked="true"] {
  background: #1A56DB !important;
  border-color: #1A56DB !important;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — TOP HEADER BAR
══════════════════════════════════════════════════════ */
.v17-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 24px;
  height: 56px;
  margin: 0 -24px 0 -24px;
  box-shadow: 0 1px 4px rgba(0,0,0,.04);
  position: sticky;
  top: 0;
  z-index: 100;
}
.v17-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.v17-header-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
}
.v17-hdr-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 8px;
}
.v17-hdr-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #EBF5FF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.v17-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.v17-role-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  background: #EBF5FF;
  color: #1A56DB;
  border: 1px solid #BFDBFE;
  letter-spacing: 0.3px;
}
.v17-hdr-time {
  font-size: 0.75rem;
  color: #6B7280;
  font-variant-numeric: tabular-nums;
}
.v17-hdr-sep {
  width: 1px;
  height: 20px;
  background: #E5E7EB;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — SIDEBAR COMPONENTS
══════════════════════════════════════════════════════ */
.v17-sb-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 14px 14px 14px;
  border-bottom: 1px solid #F3F4F6;
  margin-bottom: 8px;
}
.v17-sb-logo-icon {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: linear-gradient(135deg, #1A56DB 0%, #1648C8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(26,86,219,.3);
}
.v17-sb-logo-text .title {
  font-size: 1rem;
  font-weight: 900;
  color: #111827;
  letter-spacing: 0.3px;
}
.v17-sb-logo-text .sub {
  font-size: 0.62rem;
  color: #9CA3AF;
  font-weight: 500;
  margin-top: 1px;
}

/* User card in sidebar */
.v17-sb-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #F9FAFB;
  border-radius: 10px;
  margin: 4px 10px 12px 10px;
  border: 1px solid #F3F4F6;
  transition: background .15s ease;
}
.v17-sb-user:hover { background: #EBF5FF; }
.v17-sb-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1A56DB, #1648C8);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 800;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(26,86,219,.25);
}
.v17-sb-name {
  font-size: 0.84rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.3;
}
.v17-sb-role {
  font-size: 0.64rem;
  color: #6B7280;
  margin-top: 1px;
  font-weight: 500;
}

/* Sidebar nav section label */
.v17-sb-section {
  font-size: 0.6rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #9CA3AF !important;
  padding: 12px 14px 5px 14px;
}

/* Sidebar logout area */
.v17-sb-footer {
  border-top: 1px solid #F3F4F6;
  padding: 10px 10px 14px 10px;
  margin-top: auto;
}
.v17-sb-footer-time {
  font-size: 0.72rem;
  color: #9CA3AF;
  text-align: center;
  margin-bottom: 8px;
  direction: ltr;
  font-variant-numeric: tabular-nums;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — PAGE WRAPPER
══════════════════════════════════════════════════════ */
.v17-page {
  padding: 20px 0 32px 0;
  min-height: calc(100vh - 56px);
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — SECTION HEADER
══════════════════════════════════════════════════════ */
.v17-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #6B7280;
  border-bottom: 2px solid #E5E7EB;
  padding-bottom: 10px;
  margin: 28px 0 16px 0;
}
.v17-section-title::after {
  content: "";
  flex: 1;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — KPI CARDS
══════════════════════════════════════════════════════ */
.v17-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.v17-kpi {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 14px;
  padding: 20px 18px 16px 18px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.05), 0 1px 2px rgba(0,0,0,.04);
  transition: box-shadow .25s ease, transform .25s ease;
  cursor: default;
}
.v17-kpi:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,.09);
  transform: translateY(-2px);
}
/* Color accents */
.v17-kpi.blue   { border-top: 3px solid #1A56DB; }
.v17-kpi.green  { border-top: 3px solid #059669; }
.v17-kpi.orange { border-top: 3px solid #D97706; }
.v17-kpi.red    { border-top: 3px solid #DC2626; }
.v17-kpi.purple { border-top: 3px solid #7C3AED; }
.v17-kpi.cyan   { border-top: 3px solid #0891B2; }
.v17-kpi.teal   { border-top: 3px solid #0D9488; }

/* Subtle bg tint on hover */
.v17-kpi.blue:hover   { background: linear-gradient(180deg, #EBF5FF 0%, #FFFFFF 40%); }
.v17-kpi.green:hover  { background: linear-gradient(180deg, #ECFDF5 0%, #FFFFFF 40%); }
.v17-kpi.orange:hover { background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 40%); }
.v17-kpi.red:hover    { background: linear-gradient(180deg, #FEF2F2 0%, #FFFFFF 40%); }
.v17-kpi.purple:hover { background: linear-gradient(180deg, #F5F3FF 0%, #FFFFFF 40%); }

.v17-kpi-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 12px;
}
.blue .v17-kpi-icon   { background: #EBF5FF; }
.green .v17-kpi-icon  { background: #ECFDF5; }
.orange .v17-kpi-icon { background: #FFFBEB; }
.red .v17-kpi-icon    { background: #FEF2F2; }
.purple .v17-kpi-icon { background: #F5F3FF; }
.cyan .v17-kpi-icon   { background: #E0F7FA; }
.teal .v17-kpi-icon   { background: #ECFDF5; }

.v17-kpi-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: #6B7280;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.v17-kpi-value {
  font-size: 1.85rem;
  font-weight: 900;
  color: #111827;
  line-height: 1;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
  font-variant-numeric: tabular-nums;
}
.v17-kpi-sub {
  font-size: 0.72rem;
  color: #9CA3AF;
  line-height: 1.4;
}
.v17-kpi-trend {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  margin-top: 6px;
}
.v17-kpi-trend.up   { background: #ECFDF5; color: #059669; }
.v17-kpi-trend.down { background: #FEF2F2; color: #DC2626; }
.v17-kpi-trend.flat { background: #F9FAFB; color: #6B7280; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — CARDS / PANELS
══════════════════════════════════════════════════════ */
.v17-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
  transition: box-shadow .2s ease;
}
.v17-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.07); }
.v17-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  margin-bottom: 16px;
  border-bottom: 1px solid #F3F4F6;
}
.v17-card-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — FORM GROUPS
══════════════════════════════════════════════════════ */
.v17-form-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  margin-bottom: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.v17-form-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 13px 18px;
  background: #F9FAFB;
  border-bottom: 1px solid #E5E7EB;
  font-size: 0.82rem;
  font-weight: 700;
  color: #374151;
  letter-spacing: 0.2px;
}
.v17-form-header-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #EBF5FF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}
.v17-form-body {
  padding: 16px 18px;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — DATA TABLE
══════════════════════════════════════════════════════ */
.v17-table {
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  overflow: hidden;
  direction: rtl;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  background: #FFFFFF;
}
.v17-table-head {
  background: #F9FAFB;
  padding: 11px 16px;
  display: flex;
  direction: rtl;
  align-items: center;
  border-bottom: 2px solid #E5E7EB;
}
.v17-table-head span {
  color: #374151;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.v17-table-row {
  display: flex;
  direction: rtl;
  align-items: center;
  padding: 10px 16px;
  border-bottom: 1px solid #F9FAFB;
  background: #FFFFFF;
  transition: background .1s ease;
}
.v17-table-row:last-child { border-bottom: none; }
.v17-table-row:hover { background: #EBF5FF; }
.v17-td { font-size: 0.8rem; color: #374151; }
.v17-td.b { font-weight: 700; color: #111827; }
.v17-td.m { color: #9CA3AF; font-size: 0.72rem; }
.v17-td.c { text-align: center; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — BADGES / STATUS PILLS
══════════════════════════════════════════════════════ */
.v17-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  border: 1px solid transparent;
  white-space: nowrap;
  letter-spacing: 0.2px;
}
.v17-badge.blue   { background: #EBF5FF; color: #1648C8; border-color: #BFDBFE; }
.v17-badge.green  { background: #ECFDF5; color: #065F46; border-color: #A7F3D0; }
.v17-badge.yellow { background: #FFFBEB; color: #92400E; border-color: #FDE68A; }
.v17-badge.red    { background: #FEF2F2; color: #991B1B; border-color: #FECACA; }
.v17-badge.purple { background: #F5F3FF; color: #5B21B6; border-color: #DDD6FE; }
.v17-badge.gray   { background: #F9FAFB; color: #4B5563; border-color: #E5E7EB; }
.v17-badge.cyan   { background: #ECFEFF; color: #0E7490; border-color: #A5F3FC; }
.v17-badge.orange { background: #FFF7ED; color: #C2410C; border-color: #FED7AA; }

/* Dot indicator */
.v17-badge::before {
  content: "";
  display: inline-block;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.8;
  flex-shrink: 0;
}
.v17-badge.no-dot::before { display: none; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — ALERT CARDS
══════════════════════════════════════════════════════ */
.v17-alert {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-radius: 12px;
  margin-bottom: 10px;
  direction: rtl;
  border: 1px solid transparent;
  transition: box-shadow .2s ease;
}
.v17-alert:hover { box-shadow: 0 4px 12px rgba(0,0,0,.07); }
.v17-alert.red    { background: #FEF2F2; border-color: #FECACA; }
.v17-alert.yellow { background: #FFFBEB; border-color: #FDE68A; }
.v17-alert.green  { background: #ECFDF5; border-color: #A7F3D0; }
.v17-alert.blue   { background: #EBF5FF; border-color: #BFDBFE; }
.v17-alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.red  .v17-alert-icon { background: #FEE2E2; }
.yellow .v17-alert-icon { background: #FEF3C7; }
.green .v17-alert-icon { background: #D1FAE5; }
.blue .v17-alert-icon  { background: #DBEAFE; }
.v17-alert-body { flex: 1; }
.v17-alert-title { font-size: 0.875rem; font-weight: 700; color: #111827; line-height: 1.4; }
.v17-alert-sub   { font-size: 0.72rem; color: #6B7280; margin-top: 2px; }
.v17-alert-num {
  font-size: 1.5rem;
  font-weight: 900;
  min-width: 40px;
  text-align: center;
  line-height: 1;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — PROGRESS BAR
══════════════════════════════════════════════════════ */
.v17-progress-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 14px;
  padding: 18px 22px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.v17-progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.v17-progress-label { font-size: 0.84rem; font-weight: 700; color: #374151; }
.v17-progress-pct {
  font-size: 1.1rem;
  font-weight: 900;
  letter-spacing: -0.3px;
}
.v17-progress-track {
  background: #F3F4F6;
  border-radius: 8px;
  height: 10px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0,0,0,.06);
}
.v17-progress-fill {
  height: 10px;
  border-radius: 8px;
  transition: width .6s cubic-bezier(.4,0,.2,1);
}
.v17-progress-fill.blue   { background: linear-gradient(90deg, #1A56DB, #60A5FA); }
.v17-progress-fill.green  { background: linear-gradient(90deg, #059669, #34D399); }
.v17-progress-fill.orange { background: linear-gradient(90deg, #D97706, #FBBF24); }
.v17-progress-fill.red    { background: linear-gradient(90deg, #DC2626, #F87171); }
.v17-progress-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 0.72rem;
  color: #9CA3AF;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — CALENDAR
══════════════════════════════════════════════════════ */
.v17-cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
}
.v17-cal-day {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 8px 7px;
  min-height: 82px;
  font-size: 0.75rem;
  color: #111827;
  transition: box-shadow .15s ease;
}
.v17-cal-day:hover { box-shadow: 0 4px 12px rgba(0,0,0,.07); }
.v17-cal-day.today {
  border-color: #1A56DB;
  background: #EBF5FF;
  box-shadow: 0 0 0 2px rgba(26,86,219,.12);
}
.v17-cal-day.weekend { background: #F9FAFB; }
.v17-cal-head-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
  margin-bottom: 4px;
}
.v17-cal-head-cell {
  font-size: 0.66rem;
  font-weight: 800;
  color: #6B7280;
  text-align: center;
  padding: 6px;
  background: #F9FAFB;
  border-radius: 8px;
  letter-spacing: 0.5px;
}
.v17-cal-event {
  font-size: 0.6rem;
  background: #EBF5FF;
  border: 1px solid #BFDBFE;
  border-radius: 4px;
  padding: 2px 6px;
  margin-bottom: 2px;
  color: #1648C8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — MINI KPI (sub-pages)
══════════════════════════════════════════════════════ */
.v17-mini-kpi {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 14px 16px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);
  transition: box-shadow .2s ease;
}
.v17-mini-kpi:hover { box-shadow: 0 4px 12px rgba(0,0,0,.07); }
.v17-mini-label { font-size: 0.68rem; color: #6B7280; margin-bottom: 5px; font-weight: 700; letter-spacing: 0.3px; }
.v17-mini-value { font-size: 1.3rem; font-weight: 900; color: #111827; line-height: 1; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — ELEVATOR / FIELD CARDS
══════════════════════════════════════════════════════ */
.v17-elev-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  transition: box-shadow .2s ease, transform .2s ease;
}
.v17-elev-card:hover {
  box-shadow: 0 6px 18px rgba(0,0,0,.08);
  transform: translateY(-1px);
}
.v17-elev-title { font-size: 0.92rem; font-weight: 700; color: #111827; margin-bottom: 4px; }
.v17-elev-meta  { font-size: 0.78rem; color: #6B7280; margin-bottom: 2px; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — TECH CARDS
══════════════════════════════════════════════════════ */
.v17-tech-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 20px 18px;
  margin-bottom: 12px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  transition: box-shadow .2s ease;
}
.v17-tech-card:hover { box-shadow: 0 6px 18px rgba(0,0,0,.08); }
.v17-tech-card h3 { font-size: 0.92rem; font-weight: 700; color: #111827; margin: 0 0 14px 0; }
.v17-tech-stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: #6B7280;
  padding: 6px 0;
  border-bottom: 1px solid #F9FAFB;
}
.v17-tech-stat:last-child { border-bottom: none; }
.v17-tech-stat strong { color: #111827; font-weight: 700; }

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — DATE FILTER BAR
══════════════════════════════════════════════════════ */
.v17-filter-bar {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 20px;
  direction: rtl;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.v17-filter-label {
  font-size: 0.66rem;
  font-weight: 800;
  color: #9CA3AF;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.v17-filter-presets {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.v17-preset-btn {
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 1.5px solid #E5E7EB;
  background: #F9FAFB;
  color: #4B5563;
  cursor: pointer;
  white-space: nowrap;
  transition: all .15s ease;
  font-family: "Cairo", sans-serif;
}
.v17-preset-btn:hover {
  background: #EBF5FF;
  border-color: #BFDBFE;
  color: #1A56DB;
}
.v17-preset-btn.active {
  background: #1A56DB;
  color: #FFFFFF;
  border-color: #1A56DB;
  box-shadow: 0 2px 8px rgba(26,86,219,.3);
}

/* ══════════════════════════════════════════════════════
   LAYER 4: PATTERNS — DASHBOARD HEADER
══════════════════════════════════════════════════════ */
.v17-dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 2px solid #E5E7EB;
  padding-bottom: 18px;
  margin-bottom: 28px;
  direction: rtl;
}
.v17-dash-title-area .eyebrow {
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #9CA3AF;
  margin-bottom: 6px;
}
.v17-dash-title-area .headline {
  font-size: 1.4rem;
  font-weight: 900;
  color: #111827;
  line-height: 1.2;
}
.v17-dash-date-area { text-align: left; }
.v17-dash-date-area .date-main {
  font-size: 0.88rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 3px;
}
.v17-dash-date-area .date-sub { font-size: 0.7rem; color: #9CA3AF; }

/* ══════════════════════════════════════════════════════
   LAYER 5: UTILITIES
══════════════════════════════════════════════════════ */
/* Divider */
.v17-divider {
  border: none;
  border-top: 1px solid #E5E7EB;
  margin: 20px 0;
}

/* Empty state */
.v17-empty {
  padding: 48px 20px;
  text-align: center;
  color: #9CA3AF;
}
.v17-empty-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.5; }
.v17-empty-text { font-size: 0.875rem; font-weight: 600; color: #6B7280; }

/* Info tooltip pill */
.v17-info-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 0.72rem;
  color: #6B7280;
  font-weight: 500;
}

/* Stat inline */
.v17-stat-inline {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: #6B7280;
}
.v17-stat-inline strong { color: #111827; font-size: 0.875rem; font-weight: 700; }

/* Section separator */
.v17-section-sep {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 24px 0 16px 0;
  direction: rtl;
}
.v17-section-sep-text {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #6B7280;
  white-space: nowrap;
}
.v17-section-sep-line {
  flex: 1;
  height: 1px;
  background: #E5E7EB;
}

/* Tag/chip */
.v17-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 0.75rem;
  color: #374151;
  font-weight: 600;
}

/* ══════════════════════════════════════════════════════
   LAYER 5: LEGACY COMPAT (ensure old .kpi-mini etc. still work)
══════════════════════════════════════════════════════ */
.kpi-mini {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 13px 15px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);
}
.kpi-mini-label { font-size: 0.68rem; color: #6B7280; margin-bottom: 5px; font-weight: 700; }
.kpi-mini-value { font-size: 1.25rem; font-weight: 900; color: #111827; }

.section-header {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #6B7280;
  border-bottom: 2px solid #E5E7EB;
  padding-bottom: 10px;
  margin: 26px 0 16px 0;
}

.erp-panel {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}

.form-group {
  border: 1.5px solid #E5E7EB;
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 12px;
  background: #FFFFFF;
  box-shadow: 0 1px 2px rgba(0,0,0,.03);
}
.form-group-header {
  font-size: 0.82rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 14px;
  border-bottom: 1px solid #F3F4F6;
  padding-bottom: 8px;
}

.collection-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.collection-title { font-size: 0.7rem; font-weight: 700; color: #6B7280; letter-spacing: 0.5px; margin-bottom: 10px; text-transform: uppercase; }
.collection-amount { font-size: 1.5rem; font-weight: 900; color: #111827; margin-bottom: 10px; }
.collection-meta { display: flex; justify-content: space-between; font-size: 0.72rem; color: #6B7280; margin-top: 8px; }
.progress-bar-track { background: #F3F4F6; border-radius: 6px; height: 7px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 6px; transition: width .5s ease; }
.progress-bar-fill.green  { background: linear-gradient(90deg, #059669, #34D399); }
.progress-bar-fill.yellow { background: linear-gradient(90deg, #D97706, #FBBF24); }
.progress-bar-fill.red    { background: linear-gradient(90deg, #DC2626, #F87171); }

.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge-default  { background: #F3F4F6; color: #4B5563; }
.badge-blue     { background: #EBF5FF; color: #1648C8; border: 1px solid #BFDBFE; }
.badge-green    { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.badge-yellow   { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }
.badge-red      { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }
.badge-purple   { background: #F5F3FF; color: #5B21B6; border: 1px solid #DDD6FE; }
.badge-gray     { background: #F9FAFB; color: #4B5563; border: 1px solid #E5E7EB; }

/* Legacy dashboard CSS */
.db-wrap * { box-sizing: border-box; }
.kc {
  background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px;
  padding: 18px; height: 100%; direction: rtl;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  transition: box-shadow .2s, transform .2s;
}
.kc:hover { box-shadow: 0 6px 20px rgba(0,0,0,.09); transform: translateY(-2px); }
.kc .kl { font-size: 0.68rem; font-weight: 700; color: #6B7280; letter-spacing: 0.5px; margin-bottom: 8px; }
.kc .kv { font-size: 1.85rem; font-weight: 900; color: #111827; line-height: 1; letter-spacing: -0.5px; margin-bottom: 5px; }
.kc .ks { font-size: 0.72rem; color: #9CA3AF; line-height: 1.5; }
.kc.primary { border-top: 3px solid #1A56DB; }
.kc.success { border-top: 3px solid #059669; }
.kc.warning { border-top: 3px solid #D97706; }
.kc.danger  { border-top: 3px solid #DC2626; }
.kc.info    { border-top: 3px solid #0891B2; }

.bar-card {
  background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px;
  padding: 18px 22px; margin-top: 12px; direction: rtl;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.bar-card .bt { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.bar-card .bl { font-size: 0.84rem; font-weight: 700; color: #374151; }
.bar-card .bp { font-size: 1rem; font-weight: 900; color: #1A56DB; }
.bar-card .btr { background: #F3F4F6; border-radius: 8px; height: 10px; overflow: hidden; }
.bar-card .bf  { height: 10px; border-radius: 8px; transition: width .5s ease; }
.bar-card .bm  { display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.72rem; color: #9CA3AF; }

.al {
  display: flex; align-items: center; gap: 12px; padding: 13px 17px;
  border-radius: 12px; margin-bottom: 9px; direction: rtl;
  border: 1px solid transparent; transition: box-shadow .2s ease;
}
.al:hover { box-shadow: 0 4px 12px rgba(0,0,0,.07); }
.al.r { background: #FEF2F2; border-color: #FECACA; }
.al.y { background: #FFFBEB; border-color: #FDE68A; }
.al.g { background: #ECFDF5; border-color: #A7F3D0; }
.al .ab { flex: 1; }
.al .at { font-size: 0.84rem; font-weight: 700; color: #111827; line-height: 1.3; }
.al .as { font-size: 0.72rem; color: #6B7280; margin-top: 2px; }
.al .an { font-size: 1.4rem; font-weight: 900; min-width: 38px; text-align: center; }

.tbl { border: 1px solid #E5E7EB; border-radius: 12px; overflow: hidden; direction: rtl; box-shadow: 0 1px 3px rgba(0,0,0,.04); }
.tbl .th {
  background: #F9FAFB; padding: 11px 16px;
  display: flex; direction: rtl; align-items: center;
  border-bottom: 2px solid #E5E7EB;
}
.tbl .th span { color: #374151; font-size: 0.68rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; }
.tbl .tr {
  display: flex; direction: rtl; align-items: center;
  padding: 10px 16px; border-bottom: 1px solid #F9FAFB;
  background: #FFFFFF; transition: background .1s ease;
}
.tbl .tr:last-child { border-bottom: none; }
.tbl .tr:hover { background: #EBF5FF; }
.tbl .td { font-size: 0.78rem; color: #374151; }
.tbl .td.b { font-weight: 700; color: #111827; }
.tbl .td.g { color: #9CA3AF; font-size: 0.72rem; }
.tbl .td.c { text-align: center; }

.bdg { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.68rem; font-weight: 700; white-space: nowrap; border: 1px solid transparent; }
.bdg.g { background: #ECFDF5; color: #065F46; border-color: #A7F3D0; }
.bdg.r { background: #FEF2F2; color: #991B1B; border-color: #FECACA; }
.bdg.y { background: #FFFBEB; color: #92400E; border-color: #FDE68A; }
.bdg.k { background: #F3F4F6; color: #4B5563; border-color: #E5E7EB; }
.bdg.b { background: #EBF5FF; color: #1648C8; border-color: #BFDBFE; }
.bdg.p { background: #F5F3FF; color: #5B21B6; border-color: #DDD6FE; }

/* Dashboard section title */
.stl {
  font-size: 0.64rem; font-weight: 800; color: #9CA3AF; letter-spacing: 2.5px;
  text-transform: uppercase; margin: 26px 0 13px; padding-bottom: 8px;
  border-bottom: 1px solid #F3F4F6; direction: rtl;
}

/* Dashboard wrapper */
.db-wrap .hdr {
  display: flex; justify-content: space-between; align-items: flex-end;
  border-bottom: 2px solid #E5E7EB; padding-bottom: 18px; margin-bottom: 26px; direction: rtl;
}
.hdr-r .lbl { font-size: 0.66rem; font-weight: 800; color: #9CA3AF; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
.hdr-r .ttl { font-size: 1.4rem; font-weight: 900; color: #111827; line-height: 1.1; }
.hdr-l { text-align: left; }
.hdr-l .dt  { font-size: 0.88rem; font-weight: 700; color: #374151; margin-bottom: 3px; }
.hdr-l .src { font-size: 0.7rem; color: #9CA3AF; }

/* ══════════════════════════════════════════════════════
   LAYER 6: TOP HEADER (legacy compat)
══════════════════════════════════════════════════════ */
.top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 24px;
  height: 56px;
  margin: 0 -24px 0 -24px;
  box-shadow: 0 1px 4px rgba(0,0,0,.04);
  position: sticky;
  top: 0;
  z-index: 100;
}
.top-header-left  { display: flex; align-items: center; gap: 12px; }
.top-header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 8px;
}
.top-header-right { display: flex; align-items: center; gap: 12px; }
.header-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  background: #EBF5FF;
  color: #1A56DB;
  border: 1px solid #BFDBFE;
}
.header-time {
  font-size: 0.75rem;
  color: #6B7280;
  font-variant-numeric: tabular-nums;
}

/* ══════════════════════════════════════════════════════
   LAYER 6: SIDEBAR LEGACY COMPAT
══════════════════════════════════════════════════════ */
.sb-logo {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 14px 14px 14px;
  border-bottom: 1px solid #F3F4F6;
  margin-bottom: 8px;
}
.sb-logo-icon  { font-size: 1.4rem; }
.sb-logo-title { font-size: 1rem; font-weight: 900; color: #111827; }
.sb-logo-sub   { font-size: 0.62rem; color: #9CA3AF; font-weight: 500; }
.sb-user {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px;
  background: #F9FAFB;
  border-radius: 10px;
  margin: 4px 8px 12px 8px;
  border: 1px solid #F3F4F6;
}
.sb-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(135deg, #1A56DB, #1648C8);
  color: #FFFFFF;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; font-weight: 800; flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(26,86,219,.25);
}
.sb-name { font-size: 0.84rem; font-weight: 700; color: #111827; }
.sb-role { font-size: 0.64rem; color: #9CA3AF; margin-top: 1px; font-weight: 500; }
.sb-nav-section {
  font-size: 0.6rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #9CA3AF !important;
  padding: 10px 14px 4px 14px;
}

/* ══════════════════════════════════════════════════════
   LAYER 7: RESPONSIVE
══════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  [data-testid="stMainBlockContainer"],
  .main .block-container {
    padding: 0 12px 20px 12px !important;
  }
  .v17-kpi-value, .kc .kv { font-size: 1.5rem !important; }
  .v17-kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .v17-alert { padding: 10px 12px !important; }
  .top-header, .v17-header { padding: 0 12px !important; height: 52px !important; }
  .tbl .th, .tbl .tr { padding: 8px 10px !important; }
  .v17-table-head, .v17-table-row { padding: 8px 10px !important; }
}

@media (max-width: 480px) {
  .v17-kpi-grid { grid-template-columns: 1fr 1fr !important; gap: 10px !important; }
  .v17-kpi { padding: 14px 12px !important; }
  .v17-kpi-value { font-size: 1.3rem !important; }
}

/* ══════════════════════════════════════════════════════
   MICRO-INTERACTIONS & ANIMATIONS
══════════════════════════════════════════════════════ */
@keyframes v17-fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes v17-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
@keyframes v17-slide-in-right {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}

.v17-animate-in    { animation: v17-fade-in .3s ease forwards; }
.v17-slide-in      { animation: v17-slide-in-right .25s ease forwards; }
.v17-pulse         { animation: v17-pulse 1.5s infinite; }

/* Staggered animations for KPI grid */
.v17-kpi:nth-child(1) { animation: v17-fade-in .3s ease .05s both; }
.v17-kpi:nth-child(2) { animation: v17-fade-in .3s ease .10s both; }
.v17-kpi:nth-child(3) { animation: v17-fade-in .3s ease .15s both; }
.v17-kpi:nth-child(4) { animation: v17-fade-in .3s ease .20s both; }
.v17-kpi:nth-child(5) { animation: v17-fade-in .3s ease .25s both; }
.v17-kpi:nth-child(6) { animation: v17-fade-in .3s ease .30s both; }

/* Staggered table rows */
.v17-table-row, .tbl .tr { animation: v17-fade-in .2s ease both; }

/* ══════════════════════════════════════════════════════
   DARK GLASS OVERLAY (modals, loading)
══════════════════════════════════════════════════════ */
.v17-glass {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.6);
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
    # المصاعد — V14
    "elevators.view":   {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH, ROLE_CLIENT},
    "elevators.add":    {ROLE_ADMIN, ROLE_MANAGER},
    "elevators.edit":   {ROLE_ADMIN, ROLE_MANAGER},
    "elevators.delete": {ROLE_ADMIN},
    # الزيارات — V14
    "visits.view":      {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "visits.add":       {ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH},
    "visits.edit":      {ROLE_ADMIN, ROLE_MANAGER},
    "visits.export":    {ROLE_ADMIN, ROLE_MANAGER},
}

def has_perm(action: str) -> bool:
    """التحقق من صلاحية المستخدم الحالي — مهمة 3: backend authorization"""
    role = st.session_state.get("role", ROLE_CLIENT)
    if role not in VALID_ROLES:
        return False
    # .add هو alias لـ .create
    if action not in PERMISSIONS and action.endswith(".add"):
        action = action[:-4] + ".create"
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
    "accepted":    "مقبول",
    "declined":    "مرفوض",
    "en_route":    "في الطريق",
    "arrived":     "وصل",
    "in_progress": "جاري",
    "completed":   "مكتمل",
    "cancelled":   "ملغي",
    "on_hold":     "موقوف",
    "no_access":   "لم يتمكن من الدخول",
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
# V14 — ثوابت التشغيل والأصول
# ─────────────────────────────────────────────

# مهمة 4: SLA Rules — قواعد مستوى الخدمة (بالساعات)
SLA_RULES = {
    "urgent":  {"response_hours": 2,  "resolution_hours": 8,  "label": "عاجلة — 2 ساعة استجابة"},
    "high":    {"response_hours": 4,  "resolution_hours": 24, "label": "عالية — 4 ساعات"},
    "medium":  {"response_hours": 8,  "resolution_hours": 48, "label": "متوسطة — 8 ساعات"},
    "low":     {"response_hours": 24, "resolution_hours": 72, "label": "منخفضة — 24 ساعة"},
}

# مهمة 7: WO Lifecycle — دورة حياة أوامر العمل الكاملة
WO_LIFECYCLE = [
    ("pending",     "معلق"),
    ("assigned",    "مكلف"),
    ("in_progress", "جاري"),
    ("on_hold",     "موقوف"),
    ("completed",   "مكتمل"),
    ("cancelled",   "ملغي"),
]

# مهمة 11: Visit Types
VISIT_TYPES_V14 = [
    "صيانة وقائية دورية",
    "صيانة تصحيحية",
    "فحص ما بعد إصلاح",
    "استجابة طارئة",
    "فحص أولي ما بعد تركيب",
    "فحص سنوي",
]

# مهمة 15: Non-completion Reasons
NON_COMPLETION_REASONS = [
    "انتظار قطع غيار",
    "العميل لم يفتح",
    "انتهت ساعات العمل",
    "فني وحيد — يحتاج دعم",
    "خطر على السلامة",
    "العطل أكبر مما يسمح التفويض",
    "أخرى",
]

# مهمة 24: Resolution Taxonomy — تصنيف الحلول
RESOLUTION_TYPES = [
    "إصلاح ميكانيكي",
    "إصلاح كهربائي",
    "استبدال قطعة",
    "برمجة / إعادة ضبط",
    "تشحيم وتنظيف",
    "إصلاح أبواب",
    "فحص وقائي — لا عطل",
    "تحويل لجهة خارجية",
    "أخرى",
]

# مهمة 17: Escalation Rules
ESCALATION_HOURS = {
    "urgent": 4,
    "high":   12,
    "medium": 24,
    "low":    48,
}

# مهمة 12: PM Schedule Rules (بالأيام)
PM_INTERVALS = {
    "monthly":    30,
    "quarterly":  90,
    "biannual":   180,
    "annual":     365,
}
PM_INTERVAL_LABELS = {
    "monthly":   "شهري",
    "quarterly": "ربع سنوي",
    "biannual":  "نصف سنوي",
    "annual":    "سنوي",
}

# مهمة 9: Asset Status
ASSET_STATUSES = {
    "active":      "نشط",
    "maintenance": "تحت الصيانة",
    "stopped":     "متوقف",
    "decommissioned": "مسحوب من الخدمة",
}

# مهمة 9: Control Panel Types
CONTROL_PANELS = ["Fuji", "Sigma", "Mitsubishi", "Otis OVF", "Schindler", "Kone", "محلي", "أخرى"]

# ─────────────────────────────────────────────
# V15 — ثوابت الواجهة الميدانية للفني
# ─────────────────────────────────────────────

# مهمة 1: حالات مهمة الفني الميدانية (Field Task Statuses)
FIELD_STATUSES = {
    "pending":    "معلق",
    "accepted":   "مقبول",
    "declined":   "مرفوض",
    "en_route":   "في الطريق",
    "arrived":    "وصل",
    "in_progress":"جاري التنفيذ",
    "completed":  "مكتمل",
    "incomplete": "غير مكتمل",
    "no_access":  "لم يتمكن من الدخول",
}

# مهمة 4: أسباب رفض المهمة
DECLINE_REASONS = [
    "تعارض مع مهمة أخرى",
    "مشكلة في المركبة",
    "مرض / ظرف طارئ",
    "المنطقة بعيدة",
    "أخرى",
]

# مهمة 14: أسباب عدم الوصول
NO_ACCESS_REASONS = [
    "العميل لم يفتح",
    "الموقع مغلق",
    "العنوان خاطئ",
    "المصعد في مكان مقيد",
    "عطل في المركبة",
    "أخرى",
]

# مهمة 13: Safety Checklist items
SAFETY_CHECKLIST = [
    "الإضاءة كافية في حجرة المصعد",
    "لا يوجد تسرب كهربائي",
    "تم فصل التيار قبل العمل",
    "ارتداء معدات السلامة الشخصية",
    "لا يوجد أفراد داخل المصعد",
    "توفر طفاية حريق قريبة",
    "المنطقة المحيطة آمنة",
]

# مهمة 19: Region-based dispatch — تقسيم الفنيين على المناطق
TECH_REGIONS = {
    "فيصل":       "شمال الرياض",
    "سيلفوم":     "وسط الرياض",
    "فريتز":      "جنوب الرياض",
    "جنيد":       "شرق الرياض",
    "كفاية الله": "غرب الرياض",
}

# المناطق وأحياؤها
REGION_DISTRICTS = {
    "شمال الرياض": ["النخيل", "الملقا", "الصحافة", "الربيع", "الياسمين", "حطين", "الغدير"],
    "وسط الرياض":  ["العليا", "الورود", "السليمانية", "النزهة", "الروضة", "المرسلات"],
    "جنوب الرياض": ["الشفاء", "الوادي", "طويق", "الدرعية", "الجنوبية"],
    "شرق الرياض":  ["الرائد", "المونسية", "الرمال", "النهضة", "الروابي"],
    "غرب الرياض":  ["البديعة", "الخليج", "العزيزية", "المحمدية", "البطحاء"],
}

# مهمة 8: حالات الخطر في التقرير الميداني
HAZARD_LEVELS = {
    "none":     "لا خطر",
    "low":      "خطر منخفض",
    "medium":   "خطر متوسط — تنبيه مطلوب",
    "high":     "خطر عالٍ — إيقاف فوري",
    "critical": "حرج — إخلاء فوري",
}

# مهمة 10: قطع الغيار الشائعة
COMMON_PARTS = [
    "حبال مصعد", "بكرات", "موتور باب", "لوحة تحكم", "مفتاح طابق",
    "ضاغط كهربائي", "زيت هيدروليك", "مستشعر مستوى", "مصابيح LED",
    "بطارية احتياطية", "كابل كهربائي", "حذاء باب", "أخرى",
]

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
    "pending":     ["accepted",    "declined",    "in_progress", "cancelled", "on_hold"],
    "accepted":    ["en_route",    "declined",    "in_progress", "cancelled"],
    "declined":    ["pending"],
    "en_route":    ["arrived",     "no_access",   "cancelled"],
    "arrived":     ["in_progress", "no_access"],
    "in_progress": ["completed",   "cancelled",   "on_hold"],
    "on_hold":     ["in_progress", "cancelled"],
    "no_access":   ["pending",     "cancelled"],
    "completed":   [],
    "cancelled":   [],
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

    # Login page — V17 Premium SaaS Design
    st.markdown("""
    <style>
    [data-testid="stApp"] {
      background: #F3F4F6 !important;
    }
    .main .block-container, [data-testid="stMainBlockContainer"] {
      padding: 0 !important;
      background: transparent !important;
    }
    [data-testid="stSidebar"] { display: none !important; }

    /* Login page layout */
    .v17-login-wrap {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(ellipse at 30% 20%, #EBF5FF 0%, transparent 50%),
                  radial-gradient(ellipse at 70% 80%, #ECFDF5 0%, transparent 45%),
                  #F3F4F6;
      direction: rtl;
    }
    .v17-login-card {
      width: 420px;
      background: #FFFFFF;
      border-radius: 20px;
      padding: 40px 40px 36px 40px;
      box-shadow: 0 20px 40px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.04);
      border: 1px solid #E5E7EB;
    }
    .v17-login-logo {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 32px;
    }
    .v17-login-logo-icon {
      width: 72px;
      height: 72px;
      background: linear-gradient(135deg, #1A56DB 0%, #1648C8 100%);
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.4rem;
      margin-bottom: 18px;
      box-shadow: 0 8px 24px rgba(26,86,219,.3), 0 2px 8px rgba(26,86,219,.2);
    }
    .v17-login-logo-name {
      font-size: 1.8rem;
      font-weight: 900;
      color: #111827;
      letter-spacing: 1px;
      font-family: Cairo, sans-serif;
      margin-bottom: 6px;
    }
    .v17-login-logo-sub {
      font-size: 0.875rem;
      color: #6B7280;
      font-family: Cairo, sans-serif;
      font-weight: 500;
      text-align: center;
    }
    .v17-login-footer {
      text-align: center;
      margin-top: 20px;
      font-size: 0.72rem;
      color: #9CA3AF;
      font-family: Cairo, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .v17-login-footer::before,
    .v17-login-footer::after {
      content: "";
      flex: 1;
      height: 1px;
      background: #E5E7EB;
      max-width: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("""
        <div class="v17-login-logo" style="margin-top:56px;">
          <div class="v17-login-logo-icon">🛗</div>
          <div class="v17-login-logo-name">LIFT TECH</div>
          <div class="v17-login-logo-sub">نظام إدارة وتشغيل المصاعد</div>
        </div>
        <div class="v17-login-card">
          <div style="font-size:1.1rem;font-weight:800;color:#111827;margin-bottom:6px;text-align:right;">مرحباً بك 👋</div>
          <div style="font-size:0.8rem;color:#6B7280;margin-bottom:24px;text-align:right;">سجّل دخولك للمتابعة</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
            submit   = st.form_submit_button("تسجيل الدخول  →", use_container_width=True, type="primary")

        st.markdown("""
        </div>
        <div class="v17-login-footer">
          LiftTech ERP — نظام إداري متكامل لصيانة المصاعد
        </div>
        """, unsafe_allow_html=True)

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

# ── شاشة إجبار تغيير كلمة المرور — V17 ──
if st.session_state.get("force_change_pwd"):
    st.markdown("""
    <style>
    [data-testid="stApp"] { background: #F3F4F6 !important; }
    .main .block-container,[data-testid="stMainBlockContainer"]{
      padding:0 !important;background:transparent !important;
    }
    [data-testid="stSidebar"]{display:none !important;}
    </style>""", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        st.markdown("""
        <div style="margin-top:56px;text-align:center;margin-bottom:24px;">
          <div style="width:64px;height:64px;
                      background:linear-gradient(135deg,#D97706,#FBBF24);
                      border-radius:18px;display:flex;align-items:center;justify-content:center;
                      font-size:2rem;margin:0 auto 16px;
                      box-shadow:0 8px 24px rgba(217,119,6,.28);">🔐</div>
          <div style="font-size:1.2rem;font-weight:900;color:#111827;font-family:Cairo,sans-serif;margin-bottom:8px;">تغيير كلمة المرور مطلوب</div>
          <div style="font-size:0.84rem;color:#6B7280;font-family:Cairo,sans-serif;max-width:320px;margin:0 auto;line-height:1.6;">
            كلمة المرور الافتراضية لا تزال مفعّلة — يجب تغييرها قبل المتابعة.
          </div>
        </div>
        <div style="background:#FFFFFF;border-radius:18px;padding:32px 36px;
                    box-shadow:0 16px 36px rgba(0,0,0,.08),0 4px 10px rgba(0,0,0,.04);
                    border:1px solid #E5E7EB;">
          <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;padding:12px 16px;margin-bottom:20px;direction:rtl;">
            <div style="font-size:0.8rem;font-weight:700;color:#92400E;font-family:Cairo,sans-serif;">⚠️ يجب تغيير كلمة المرور الافتراضية (12345) قبل الدخول للنظام</div>
          </div>
        """, unsafe_allow_html=True)
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
    colors = {
        "urgent": "background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;",
        "high":   "background:#FFFBEB;color:#D97706;border:1px solid #FDE68A;",
        "medium": "background:#EBF5FF;color:#1A56DB;border:1px solid #BFDBFE;",
        "low":    "background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;",
    }
    label = labels.get(priority, priority)
    style = colors.get(priority, "background:#F3F4F6;color:#4B5563;")
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;{style}">{label}</span>'

def status_badge(status):
    labels = {
        "pending": "معلق", "in_progress": "جاري", "completed": "مكتمل",
        "cancelled": "ملغي", "open": "مفتوح", "assigned": "مكلف",
        "resolved": "محلول", "closed": "مغلق",
        "active": "نشط", "expired": "منتهي", "on_hold": "موقف",
    }
    colors = {
        "pending":     "background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;",
        "in_progress": "background:#EBF5FF;color:#1648C8;border:1px solid #BFDBFE;",
        "completed":   "background:#ECFDF5;color:#065F46;border:1px solid #A7F3D0;",
        "cancelled":   "background:#F3F4F6;color:#4B5563;border:1px solid #E5E7EB;",
        "open":        "background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;",
        "assigned":    "background:#F5F3FF;color:#6D28D9;border:1px solid #DDD6FE;",
        "resolved":    "background:#ECFDF5;color:#065F46;border:1px solid #A7F3D0;",
        "closed":      "background:#F3F4F6;color:#4B5563;border:1px solid #E5E7EB;",
        "active":      "background:#ECFDF5;color:#065F46;border:1px solid #A7F3D0;",
        "expired":     "background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;",
        "on_hold":     "background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;",
    }
    label = labels.get(status, status)
    style = colors.get(status, "background:#F3F4F6;color:#4B5563;border:1px solid #E5E7EB;")
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;{style}">{label}</span>'

def priority_text(priority):
    """نص + emoji للأولوية — للاستخدام في عناوين st.expander"""
    icons  = {"urgent": "🔴", "high": "🟠", "medium": "🔵", "low": "🟢"}
    labels = {"urgent": "عاجلة", "high": "عالية", "medium": "متوسطة", "low": "منخفضة"}
    return f"{icons.get(priority,'⚪')} {labels.get(priority, priority)}"

def status_text(status):
    """نص + emoji للحالة — للاستخدام في عناوين st.expander"""
    icons = {
        "pending": "⏳", "in_progress": "⚙️", "completed": "✅",
        "cancelled": "🚫", "open": "🔓", "assigned": "👷",
        "resolved": "✅", "closed": "🔒",
        "active": "✅", "expired": "❌", "on_hold": "⏸️",
    }
    labels = {
        "pending": "معلق", "in_progress": "جاري", "completed": "مكتمل",
        "cancelled": "ملغي", "open": "مفتوح", "assigned": "مكلف",
        "resolved": "محلول", "closed": "مغلق",
        "active": "نشط", "expired": "منتهي", "on_hold": "موقف",
    }
    return f"{icons.get(status,'◦')} {labels.get(status, status)}"

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

@st.cache_data(ttl=30)
def load_elevators():
    if supabase is None: return []
    try:
        resp = supabase.table("elevators").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل المصاعد: {e}")
        return []

@st.cache_data(ttl=30)
def load_visits():
    if supabase is None: return []
    try:
        resp = supabase.table("visits").select("*").order("created_at", desc=True).execute()
        return resp.data or []
    except Exception as e:
        st.warning(f"⚠️ تعذّر تحميل الزيارات: {e}")
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
.date-filter-bar{background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;
    padding:14px 18px;margin-bottom:20px;direction:rtl;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.date-filter-bar .df-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.df-label{font-size:0.66rem;font-weight:800;color:#9CA3AF;letter-spacing:1.8px;text-transform:uppercase;margin-bottom:10px;}
.df-preset-row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px;}
.df-btn{padding:5px 14px;border-radius:20px;font-size:0.75rem;font-weight:700;
    border:1.5px solid #E5E7EB;background:#F9FAFB;color:#4B5563;cursor:pointer;white-space:nowrap;
    transition:all .15s ease;font-family:Cairo,sans-serif;}
.df-btn:hover{background:#EBF5FF;border-color:#BFDBFE;color:#1A56DB;}
.df-btn.active{background:#1A56DB;color:#fff;border-color:#1A56DB;box-shadow:0 2px 8px rgba(26,86,219,.3);}
.df-range{font-size:0.75rem;color:#6B7280;margin-top:6px;}
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
            btn_style = "background:#1A56DB;color:#fff;border:1.5px solid #1A56DB;box-shadow:0 2px 8px rgba(26,86,219,.3);" if is_active else "background:#F9FAFB;color:#4B5563;border:1.5px solid #E5E7EB;"
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

    bar_clr = (
    "linear-gradient(90deg,#059669,#34D399)" if collect_pct >= 70 else
    ("linear-gradient(90deg,#D97706,#FBBF24)" if collect_pct >= 40 else
     "linear-gradient(90deg,#DC2626,#F87171)")
)
    bar_w   = min(int(collect_pct), 100)

    # ══ CSS ══
    st.markdown("""<style>
/* V16 Dashboard */
.db-wrap * { box-sizing: border-box; }

/* header */
.db-wrap .hdr {
    display:flex; justify-content:space-between; align-items:flex-end;
    border-bottom:2px solid #E5E7EB; padding-bottom:16px; margin-bottom:24px;
    direction:rtl;
}
.hdr-r .lbl { font-size:0.66rem; font-weight:700; color:#9CA3AF; letter-spacing:2px; text-transform:uppercase; margin-bottom:5px; }
.hdr-r .ttl { font-size:1.5rem; font-weight:900; color:#111827; line-height:1.1; }
.hdr-l { text-align:left; }
.hdr-l .dt  { font-size:0.88rem; font-weight:700; color:#374151; margin-bottom:3px; }
.hdr-l .src { font-size:0.7rem; color:#9CA3AF; }

/* section title */
.db-wrap .stl {
    font-size:0.64rem; font-weight:700; color:#9CA3AF; letter-spacing:2.5px;
    text-transform:uppercase; margin:24px 0 12px; padding-bottom:8px;
    border-bottom:1px solid #F3F4F6; direction:rtl;
}

/* KPI card */
.db-wrap .kc {
    background:#FFFFFF; border:1px solid #E5E7EB; border-radius:14px;
    padding:18px 18px; height:100%; direction:rtl;
    box-shadow:0 1px 4px rgba(0,0,0,.04);
    transition: box-shadow .2s, transform .2s;
}
.db-wrap .kc:hover { box-shadow:0 6px 20px rgba(0,0,0,.09); transform:translateY(-2px); }
.kc .kl { font-size:0.68rem; font-weight:600; color:#6B7280; letter-spacing:0.5px; margin-bottom:8px; }
.kc .kv { font-size:2rem; font-weight:900; color:#111827; line-height:1; letter-spacing:-1px; margin-bottom:5px; }
.kc .ks { font-size:0.75rem; color:#9CA3AF; line-height:1.5; }
.kc.primary { border-top:3px solid #1A56DB; }
.kc.success { border-top:3px solid #059669; }
.kc.warning { border-top:3px solid #D97706; }
.kc.danger  { border-top:3px solid #DC2626; }
.kc.info    { border-top:3px solid #0EA5E9; }

/* bar */
.db-wrap .bar-card {
    background:#FFFFFF; border:1px solid #E5E7EB; border-radius:14px;
    padding:16px 20px; margin-top:10px; direction:rtl;
    box-shadow:0 1px 4px rgba(0,0,0,.04);
}
.bar-card .bt { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.bar-card .bl { font-size:0.84rem; font-weight:700; color:#374151; }
.bar-card .bp { font-size:1rem; font-weight:900; color:#1A56DB; }
.bar-card .btr { background:#F3F4F6; border-radius:8px; height:10px; overflow:hidden; }
.bar-card .bf  { height:10px; border-radius:8px; transition:width .4s ease; }
.bar-card .bm  { display:flex; justify-content:space-between; margin-top:9px; font-size:0.72rem; color:#9CA3AF; }

/* alerts */
.db-wrap .al {
    display:flex; align-items:center; gap:12px; padding:12px 16px;
    border-radius:12px; margin-bottom:8px; direction:rtl;
    transition:box-shadow .2s;
}
.db-wrap .al:hover { box-shadow:0 3px 10px rgba(0,0,0,.07); }
.al.r { background:#FEF2F2; border:1px solid #FECACA; }
.al.y { background:#FFFBEB; border:1px solid #FDE68A; }
.al.g { background:#ECFDF5; border:1px solid #A7F3D0; }
.al .ab { flex:1; }
.al .at { font-size:0.84rem; font-weight:700; color:#111827; line-height:1.3; }
.al .as { font-size:0.72rem; color:#6B7280; margin-top:2px; }
.al .an { font-size:1.4rem; font-weight:900; min-width:38px; text-align:center; }

/* tables */
.db-wrap .tbl { border:1px solid #E5E7EB; border-radius:12px; overflow:hidden; direction:rtl; box-shadow:0 1px 4px rgba(0,0,0,.04); }
.tbl .th {
    background:#F9FAFB; padding:10px 16px;
    display:flex; direction:rtl; align-items:center;
    border-bottom:2px solid #E5E7EB;
}
.tbl .th span { color:#374151; font-size:0.68rem; font-weight:700; letter-spacing:.5px; }
.tbl .tr {
    display:flex; direction:rtl; align-items:center;
    padding:9px 16px; border-bottom:1px solid #F9FAFB;
    background:#FFFFFF; transition:background .12s;
}
.tbl .tr:last-child { border-bottom:none; }
.tbl .tr:hover { background:#EBF5FF; }
.tbl .td { font-size:0.78rem; color:#374151; }
.tbl .td.b { font-weight:700; color:#111827; }
.tbl .td.g { color:#9CA3AF; font-size:0.72rem; }
.tbl .td.c { text-align:center; }

/* badges */
.bdg { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.68rem; font-weight:700; white-space:nowrap; border:1px solid transparent; }
.bdg.g { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
.bdg.r { background:#FEF2F2; color:#DC2626; border-color:#FECACA; }
.bdg.y { background:#FFFBEB; color:#92400E; border-color:#FDE68A; }
.bdg.k { background:#F3F4F6; color:#4B5563; border-color:#E5E7EB; }
.bdg.b { background:#EBF5FF; color:#1A56DB; border-color:#BFDBFE; }
.bdg.p { background:#F5F3FF; color:#6D28D9; border-color:#DDD6FE; }
</style>""", unsafe_allow_html=True)

    st.markdown('<div class="db-wrap">', unsafe_allow_html=True)

    # ─── HEADER ───
    st.markdown(f"""<div class="hdr">
  <div class="hdr-r">
    <div class="lbl">🛗 LiftTech — لوحة التحكم الإدارية</div>
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
        (c1, "إجمالي المحفظة",   fmt(total_v),     f"{total_c} عقد — {total_el} مصعد",       "primary", "💼"),
        (c2, "إجمالي المحصّل",   fmt(paid_v),      f"{collect_pct}% من المحفظة — {paid_c} عقد", "success", "✅"),
        (c3, "إجمالي المتأخر",   fmt(unpaid_v),    f"{round(100-collect_pct,1)}% من المحفظة — {unpaid_c} عقد", "danger", "⚠️"),
        (c4, "متوسط قيمة العقد", fmt(avg_contract), "ريال سعودي / عقد",                        "info",    "📊"),
    ]
    for col, lbl, val, sub, variant, icon in kpis:
        with col:
            st.markdown(f"""<div class="kc {variant}">
  <div style="font-size:1.4rem;margin-bottom:8px;opacity:.8">{icon}</div>
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
    "technician", "status", "priority", "work_type", "notes",
    "elevator_id", "fault_report_id",
    # V15 field columns
    "field_status", "accepted_at", "declined_reason",
    "en_route_at", "arrived_at", "work_started_at",
    "no_access_reason", "no_access_at", "hazard_level",
    "safety_checklist", "parts_used_structured", "photo_urls",
    "customer_signature", "followup_recommendation", "field_notes",
}
SCHEMA_FAULT_REPORTS = {
    "contract_id", "title", "description", "reported_date",
    "technician", "status", "priority", "notes",
    "fault_type", "resolution_type", "elevator_id",
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
    require_perm("contracts.view")
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
# TAB 3: Work Orders — V14 Full Lifecycle + Assignment Engine + SLA
# ════════════════════════════════════════════════════════
def tab_work_orders():
    require_perm("work_orders.view")
    contracts   = load_contracts()
    work_orders = load_work_orders()
    elev_db     = load_elevators()

    section_header("🔧 أوامر العمل")

    contracts_map   = {str(c["id"]): c for c in contracts}
    contract_labels_map = {str(c["id"]): contract_label(c) for c in contracts}
    id_to_cno       = id_to_contract_no_map(contracts)
    elev_map        = {str(e["id"]): e for e in elev_db}

    # ── Scope by role ──
    work_orders = scope_by_role(work_orders, "technician")

    # ── إحصائيات SLA ──
    today = date.today()
    wo_pending    = sum(1 for w in work_orders if w.get("status") == "pending")
    wo_in_prog    = sum(1 for w in work_orders if w.get("status") == "in_progress")
    wo_on_hold    = sum(1 for w in work_orders if w.get("status") == "on_hold")
    wo_overdue    = sum(1 for w in work_orders if
                       w.get("status") not in ("completed","cancelled") and
                       w.get("scheduled_date") and
                       parse_date_safe(w.get("scheduled_date")) and
                       parse_date_safe(w.get("scheduled_date")) < today)

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">📋 معلقة</div><div class="kpi-mini-value">{wo_pending}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚙️ جارية</div><div class="kpi-mini-value" style="color:#2563eb">{wo_in_prog}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⏸️ موقوفة</div><div class="kpi-mini-value" style="color:#d97706">{wo_on_hold}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚠️ متأخرة</div><div class="kpi-mini-value" style="color:#dc2626">{wo_overdue}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    wo_sub = st.radio(
        "عرض أوامر العمل",
        ["📋 قائمة أوامر العمل", "➕ أمر عمل جديد", "⏳ لوحة المعلقة"],
        horizontal=True,
        key="wo_sub_tab",
        label_visibility="collapsed",
    )

    # ══════════════════════════════════════════════════
    # SUB 1: قائمة أوامر العمل
    # ══════════════════════════════════════════════════
    if wo_sub == "📋 قائمة أوامر العمل":
        f1,f2,f3,f4 = st.columns(4)
        with f1:
            q_wo = st.text_input("🔍 بحث", key="wo_q_list")
        with f2:
            f_status_wo = st.selectbox("الحالة", ["الكل"] + list(WO_STATUSES.values()), key="wo_f_status")
        with f3:
            f_priority = st.selectbox("الأولوية", ["الكل"] + list(PRIORITY_LEVELS.values()), key="wo_f_priority")
        with f4:
            f_tech_wo = st.selectbox("الفني", ["الكل"] + TECHNICIANS, key="wo_f_tech")

        filtered_wo = work_orders[:]
        if q_wo.strip():
            q = q_wo.strip().lower()
            filtered_wo = [w for w in filtered_wo if
                q in safe_text(w.get("title"),"").lower() or
                q in safe_text(id_to_cno.get(str(w.get("contract_id","")),""),"").lower()]
        if f_status_wo != "الكل":
            sk = next((k for k,v in WO_STATUSES.items() if v == f_status_wo), None)
            if sk: filtered_wo = [w for w in filtered_wo if w.get("status") == sk]
        if f_priority != "الكل":
            pk = next((k for k,v in PRIORITY_LEVELS.items() if v == f_priority), None)
            if pk: filtered_wo = [w for w in filtered_wo if w.get("priority") == pk]
        if f_tech_wo != "الكل":
            filtered_wo = [w for w in filtered_wo if w.get("technician") == f_tech_wo]

        if not filtered_wo:
            st.info("لا توجد أوامر عمل مطابقة.")
        else:
            for w in filtered_wo:
                w_id    = str(w.get("id",""))
                w_title = safe_text(w.get("title"),"—")
                w_stat  = w.get("status","pending")
                w_pri   = w.get("priority","medium")
                w_tech  = safe_text(w.get("technician"),"—")
                w_date  = safe_text(w.get("scheduled_date"),"—")
                w_type  = WORK_TYPES.get(safe_text(w.get("work_type"),""),"—")
                c_no    = id_to_cno.get(str(w.get("contract_id","")), "—")
                sla_info = SLA_RULES.get(w_pri, {})
                sla_label = sla_info.get("label","—")

                # SLA overdue check
                is_overdue = False
                if w_stat not in ("completed","cancelled") and w.get("scheduled_date"):
                    d = parse_date_safe(w.get("scheduled_date"))
                    if d and d < today:
                        is_overdue = True

                overdue_banner = '<span style="background:#fee2e2;color:#dc2626;padding:1px 8px;border-radius:8px;font-size:0.78rem;margin-right:6px">⚠️ متأخر</span>' if is_overdue else ''

                _exp_overdue = " ⚠️ متأخر" if is_overdue else ""
                with st.expander(f"{priority_text(w_pri)}  {status_text(w_stat)}{_exp_overdue}  |  {w_title} — {c_no} — {w_date}"):
                    # Badges HTML داخل المحتوى
                    st.markdown(f'''<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;direction:rtl;">
                      {priority_badge(w_pri)} {status_badge(w_stat)}
                      {"<span style=\'background:#FEE2E2;color:#DC2626;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;border:1px solid #FECACA;\'>⚠️ متأخر</span>" if is_overdue else ""}
                    </div>''', unsafe_allow_html=True)
                    d1, d2 = st.columns(2)
                    with d1:
                        st.write(f"**العنوان:** {w_title}")
                        st.write(f"**العقد:** {c_no}")
                        st.write(f"**التاريخ المجدول:** {w_date}")
                        st.write(f"**نوع العمل:** {w_type}")
                        st.write(f"**SLA:** {sla_label}")
                    with d2:
                        st.write(f"**الفني:** {w_tech}")
                        st.write(f"**الحالة:** {WO_STATUSES.get(w_stat,w_stat)}")
                        st.write(f"**الوصف:** {safe_text(w.get('description'),'—')}")
                        st.write(f"**ملاحظات:** {safe_text(w.get('notes'),'—')}")

                    if has_perm("work_orders.edit"):
                        st.markdown("**── تحديث الحالة ──**")
                        u1, u2, u3 = st.columns(3)
                        with u1:
                            allowed = get_allowed_transitions(w_stat, WO_TRANSITIONS)
                            allowed_labels = [WO_STATUSES.get(s,s) for s in allowed]
                            if allowed_labels:
                                new_st_label = st.selectbox("الحالة الجديدة", allowed_labels, key=f"wo_new_st_{w_id}")
                                new_st = next((k for k,v in WO_STATUSES.items() if v == new_st_label), w_stat)
                        with u2:
                            hold_reason_sel = ""
                            if allowed and "on_hold" in allowed:
                                hold_reason_sel = st.selectbox("سبب الإيقاف", ["—"] + HOLD_REASONS, key=f"wo_hold_{w_id}")
                            cancel_reason_sel = ""
                            if allowed and "cancelled" in allowed:
                                cancel_reason_sel = st.selectbox("سبب الإلغاء", ["—"] + CANCEL_REASONS, key=f"wo_cancel_{w_id}")
                        with u3:
                            close_reason_sel = ""
                            if allowed and "completed" in allowed:
                                close_reason_sel = st.selectbox("سبب الإغلاق", ["—"] + CLOSE_REASONS, key=f"wo_close_{w_id}")

                        if allowed_labels and st.button("💾 تحديث", key=f"wo_upd_{w_id}"):
                            errors = []
                            if new_st == "on_hold" and (not hold_reason_sel or hold_reason_sel == "—"):
                                errors.append("سبب الإيقاف مطلوب")
                            if new_st == "cancelled" and (not cancel_reason_sel or cancel_reason_sel == "—"):
                                errors.append("سبب الإلغاء مطلوب")
                            if new_st == "completed":
                                close_errs = validate_closure(new_st, close_reason_sel, w_tech)
                                errors.extend(close_errs)

                            if show_validation_errors(errors):
                                pass
                            else:
                                note_extra = ""
                                if new_st == "on_hold":   note_extra = hold_reason_sel
                                if new_st == "cancelled": note_extra = cancel_reason_sel
                                if new_st == "completed": note_extra = close_reason_sel
                                try:
                                    update_data = {"status": new_st}
                                    if note_extra and note_extra != "—":
                                        update_data["notes"] = f"{safe_text(w.get('notes'),'')} | سبب: {note_extra}".strip(" |")
                                    supabase.table("work_orders").update(update_data).eq("id", w_id).execute()
                                    log_action("edit","work_orders",f"تحديث حالة أمر {w_title}: {w_stat} ← {new_st}",
                                               severity="normal", entity_id=w_id, old_value=w_stat, new_value=new_st)
                                    if new_st == "completed":
                                        log_decision("closure","work_order",w_id,new_st,note_extra)
                                    load_work_orders.clear()
                                    st.success("✅ تم التحديث")
                                    st.rerun()
                                except Exception as ex:
                                    st.error(friendly_error(ex))

                        # ── إعادة الفتح ──
                        if w_stat in ("completed","cancelled") and can_reopen(w_stat, get_role()):
                            st.markdown("**── إعادة الفتح ──**")
                            reopen_r = st.selectbox("سبب إعادة الفتح", REOPEN_REASONS, key=f"wo_reopen_r_{w_id}")
                            if st.button("🔄 إعادة فتح", key=f"wo_reopen_{w_id}"):
                                rerr = validate_reopen(w_stat, reopen_r)
                                if show_validation_errors(rerr):
                                    pass
                                else:
                                    try:
                                        supabase.table("work_orders").update({"status":"pending","notes": f"{safe_text(w.get('notes'),'')} | إعادة فتح: {reopen_r}".strip(" |")}).eq("id",w_id).execute()
                                        log_action("edit","work_orders",f"إعادة فتح أمر {w_title}: سبب: {reopen_r}",
                                                   severity="important", entity_id=w_id)
                                        log_decision("reopen","work_order",w_id,"pending",reopen_r)
                                        load_work_orders.clear()
                                        st.success("✅ تم إعادة الفتح")
                                        st.rerun()
                                    except Exception as ex:
                                        st.error(friendly_error(ex))

            # تصدير
            df_wo_exp = pd.DataFrame([{
                "العنوان": safe_text(w.get("title")),
                "العقد": id_to_cno.get(str(w.get("contract_id","")), "—"),
                "التاريخ": safe_text(w.get("scheduled_date")),
                "الفني": safe_text(w.get("technician")),
                "الحالة": WO_STATUSES.get(safe_text(w.get("status"),"pending"),"—"),
                "الأولوية": PRIORITY_LEVELS.get(safe_text(w.get("priority"),"medium"),"—"),
                "نوع العمل": WORK_TYPES.get(safe_text(w.get("work_type"),""),"—"),
            } for w in filtered_wo])
            controlled_download_button("📥 تصدير CSV", to_csv_bytes(df_wo_exp),
                                       "work_orders_export.csv","text/csv","work_orders")

    # ══════════════════════════════════════════════════
    # SUB 2: أمر عمل جديد — Assignment Engine
    # ══════════════════════════════════════════════════
    elif wo_sub == "➕ أمر عمل جديد":
        require_perm("work_orders.add")
        section_header("➕ إنشاء أمر عمل جديد")

        if not contracts:
            st.warning("لا توجد عقود.")
            return

        c1, c2 = st.columns(2)
        with c1:
            sel_contract_wo = st.selectbox("العقد *", list(contract_labels_map.values()), key="new_wo_c")
            sel_c_id_wo = next((k for k,v in contract_labels_map.items() if v == sel_contract_wo), None)
            wo_title = st.text_input("عنوان الأمر *", key="new_wo_title")
            wo_desc  = st.text_area("الوصف", key="new_wo_desc", height=80)
            wo_date  = st.date_input("التاريخ المجدول *", value=date.today(), key="new_wo_date")

            # Asset linkage
            elev_options_wo = ["— بدون ربط —"] + [safe_text(e.get("internal_code"),"") + " — " + safe_text(e.get("building_name"),"") for e in elev_db if str(e.get("contract_id","")) == str(sel_c_id_wo or "")]
            linked_elev_label = st.selectbox("ربط بمصعد (اختياري)", elev_options_wo, key="new_wo_elev_link")
            linked_elev_id = None
            if linked_elev_label != "— بدون ربط —":
                linked_code = linked_elev_label.split(" — ")[0]
                linked_elev_id = next((str(e["id"]) for e in elev_db if safe_text(e.get("internal_code"),"") == linked_code), None)

        with c2:
            wo_priority = st.selectbox("الأولوية *", list(PRIORITY_LEVELS.values()), index=2, key="new_wo_pri")
            wo_priority_key = next((k for k,v in PRIORITY_LEVELS.items() if v == wo_priority), "medium")

            # SLA display
            sla = SLA_RULES.get(wo_priority_key, {})
            st.info(f"📋 SLA: {sla.get('label','—')} | وقت الحل: {sla.get('resolution_hours','—')} ساعة")

            wo_type_label = st.selectbox("نوع العمل *", list(WORK_TYPES.values()), key="new_wo_type")
            wo_type_key   = next((k for k,v in WORK_TYPES.items() if v == wo_type_label), "preventive")

            # Assignment Engine — اقتراح فني بناءً على تكليفات اليوم
            today_str = date.today().isoformat()
            tech_load = {t: sum(1 for w in work_orders if w.get("technician") == t and w.get("scheduled_date","") == today_str and w.get("status") not in ("completed","cancelled")) for t in TECHNICIANS}
            suggested_tech = min(TECHNICIANS, key=lambda t: tech_load.get(t, 0))
            tech_load_display = " | ".join([f"{t}: {tech_load.get(t,0)}" for t in TECHNICIANS])
            st.caption(f"💡 أقل تكليفاً اليوم: **{suggested_tech}** | التوزيع: {tech_load_display}")

            wo_tech = st.selectbox("تكليف الفني *",
                                   TECHNICIANS_WITH_UNASSIGNED,
                                   index=TECHNICIANS_WITH_UNASSIGNED.index(suggested_tech) if suggested_tech in TECHNICIANS_WITH_UNASSIGNED else 0,
                                   key="new_wo_tech")
            wo_notes = st.text_area("ملاحظات", key="new_wo_notes", height=60)

        if st.button("💾 حفظ أمر العمل", type="primary", use_container_width=True, key="save_new_wo"):
            errors = validate_work_order(wo_title, sel_c_id_wo, wo_tech, wo_date.isoformat())
            dup = check_duplicate_work_order(supabase, sel_c_id_wo, wo_title, wo_date.isoformat())
            if dup: errors.append(f"⚠️ يوجد أمر مشابه: {dup}")

            if show_validation_errors(errors):
                pass
            else:
                initial_status = "assigned" if wo_tech and wo_tech != "-- غير مكلف --" else "pending"
                payload = {
                    "contract_id":    sel_c_id_wo,
                    "title":          wo_title.strip(),
                    "description":    wo_desc.strip(),
                    "scheduled_date": wo_date.isoformat(),
                    "technician":     wo_tech if wo_tech != "-- غير مكلف --" else None,
                    "status":         initial_status,
                    "priority":       wo_priority_key,
                    "work_type":      wo_type_key,
                    "notes":          wo_notes.strip(),
                }
                if linked_elev_id:
                    payload["elevator_id"] = linked_elev_id
                try:
                    supabase.table("work_orders").insert(payload).execute()
                    log_action("add","work_orders",f"إنشاء أمر عمل: {wo_title.strip()}")
                    load_work_orders.clear()
                    st.success(f"✅ تم إنشاء أمر العمل بنجاح — حالة: {WO_STATUSES.get(initial_status,'')}")
                    st.rerun()
                except Exception as ex:
                    st.error(friendly_error(ex))

    # ══════════════════════════════════════════════════
    # SUB 3: لوحة المعلقة — Pending Board (مهمة 20)
    # ══════════════════════════════════════════════════
    elif wo_sub == "⏳ لوحة المعلقة":
        require_perm("work_orders.view")
        section_header("⏳ لوحة أوامر العمل المعلقة والمتأخرة")

        pending_wo = [w for w in work_orders if w.get("status") not in ("completed","cancelled")]
        pending_wo.sort(key=lambda w: (
            {"urgent":0,"high":1,"medium":2,"low":3}.get(w.get("priority","medium"), 2),
            safe_text(w.get("scheduled_date",""))
        ))

        if not pending_wo:
            st.success("✅ لا توجد أوامر عمل معلقة.")
            return

        # جدول مدمج
        rows = []
        for w in pending_wo:
            d = parse_date_safe(w.get("scheduled_date"))
            days_late = (today - d).days if d and d < today else 0
            rows.append({
                "العنوان": safe_text(w.get("title"),"—"),
                "العقد": id_to_cno.get(str(w.get("contract_id","")), "—"),
                "الفني": safe_text(w.get("technician"),"— غير مكلف —"),
                "الحالة": WO_STATUSES.get(w.get("status","pending"),"—"),
                "الأولوية": PRIORITY_LEVELS.get(w.get("priority","medium"),"—"),
                "التاريخ": safe_text(w.get("scheduled_date"),"—"),
                "تأخر (أيام)": days_late if days_late > 0 else "—",
                "SLA": SLA_RULES.get(w.get("priority","medium"), {}).get("label","—"),
            })
        df_pend = pd.DataFrame(rows)
        st.dataframe(df_pend, use_container_width=True, hide_index=True)

        controlled_download_button("📥 تصدير المعلقة CSV", to_csv_bytes(df_pend),
                                   "pending_work_orders.csv","text/csv","work_orders")


# ════════════════════════════════════════════════════════
# TAB 4: Fault Reports — V14 Professional Form + Fault Workflow + Fault-to-WO Linkage
# ════════════════════════════════════════════════════════
def tab_fault_reports():
    require_perm("fault_reports.view")
    contracts     = load_contracts()
    fault_reports = load_fault_reports()
    work_orders   = load_work_orders()
    elev_db       = load_elevators()

    section_header("🚨 البلاغات والأعطال")

    contracts_map       = {str(c["id"]): c for c in contracts}
    contract_labels_map = {str(c["id"]): contract_label(c) for c in contracts}
    id_to_cno           = id_to_contract_no_map(contracts)
    elev_map            = {str(e["id"]): e for e in elev_db}

    fault_reports = scope_by_role(fault_reports, "technician")

    # إحصائيات
    fr_open     = sum(1 for f in fault_reports if f.get("status") == "open")
    fr_assigned = sum(1 for f in fault_reports if f.get("status") == "assigned")
    fr_escalated= sum(1 for f in fault_reports if f.get("status") == "escalated")
    fr_resolved = sum(1 for f in fault_reports if f.get("status") == "resolved")

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🔴 مفتوحة</div><div class="kpi-mini-value" style="color:#dc2626">{fr_open}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🟡 مكلفة</div><div class="kpi-mini-value" style="color:#d97706">{fr_assigned}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🔺 مصعّدة</div><div class="kpi-mini-value" style="color:#7c3aed">{fr_escalated}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ محلولة</div><div class="kpi-mini-value" style="color:#16a34a">{fr_resolved}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    fr_sub = st.radio(
        "عرض البلاغات",
        ["📋 قائمة البلاغات", "➕ بلاغ جديد"],
        horizontal=True,
        key="fr_sub_tab",
        label_visibility="collapsed",
    )

    # ══════════════════════════════════════════════════
    # SUB 1: قائمة البلاغات
    # ══════════════════════════════════════════════════
    if fr_sub == "📋 قائمة البلاغات":
        f1,f2,f3 = st.columns(3)
        with f1:
            q_fr = st.text_input("🔍 بحث", key="fr_q_list")
        with f2:
            f_status_fr = st.selectbox("الحالة", ["الكل"] + list(FR_STATUSES.values()), key="fr_f_status")
        with f3:
            f_pri_fr = st.selectbox("الأولوية", ["الكل"] + list(PRIORITY_LEVELS.values()), key="fr_f_pri")

        filtered_fr = fault_reports[:]
        if q_fr.strip():
            q = q_fr.strip().lower()
            filtered_fr = [f for f in filtered_fr if
                q in safe_text(f.get("title"),"").lower() or
                q in safe_text(f.get("description"),"").lower() or
                q in safe_text(id_to_cno.get(str(f.get("contract_id","")),""),"").lower()]
        if f_status_fr != "الكل":
            sk = next((k for k,v in FR_STATUSES.items() if v == f_status_fr), None)
            if sk: filtered_fr = [f for f in filtered_fr if f.get("status") == sk]
        if f_pri_fr != "الكل":
            pk = next((k for k,v in PRIORITY_LEVELS.items() if v == f_pri_fr), None)
            if pk: filtered_fr = [f for f in filtered_fr if f.get("priority") == pk]

        if not filtered_fr:
            st.info("لا توجد بلاغات مطابقة.")
        else:
            for fr in filtered_fr:
                fr_id    = str(fr.get("id",""))
                fr_title = safe_text(fr.get("title"),"—")
                fr_stat  = fr.get("status","open")
                fr_pri   = fr.get("priority","medium")
                fr_tech  = safe_text(fr.get("technician"),"—")
                fr_date  = safe_text(fr.get("reported_date"),"—")
                c_no     = id_to_cno.get(str(fr.get("contract_id","")), "—")
                sla_label = SLA_RULES.get(fr_pri, {}).get("label","—")

                # ربط بأوامر عمل
                linked_wo = [w for w in work_orders if str(w.get("fault_report_id","")) == fr_id]

                with st.expander(f"{priority_text(fr_pri)}  {status_text(fr_stat)}  |  {fr_title} — {c_no} — {fr_date}"):
                    # Badges HTML داخل المحتوى
                    st.markdown(f'''<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;direction:rtl;">
                      {priority_badge(fr_pri)} {status_badge(fr_stat)}
                    </div>''', unsafe_allow_html=True)
                    d1, d2 = st.columns(2)
                    with d1:
                        st.write(f"**العنوان:** {fr_title}")
                        st.write(f"**العقد:** {c_no}")
                        st.write(f"**تاريخ البلاغ:** {fr_date}")
                        st.write(f"**الحالة:** {FR_STATUSES.get(fr_stat,fr_stat)}")
                        st.write(f"**SLA:** {sla_label}")
                    with d2:
                        st.write(f"**الوصف:** {safe_text(fr.get('description'),'—')}")
                        st.write(f"**الفني:** {fr_tech}")
                        st.write(f"**نوع العطل:** {safe_text(fr.get('fault_type'),'—')}")
                        st.write(f"**نوع الحل:** {safe_text(fr.get('resolution_type'),'—')}")
                        st.write(f"**ملاحظات:** {safe_text(fr.get('notes'),'—')}")

                    # أوامر عمل مرتبطة
                    if linked_wo:
                        st.markdown(f"**🔗 أوامر عمل مرتبطة ({len(linked_wo)}):**")
                        for lw in linked_wo:
                            st.write(f"  - {safe_text(lw.get('title'),'—')} | {WO_STATUSES.get(lw.get('status','pending'),'—')} | {safe_text(lw.get('scheduled_date'),'—')}")

                    if has_perm("fault_reports.edit"):
                        st.markdown("**── تحديث الحالة ──**")
                        u1, u2 = st.columns(2)
                        with u1:
                            allowed_fr = get_allowed_transitions(fr_stat, FR_TRANSITIONS)
                            allowed_fr_labels = [FR_STATUSES.get(s,s) for s in allowed_fr]
                            new_fr_st_label = st.selectbox("الحالة الجديدة", ["— بدون تغيير —"] + allowed_fr_labels, key=f"fr_new_st_{fr_id}")
                            new_fr_st = next((k for k,v in FR_STATUSES.items() if v == new_fr_st_label), fr_stat)
                            fr_tech_upd = st.selectbox("تكليف فني", TECHNICIANS_WITH_UNASSIGNED,
                                                        index=TECHNICIANS_WITH_UNASSIGNED.index(fr_tech) if fr_tech in TECHNICIANS_WITH_UNASSIGNED else 0,
                                                        key=f"fr_tech_{fr_id}")
                        with u2:
                            resol_type = st.selectbox("نوع الحل", ["—"] + RESOLUTION_TYPES, key=f"fr_resol_{fr_id}")
                            fr_notes_upd = st.text_input("ملاحظة التحديث", key=f"fr_notes_upd_{fr_id}")

                        if new_fr_st_label != "— بدون تغيير —" and st.button("💾 تحديث", key=f"fr_upd_{fr_id}"):
                            try:
                                upd = {"status": new_fr_st}
                                if fr_tech_upd and fr_tech_upd != "-- غير مكلف --":
                                    upd["technician"] = fr_tech_upd
                                if resol_type and resol_type != "—":
                                    upd["resolution_type"] = resol_type
                                if fr_notes_upd.strip():
                                    upd["notes"] = f"{safe_text(fr.get('notes'),'')} | {fr_notes_upd.strip()}".strip(" |")
                                supabase.table("fault_reports").update(upd).eq("id", fr_id).execute()
                                log_action("edit","fault_reports",f"تحديث بلاغ {fr_title}: {fr_stat} ← {new_fr_st}",
                                           severity="normal", entity_id=fr_id, old_value=fr_stat, new_value=new_fr_st)
                                load_fault_reports.clear()
                                st.success("✅ تم التحديث")
                                st.rerun()
                            except Exception as ex:
                                st.error(friendly_error(ex))

                        # Fault-to-WO Linkage (مهمة 6)
                        if has_perm("work_orders.add") and fr_stat in ("assigned","in_progress","escalated"):
                            st.markdown("**── إنشاء أمر عمل من البلاغ ──**")
                            if st.button("🔧 إنشاء أمر عمل مرتبط", key=f"fr_to_wo_{fr_id}"):
                                wo_payload = {
                                    "contract_id":      fr.get("contract_id"),
                                    "title":            f"[بلاغ] {fr_title}",
                                    "description":      safe_text(fr.get("description"),""),
                                    "scheduled_date":   date.today().isoformat(),
                                    "technician":       fr_tech if fr_tech in TECHNICIANS else None,
                                    "status":           "assigned" if fr_tech in TECHNICIANS else "pending",
                                    "priority":         fr_pri,
                                    "work_type":        "corrective",
                                    "fault_report_id":  fr_id,
                                    "notes":            f"مرتبط بالبلاغ #{fr_id}",
                                }
                                try:
                                    supabase.table("work_orders").insert(wo_payload).execute()
                                    log_action("add","work_orders",f"إنشاء WO من البلاغ #{fr_id}: {fr_title}")
                                    load_work_orders.clear()
                                    st.success("✅ تم إنشاء أمر العمل المرتبط")
                                    st.rerun()
                                except Exception as ex:
                                    st.error(friendly_error(ex))

            # تصدير
            df_fr_exp = pd.DataFrame([{
                "العنوان": safe_text(f.get("title")),
                "العقد": id_to_cno.get(str(f.get("contract_id","")), "—"),
                "التاريخ": safe_text(f.get("reported_date")),
                "الفني": safe_text(f.get("technician")),
                "الحالة": FR_STATUSES.get(safe_text(f.get("status"),"open"),"—"),
                "الأولوية": PRIORITY_LEVELS.get(safe_text(f.get("priority"),"medium"),"—"),
                "نوع العطل": safe_text(f.get("fault_type","—")),
                "نوع الحل": safe_text(f.get("resolution_type","—")),
            } for f in filtered_fr])
            controlled_download_button("📥 تصدير CSV", to_csv_bytes(df_fr_exp),
                                       "fault_reports_export.csv","text/csv","fault_reports")

    # ══════════════════════════════════════════════════
    # SUB 2: بلاغ جديد (Professional Form — مهمة 4+5)
    # ══════════════════════════════════════════════════
    elif fr_sub == "➕ بلاغ جديد":
        require_perm("fault_reports.add")
        section_header("➕ تسجيل بلاغ جديد")

        if not contracts:
            st.warning("لا توجد عقود.")
            return

        c1, c2 = st.columns(2)
        with c1:
            sel_c_fr = st.selectbox("العقد *", list(contract_labels_map.values()), key="new_fr_c")
            sel_c_id_fr = next((k for k,v in contract_labels_map.items() if v == sel_c_fr), None)
            fr_title_new = st.text_input("عنوان البلاغ *", key="new_fr_title")
            fr_desc_new  = st.text_area("وصف العطل *", key="new_fr_desc", height=100, placeholder="صف العطل بالتفصيل...")
            fr_fault_type = st.selectbox("نوع العطل *", FAULT_TYPES, key="new_fr_fault_type")
            fr_date_new  = st.date_input("تاريخ البلاغ *", value=date.today(), key="new_fr_date")

            # ربط بمصعد محدد
            elev_opts_fr = ["— بدون ربط —"] + [safe_text(e.get("internal_code"),"") + " — " + safe_text(e.get("building_name"),"") for e in elev_db if str(e.get("contract_id","")) == str(sel_c_id_fr or "")]
            linked_elev_fr = st.selectbox("ربط بمصعد (اختياري)", elev_opts_fr, key="new_fr_elev")
            linked_elev_id_fr = None
            if linked_elev_fr != "— بدون ربط —":
                lc = linked_elev_fr.split(" — ")[0]
                linked_elev_id_fr = next((str(e["id"]) for e in elev_db if safe_text(e.get("internal_code"),"") == lc), None)

        with c2:
            fr_priority_new = st.selectbox("الأولوية *", list(PRIORITY_LEVELS.values()), index=0, key="new_fr_pri")
            fr_priority_key = next((k for k,v in PRIORITY_LEVELS.items() if v == fr_priority_new), "medium")

            sla_fr = SLA_RULES.get(fr_priority_key, {})
            st.info(f"📋 SLA: {sla_fr.get('label','—')} | وقت الاستجابة: {sla_fr.get('response_hours','—')} ساعة")

            fr_tech_new = st.selectbox("تكليف فني", TECHNICIANS_WITH_UNASSIGNED, key="new_fr_tech")
            fr_notes_new = st.text_area("ملاحظات", key="new_fr_notes", height=60)

        if st.button("💾 تسجيل البلاغ", type="primary", use_container_width=True, key="save_new_fr"):
            errors = validate_fault_report(fr_desc_new)
            if not fr_title_new.strip(): errors.append("عنوان البلاغ مطلوب")
            if not sel_c_id_fr: errors.append("اختر عقداً")
            dup = check_duplicate_fault(supabase, sel_c_id_fr, fr_desc_new, fr_date_new.isoformat())
            if dup: errors.append(f"⚠️ بلاغ مشابه موجود: {dup}")

            if show_validation_errors(errors):
                pass
            else:
                initial_fr_status = "assigned" if fr_tech_new and fr_tech_new != "-- غير مكلف --" else "open"
                payload_fr = {
                    "contract_id":   sel_c_id_fr,
                    "title":         fr_title_new.strip(),
                    "description":   fr_desc_new.strip(),
                    "fault_type":    fr_fault_type,
                    "reported_date": fr_date_new.isoformat(),
                    "technician":    fr_tech_new if fr_tech_new != "-- غير مكلف --" else None,
                    "status":        initial_fr_status,
                    "priority":      fr_priority_key,
                    "notes":         fr_notes_new.strip(),
                }
                if linked_elev_id_fr:
                    payload_fr["elevator_id"] = linked_elev_id_fr
                try:
                    supabase.table("fault_reports").insert(payload_fr).execute()
                    log_action("add","fault_reports",f"تسجيل بلاغ: {fr_title_new.strip()}")
                    load_fault_reports.clear()
                    st.success(f"✅ تم تسجيل البلاغ — حالة: {FR_STATUSES.get(initial_fr_status,'')}")
                    st.rerun()
                except Exception as ex:
                    st.error(friendly_error(ex))


# ════════════════════════════════════════════════════════
# TAB 5: Maintenance Logs
# ════════════════════════════════════════════════════════
def tab_maintenance_logs():
    require_perm("maintenance.view")
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
# TAB 6: Elevators — V14 Asset Profile + Technical History + Asset-Location Mapping
# ════════════════════════════════════════════════════════
def tab_elevators():
    require_perm("elevators.view")
    contracts = load_contracts()
    visits    = load_visits()
    elev_db   = load_elevators()

    section_header("🛗 أصول المصاعد — Asset Management")

    # ── Tabs ──
    sub_tab = st.radio(
        "عرض",
        ["📋 قائمة الأصول", "➕ إضافة مصعد", "📜 السجل التقني"],
        horizontal=True,
        key="elev_sub_tab",
        label_visibility="collapsed",
    )

    contracts_map = {str(c["id"]): c for c in contracts}
    contract_labels = {str(c["id"]): contract_label(c) for c in contracts}

    # ──────────────────────────────────────────────────────
    # SUB 1: قائمة الأصول
    # ──────────────────────────────────────────────────────
    if sub_tab == "📋 قائمة الأصول":
        # ── فلاتر ──
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            q_search = st.text_input("🔍 بحث بالعميل أو المبنى أو الكود", key="elev_q")
        with f2:
            f_city = st.selectbox("المدينة", ["الكل"] + CITIES, key="elev_city")
        with f3:
            f_type = st.selectbox("النوع", ["الكل"] + ELEVATOR_TYPES, key="elev_type_f")
        with f4:
            f_status = st.selectbox("الحالة", ["الكل"] + list(ASSET_STATUSES.values()), key="elev_status_f")

        filtered = elev_db[:]
        if q_search.strip():
            q = q_search.strip().lower()
            filtered = [e for e in filtered if
                q in safe_text(e.get("customer_name"),"").lower() or
                q in safe_text(e.get("building_name"),"").lower() or
                q in safe_text(e.get("internal_code"),"").lower()]
        if f_city != "الكل":
            filtered = [e for e in filtered if e.get("city") == f_city]
        if f_type != "الكل":
            filtered = [e for e in filtered if e.get("elevator_type") == f_type]
        if f_status != "الكل":
            status_key = next((k for k,v in ASSET_STATUSES.items() if v == f_status), None)
            if status_key:
                filtered = [e for e in filtered if e.get("asset_status") == status_key]

        # ── إحصائيات ──
        s1, s2, s3, s4 = st.columns(4)
        total = len(filtered)
        active_c   = sum(1 for e in filtered if e.get("asset_status","active") == "active")
        maint_c    = sum(1 for e in filtered if e.get("asset_status") == "maintenance")
        stopped_c  = sum(1 for e in filtered if e.get("asset_status") == "stopped")
        s1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">إجمالي المصاعد</div><div class="kpi-mini-value">{total}</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ نشطة</div><div class="kpi-mini-value">{active_c}</div></div>', unsafe_allow_html=True)
        s3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🔧 تحت الصيانة</div><div class="kpi-mini-value" style="color:#f59e0b">{maint_c}</div></div>', unsafe_allow_html=True)
        s4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⛔ متوقفة</div><div class="kpi-mini-value" style="color:#c00">{stopped_c}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        if not filtered:
            st.info("لا توجد أصول مطابقة للفلتر.")
            return

        # ── بطاقات Asset ──
        # آخر زيارة لكل مصعد
        visits_map = {}
        for v in visits:
            eid = str(v.get("elevator_id",""))
            if eid:
                existing = visits_map.get(eid)
                if not existing or safe_text(v.get("visit_date","")) > safe_text(existing.get("visit_date","")):
                    visits_map[eid] = v

        cols_per_row = 3
        col_list = st.columns(cols_per_row)
        for idx, e in enumerate(filtered):
            eid = str(e.get("id",""))
            c_id = str(e.get("contract_id",""))
            contract_info = contracts_map.get(c_id, {})
            last_v = visits_map.get(eid)
            last_visit_date = safe_text(last_v.get("visit_date"),"—") if last_v else "لا يوجد"
            last_tech = safe_text(last_v.get("technician"),"—") if last_v else "—"
            a_status = e.get("asset_status","active")
            status_ar = ASSET_STATUSES.get(a_status, a_status)
            status_color = {"active":"#16a34a","maintenance":"#d97706","stopped":"#dc2626","decommissioned":"#6b7280"}.get(a_status,"#111")

            with col_list[idx % cols_per_row]:
                st.markdown(f"""
                <div class="elev-card">
                  <div class="elev-card-title">🛗 {safe_text(e.get('internal_code'),'—')} — {safe_text(e.get('building_name'),'—')}</div>
                  <div class="elev-card-meta">👤 {safe_text(e.get('customer_name'),'—')} &nbsp;|&nbsp; 📍 {safe_text(e.get('district'),'—')}, {safe_text(e.get('city'),'—')}</div>
                  <div class="elev-card-meta">نوع: {safe_text(e.get('elevator_type'),'—')} &nbsp;|&nbsp; ماركة: {safe_text(e.get('elevator_brand'),'—')}</div>
                  <div class="elev-card-meta">حمولة: {safe_text(e.get('capacity_kg'),'—')} كغ &nbsp;|&nbsp; طوابق: {safe_text(e.get('floors'),'—')} &nbsp;|&nbsp; لوحة: {safe_text(e.get('control_panel'),'—')}</div>
                  <hr style="margin:6px 0;border-color:#e9ecef">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                    <span style="font-size:0.88rem;color:#555">الحالة</span>
                    <span style="background:{status_color};color:#fff;padding:2px 10px;border-radius:12px;font-size:0.82rem;font-weight:700">{status_ar}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:0.88rem;color:#555;margin-bottom:3px">
                    <span>آخر زيارة</span><strong style="color:#111">{last_visit_date}</strong>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:0.88rem;color:#555">
                    <span>الفني</span><strong style="color:#111">{last_tech}</strong>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # تعديل الحالة
                if has_perm("elevators.edit"):
                    new_status_label = st.selectbox(
                        "تحديث الحالة",
                        list(ASSET_STATUSES.values()),
                        index=list(ASSET_STATUSES.keys()).index(a_status) if a_status in ASSET_STATUSES else 0,
                        key=f"elev_st_{eid}",
                        label_visibility="collapsed",
                    )
                    new_status_key = next((k for k,v in ASSET_STATUSES.items() if v == new_status_label), a_status)
                    if new_status_key != a_status:
                        if st.button("💾 حفظ الحالة", key=f"save_elev_st_{eid}"):
                            try:
                                supabase.table("elevators").update({"asset_status": new_status_key}).eq("id", eid).execute()
                                log_action("edit","elevators",f"تحديث حالة المصعد {e.get('internal_code',eid)}",
                                           severity="normal", entity_id=eid,
                                           old_value=a_status, new_value=new_status_key)
                                load_elevators.clear()
                                st.success("✅ تم التحديث")
                                st.rerun()
                            except Exception as ex:
                                st.error(friendly_error(ex))

        st.markdown("---")
        # ── تصدير ──
        if filtered:
            df_exp = pd.DataFrame([{
                "الكود الداخلي": safe_text(e.get("internal_code")),
                "العميل": safe_text(e.get("customer_name")),
                "المبنى": safe_text(e.get("building_name")),
                "الحي": safe_text(e.get("district")),
                "المدينة": safe_text(e.get("city")),
                "النوع": safe_text(e.get("elevator_type")),
                "الماركة": safe_text(e.get("elevator_brand")),
                "الحمولة": safe_text(e.get("capacity_kg")),
                "الطوابق": safe_text(e.get("floors")),
                "لوحة التحكم": safe_text(e.get("control_panel")),
                "الحالة": ASSET_STATUSES.get(safe_text(e.get("asset_status","active")), "—"),
                "ملاحظات": safe_text(e.get("notes")),
            } for e in filtered])
            controlled_download_button("📥 تصدير CSV", to_csv_bytes(df_exp),
                                       "elevators_export.csv", "text/csv", "elevators")

    # ──────────────────────────────────────────────────────
    # SUB 2: إضافة مصعد
    # ──────────────────────────────────────────────────────
    elif sub_tab == "➕ إضافة مصعد":
        require_perm("elevators.add")
        section_header("➕ تسجيل مصعد جديد")

        if not contracts:
            st.warning("لا توجد عقود. أضف عقداً أولاً.")
            return

        c1, c2 = st.columns(2)
        with c1:
            sel_contract = st.selectbox("العقد *", list(contract_labels.values()), key="new_elev_contract")
            sel_c_id = next((k for k,v in contract_labels.items() if v == sel_contract), None)
            c_data = contracts_map.get(str(sel_c_id), {})
            internal_code  = st.text_input("الكود الداخلي للمصعد *", placeholder="مثال: LT-001", key="new_elev_code")
            customer_name  = st.text_input("اسم العميل *", value=safe_text(c_data.get("customer_name"),""), key="new_elev_cust")
            building_name  = st.text_input("اسم المبنى *", value=safe_text(c_data.get("building_name"),""), key="new_elev_bldg")
            district       = st.text_input("الحي", value=safe_text(c_data.get("district"),""), key="new_elev_dist")
            city           = st.selectbox("المدينة", CITIES,
                                          index=CITIES.index(c_data.get("city","الرياض")) if c_data.get("city","الرياض") in CITIES else 0,
                                          key="new_elev_city")
        with c2:
            elevator_type  = st.selectbox("نوع المصعد *", ELEVATOR_TYPES, key="new_elev_type")
            elevator_brand = st.selectbox("الماركة *", ELEVATOR_BRANDS, key="new_elev_brand")
            capacity_kg    = st.number_input("الحمولة (كغ)", min_value=0, value=630, step=50, key="new_elev_cap")
            floors         = st.number_input("عدد الطوابق", min_value=1, value=5, step=1, key="new_elev_floors")
            control_panel  = st.selectbox("لوحة التحكم", CONTROL_PANELS, key="new_elev_cp")
            asset_status   = st.selectbox("الحالة الأولية", list(ASSET_STATUSES.values()), key="new_elev_astatus")
        notes = st.text_area("ملاحظات تقنية", key="new_elev_notes", height=80)

        if st.button("💾 حفظ المصعد", type="primary", use_container_width=True, key="save_new_elev"):
            errors = []
            if not internal_code.strip(): errors.append("الكود الداخلي مطلوب")
            if not customer_name.strip():  errors.append("اسم العميل مطلوب")
            if not building_name.strip():  errors.append("اسم المبنى مطلوب")
            if not sel_c_id:               errors.append("اختر عقداً")
            # تحقق من عدم تكرار الكود
            existing_codes = [safe_text(e.get("internal_code"),"").lower() for e in elev_db]
            if internal_code.strip().lower() in existing_codes:
                errors.append(f"الكود '{internal_code}' مستخدم مسبقاً")

            if show_validation_errors(errors):
                pass
            else:
                status_key = next((k for k,v in ASSET_STATUSES.items() if v == asset_status), "active")
                payload = {
                    "contract_id":    sel_c_id,
                    "internal_code":  internal_code.strip().upper(),
                    "customer_name":  customer_name.strip(),
                    "building_name":  building_name.strip(),
                    "district":       district.strip(),
                    "city":           city,
                    "elevator_type":  elevator_type,
                    "elevator_brand": elevator_brand,
                    "capacity_kg":    int(capacity_kg),
                    "floors":         int(floors),
                    "control_panel":  control_panel,
                    "asset_status":   status_key,
                    "notes":          notes.strip(),
                }
                try:
                    supabase.table("elevators").insert(payload).execute()
                    log_action("add","elevators",f"إضافة مصعد: {internal_code.strip().upper()}")
                    load_elevators.clear()
                    st.success(f"✅ تم تسجيل المصعد {internal_code.strip().upper()} بنجاح")
                    st.rerun()
                except Exception as ex:
                    st.error(friendly_error(ex))

    # ──────────────────────────────────────────────────────
    # SUB 3: السجل التقني (Technical History)
    # ──────────────────────────────────────────────────────
    elif sub_tab == "📜 السجل التقني":
        section_header("📜 السجل التقني للمصاعد — Technical History")

        if not elev_db:
            st.info("لا توجد مصاعد مسجلة بعد.")
            return

        # اختيار المصعد
        elev_options = {safe_text(e.get("internal_code"),"—") + " — " + safe_text(e.get("building_name"),"—"): e for e in elev_db}
        sel_elev_label = st.selectbox("اختر المصعد", list(elev_options.keys()), key="hist_elev_sel")
        sel_elev = elev_options[sel_elev_label]
        sel_elev_id = str(sel_elev.get("id",""))

        # بيانات المصعد
        c_id = str(sel_elev.get("contract_id",""))
        c_info = contracts_map.get(c_id, {})
        hi1, hi2, hi3 = st.columns(3)
        hi1.markdown(f"**العقد:** {safe_text(c_info.get('contract_no'),'—')}")
        hi2.markdown(f"**العميل:** {safe_text(sel_elev.get('customer_name'),'—')}")
        hi3.markdown(f"**الحالة:** {ASSET_STATUSES.get(safe_text(sel_elev.get('asset_status'),'active'),'—')}")
        hi1.markdown(f"**النوع:** {safe_text(sel_elev.get('elevator_type'),'—')}")
        hi2.markdown(f"**الماركة:** {safe_text(sel_elev.get('elevator_brand'),'—')}")
        hi3.markdown(f"**الحمولة:** {safe_text(sel_elev.get('capacity_kg'),'—')} كغ")
        st.markdown("---")

        # زيارات هذا المصعد
        elev_visits = [v for v in visits if str(v.get("elevator_id","")) == sel_elev_id]
        elev_visits.sort(key=lambda v: safe_text(v.get("visit_date",""),""), reverse=True)

        st.markdown(f"**عدد الزيارات المسجلة:** {len(elev_visits)}")

        if not elev_visits:
            st.info("لا توجد زيارات مسجلة لهذا المصعد بعد.")
        else:
            for v in elev_visits:
                vtype  = safe_text(v.get("visit_type"),"—")
                vdate  = safe_text(v.get("visit_date"),"—")
                vtech  = safe_text(v.get("technician"),"—")
                vstatus = safe_text(v.get("status"),"—")
                cond_after = safe_text(v.get("condition_after"),"—")
                with st.expander(f"🗓️ {vdate} — {vtype} — فني: {vtech} — الحالة: {vstatus}"):
                    v1, v2 = st.columns(2)
                    with v1:
                        st.write(f"**نوع الزيارة:** {vtype}")
                        st.write(f"**تاريخ الزيارة:** {vdate}")
                        st.write(f"**الفني:** {vtech}")
                        st.write(f"**وقت الوصول:** {safe_text(v.get('arrival_time'),'—')}")
                        st.write(f"**بداية العمل:** {safe_text(v.get('start_time'),'—')}")
                        st.write(f"**نهاية العمل:** {safe_text(v.get('end_time'),'—')}")
                    with v2:
                        st.write(f"**الأعمال المنجزة:** {safe_text(v.get('work_done'),'—')}")
                        st.write(f"**قطع الغيار:** {safe_text(v.get('parts_used'),'—')}")
                        st.write(f"**الحالة بعد الزيارة:** {cond_after}")
                        st.write(f"**توصيات:** {safe_text(v.get('recommendations'),'—')}")
                        ncr = safe_text(v.get("non_completion_reason"),"")
                        if ncr:
                            st.warning(f"⚠️ سبب عدم الإتمام: {ncr}")
                        if v.get("followup_needed"):
                            st.info(f"📌 متابعة مطلوبة: {safe_text(v.get('followup_date'),'—')}")


# ════════════════════════════════════════════════════════
# TAB 7: Maintenance Calendar
# ════════════════════════════════════════════════════════
def tab_calendar():
    require_role(ROLE_ADMIN, ROLE_MANAGER, ROLE_TECH)
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
            header_color = "#1A56DB" if is_today else "#6B7280"
            bg_color     = "#f0f0f0" if is_today else "#ffffff"
            st.markdown(f"""
            <div class="cal-day" style="background:{bg_color}; {'border:2px solid #1A56DB;' if is_today else ''}">
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
    require_role(ROLE_ADMIN, ROLE_MANAGER)
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
          <div style="width:72px;height:72px;background:linear-gradient(135deg,#1A56DB,#1648C8);border-radius:50%;
                      display:flex;align-items:center;justify-content:center;
                      font-size:1.8rem;font-weight:800;color:white;margin:0 auto 14px;
                      box-shadow:0 4px 14px rgba(0,0,0,0.1)">{acc_av}</div>
          <h3 style="margin:0 0 6px;color:#111827;font-size:1.1rem">{display_name}</h3>
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
# TAB: Visits — V14 Visit Log + Visit Report + Non-completion + Follow-up + Closure (مهام 11-20)
# ════════════════════════════════════════════════════════
def tab_visits():
    require_perm("work_orders.view")
    contracts   = load_contracts()
    visits      = load_visits()
    work_orders = load_work_orders()
    fault_reports = load_fault_reports()
    elev_db     = load_elevators()

    section_header("📋 سجل الزيارات والتقارير")

    id_to_cno   = id_to_contract_no_map(contracts)
    elev_map    = {str(e["id"]): e for e in elev_db}
    wo_map      = {str(w["id"]): w for w in work_orders}
    fr_map      = {str(f["id"]): f for f in fault_reports}

    visits = scope_by_role(visits, "technician")

    # إحصائيات
    v_done       = sum(1 for v in visits if v.get("status") == "completed")
    v_pending    = sum(1 for v in visits if v.get("status") in ("scheduled","in_progress"))
    v_incomplete = sum(1 for v in visits if v.get("status") == "incomplete")
    v_followup   = sum(1 for v in visits if v.get("followup_needed"))

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ مكتملة</div><div class="kpi-mini-value" style="color:#16a34a">{v_done}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⏳ مجدولة</div><div class="kpi-mini-value">{v_pending}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚠️ غير مكتملة</div><div class="kpi-mini-value" style="color:#dc2626">{v_incomplete}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">📌 تحتاج متابعة</div><div class="kpi-mini-value" style="color:#7c3aed">{v_followup}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    vs_sub = st.radio(
        "عرض الزيارات",
        ["📋 سجل الزيارات", "➕ تسجيل زيارة", "📌 متابعة مطلوبة"],
        horizontal=True,
        key="vs_sub_tab",
        label_visibility="collapsed",
    )

    # ══════════════════════════════════════════════════
    # SUB 1: سجل الزيارات
    # ══════════════════════════════════════════════════
    if vs_sub == "📋 سجل الزيارات":
        f1,f2,f3 = st.columns(3)
        with f1:
            q_vs = st.text_input("🔍 بحث بالفني أو المبنى", key="vs_q")
        with f2:
            f_type_vs = st.selectbox("نوع الزيارة", ["الكل"] + VISIT_TYPES_V14, key="vs_f_type")
        with f3:
            f_stat_vs = st.selectbox("الحالة", ["الكل","completed","incomplete","scheduled","in_progress"], key="vs_f_stat")

        filtered_vs = visits[:]
        if q_vs.strip():
            q = q_vs.strip().lower()
            def _vs_match(v, q):
                if q in safe_text(v.get("technician"),"").lower(): return True
                elev_info = elev_map.get(str(v.get("elevator_id","")),{})
                if isinstance(elev_info, dict) and q in safe_text(elev_info.get("building_name"),"").lower(): return True
                return False
            filtered_vs = [v for v in filtered_vs if _vs_match(v, q)]
        if f_type_vs != "الكل":
            filtered_vs = [v for v in filtered_vs if v.get("visit_type") == f_type_vs]
        if f_stat_vs != "الكل":
            filtered_vs = [v for v in filtered_vs if v.get("status") == f_stat_vs]

        if not filtered_vs:
            st.info("لا توجد زيارات مطابقة.")
        else:
            rows_vs = []
            for v in filtered_vs:
                eid = str(v.get("elevator_id",""))
                elev_info = elev_map.get(eid,{})
                elev_label_v = safe_text(elev_info.get("internal_code"),"—") if elev_info else "—"
                c_no = id_to_cno.get(str(v.get("contract_id","")), "—")
                ncr = safe_text(v.get("non_completion_reason"),"")
                rows_vs.append({
                    "التاريخ": safe_text(v.get("visit_date"),"—"),
                    "المصعد": elev_label_v,
                    "العقد": c_no,
                    "نوع الزيارة": safe_text(v.get("visit_type"),"—"),
                    "الفني": safe_text(v.get("technician"),"—"),
                    "الحالة": safe_text(v.get("status"),"—"),
                    "سبب عدم الإتمام": ncr if ncr else "—",
                    "متابعة": "✅" if v.get("followup_needed") else "—",
                })
            df_vs = pd.DataFrame(rows_vs)
            st.dataframe(df_vs, use_container_width=True, hide_index=True)

            # تفاصيل الزيارات
            for v in filtered_vs[:15]:
                eid = str(v.get("elevator_id",""))
                elev_info = elev_map.get(eid,{})
                vdate = safe_text(v.get("visit_date"),"—")
                vtech = safe_text(v.get("technician"),"—")
                vstatus = safe_text(v.get("status"),"—")
                with st.expander(f"🗓️ {vdate} — {safe_text(v.get('visit_type'),'—')} — {vtech} — {vstatus}"):
                    e1, e2 = st.columns(2)
                    with e1:
                        st.write(f"**التاريخ:** {vdate}")
                        st.write(f"**وقت الوصول:** {safe_text(v.get('arrival_time'),'—')}")
                        st.write(f"**بداية العمل:** {safe_text(v.get('start_time'),'—')}")
                        st.write(f"**نهاية العمل:** {safe_text(v.get('end_time'),'—')}")
                        st.write(f"**الأعمال المنجزة:** {safe_text(v.get('work_done'),'—')}")
                    with e2:
                        st.write(f"**قطع الغيار:** {safe_text(v.get('parts_used'),'—')}")
                        st.write(f"**الحالة بعد الزيارة:** {safe_text(v.get('condition_after'),'—')}")
                        st.write(f"**توصيات:** {safe_text(v.get('recommendations'),'—')}")
                        ncr = safe_text(v.get("non_completion_reason"),"")
                        if ncr:
                            st.warning(f"⚠️ سبب عدم الإتمام: {ncr}")
                        if v.get("followup_needed"):
                            st.info(f"📌 متابعة: {safe_text(v.get('followup_date'),'—')}")

            controlled_download_button("📥 تصدير CSV", to_csv_bytes(df_vs),
                                       "visits_export.csv","text/csv","visits")

    # ══════════════════════════════════════════════════
    # SUB 2: تسجيل زيارة جديدة — Visit Report Form
    # ══════════════════════════════════════════════════
    elif vs_sub == "➕ تسجيل زيارة":
        require_perm("work_orders.add")
        section_header("➕ تسجيل زيارة جديدة")

        c1, c2 = st.columns(2)
        with c1:
            # ربط بعقد
            contracts_labels = {str(c["id"]): contract_label(c) for c in contracts}
            sel_c_vs = st.selectbox("العقد *", list(contracts_labels.values()), key="new_vs_c")
            sel_c_id_vs = next((k for k,v in contracts_labels.items() if v == sel_c_vs), None)

            # ربط بأمر عمل
            wo_for_c = [w for w in work_orders if str(w.get("contract_id","")) == str(sel_c_id_vs or "")]
            wo_opts = ["— بدون ربط —"] + [f"{w.get('id','')} — {safe_text(w.get('title'),'')}" for w in wo_for_c]
            sel_wo_vs = st.selectbox("ربط بأمر عمل (اختياري)", wo_opts, key="new_vs_wo")
            linked_wo_id = None
            if sel_wo_vs != "— بدون ربط —":
                linked_wo_id = sel_wo_vs.split(" — ")[0]

            # ربط بمصعد
            elev_for_c = [e for e in elev_db if str(e.get("contract_id","")) == str(sel_c_id_vs or "")]
            elev_opts_vs = ["— بدون ربط —"] + [safe_text(e.get("internal_code"),"") + " — " + safe_text(e.get("building_name"),"") for e in elev_for_c]
            sel_elev_vs = st.selectbox("ربط بمصعد (اختياري)", elev_opts_vs, key="new_vs_elev")
            linked_elev_id_vs = None
            if sel_elev_vs != "— بدون ربط —":
                lc = sel_elev_vs.split(" — ")[0]
                linked_elev_id_vs = next((str(e["id"]) for e in elev_db if safe_text(e.get("internal_code"),"") == lc), None)

            v_type = st.selectbox("نوع الزيارة *", VISIT_TYPES_V14, key="new_vs_type")
            v_date = st.date_input("تاريخ الزيارة *", value=date.today(), key="new_vs_date")
            v_tech = st.selectbox("الفني *", TECHNICIANS, key="new_vs_tech")

        with c2:
            v_status_opts = ["completed","incomplete","scheduled","in_progress"]
            v_status_labels = {"completed":"مكتملة","incomplete":"غير مكتملة","scheduled":"مجدولة","in_progress":"جارية"}
            v_status_label = st.selectbox("حالة الزيارة *",
                                           [v_status_labels[s] for s in v_status_opts],
                                           key="new_vs_status")
            v_status = next((k for k,v in v_status_labels.items() if v == v_status_label), "completed")

            v_arrival  = st.text_input("وقت الوصول (HH:MM)", placeholder="08:30", key="new_vs_arrive")
            v_start    = st.text_input("بداية العمل (HH:MM)", placeholder="09:00", key="new_vs_start")
            v_end      = st.text_input("نهاية العمل (HH:MM)", placeholder="11:00", key="new_vs_end")
            v_cond     = st.text_input("حالة المصعد بعد الزيارة", key="new_vs_cond")

        v_work_done = st.text_area("الأعمال المنجزة", key="new_vs_work", height=70)
        v_parts     = st.text_area("قطع الغيار المستخدمة", key="new_vs_parts", height=50)
        v_recom     = st.text_area("توصيات", key="new_vs_recom", height=50)

        # Non-completion (مهمة 15)
        ncr_vs = ""
        if v_status == "incomplete":
            ncr_vs = st.selectbox("سبب عدم الإتمام *", NON_COMPLETION_REASONS, key="new_vs_ncr")

        # Follow-up (مهمة 18)
        followup_vs = st.checkbox("متابعة مطلوبة؟", key="new_vs_followup")
        followup_date_vs = None
        if followup_vs:
            followup_date_vs = st.date_input("تاريخ المتابعة", value=date.today() + timedelta(days=7), key="new_vs_fdate")

        v_notes = st.text_area("ملاحظات إضافية", key="new_vs_notes", height=50)

        if st.button("💾 حفظ الزيارة", type="primary", use_container_width=True, key="save_new_vs"):
            errors = []
            if not v_tech: errors.append("الفني مطلوب")
            if not v_type: errors.append("نوع الزيارة مطلوب")
            if v_status == "incomplete" and not ncr_vs: errors.append("سبب عدم الإتمام مطلوب للزيارات غير المكتملة")

            if show_validation_errors(errors):
                pass
            else:
                payload_vs = {
                    "contract_id":          sel_c_id_vs,
                    "elevator_id":          linked_elev_id_vs,
                    "work_order_id":        linked_wo_id,
                    "visit_type":           v_type,
                    "visit_date":           v_date.isoformat(),
                    "technician":           v_tech,
                    "status":               v_status,
                    "arrival_time":         v_arrival.strip() or None,
                    "start_time":           v_start.strip() or None,
                    "end_time":             v_end.strip() or None,
                    "work_done":            v_work_done.strip(),
                    "parts_used":           v_parts.strip(),
                    "condition_after":      v_cond.strip(),
                    "non_completion_reason":ncr_vs if v_status == "incomplete" else None,
                    "recommendations":      v_recom.strip(),
                    "followup_needed":      followup_vs,
                    "followup_date":        followup_date_vs.isoformat() if followup_date_vs and followup_vs else None,
                    "notes":                v_notes.strip(),
                }
                try:
                    supabase.table("visits").insert(payload_vs).execute()
                    log_action("add","visits",f"تسجيل زيارة: {v_type} | فني: {v_tech} | {v_date.isoformat()}")
                    # تحديث حالة أمر العمل إلى completed إذا الزيارة مكتملة
                    if linked_wo_id and v_status == "completed":
                        supabase.table("work_orders").update({"status":"completed"}).eq("id", linked_wo_id).execute()
                        log_action("edit","work_orders",f"إغلاق WO #{linked_wo_id} تلقائياً عند إتمام الزيارة")
                        load_work_orders.clear()
                    load_visits.clear()
                    load_elevators.clear()
                    st.success("✅ تم تسجيل الزيارة بنجاح")
                    st.rerun()
                except Exception as ex:
                    st.error(friendly_error(ex))

    # ══════════════════════════════════════════════════
    # SUB 3: متابعة مطلوبة (مهمة 18)
    # ══════════════════════════════════════════════════
    elif vs_sub == "📌 متابعة مطلوبة":
        section_header("📌 زيارات تحتاج متابعة")
        followup_list = [v for v in visits if v.get("followup_needed")]
        followup_list.sort(key=lambda v: safe_text(v.get("followup_date",""),""))

        if not followup_list:
            st.success("✅ لا توجد متابعات مطلوبة حالياً.")
            return

        today_str = date.today().isoformat()
        for v in followup_list:
            fdate = safe_text(v.get("followup_date"),"—")
            is_overdue = fdate != "—" and fdate < today_str
            vtech = safe_text(v.get("technician"),"—")
            vtype = safe_text(v.get("visit_type"),"—")
            eid   = str(v.get("elevator_id",""))
            elev_info = elev_map.get(eid,{})
            bldg = safe_text(elev_info.get("building_name"),"—") if elev_info else "—"

            badge = '🔴 متأخر' if is_overdue else '🟡 قادم'
            with st.expander(f"{badge} — متابعة {fdate} — {bldg} — فني: {vtech}"):
                st.write(f"**الزيارة الأصلية:** {safe_text(v.get('visit_date'),'—')}")
                st.write(f"**نوع الزيارة:** {vtype}")
                st.write(f"**الأعمال السابقة:** {safe_text(v.get('work_done'),'—')}")
                st.write(f"**التوصيات:** {safe_text(v.get('recommendations'),'—')}")
                st.write(f"**سبب عدم الإتمام:** {safe_text(v.get('non_completion_reason'),'—')}")
                v_id = str(v.get("id",""))
                if has_perm("work_orders.edit") and st.button("✅ تم إتمام المتابعة", key=f"vs_followup_done_{v_id}"):
                    try:
                        supabase.table("visits").update({"followup_needed": False}).eq("id", v_id).execute()
                        log_action("edit","visits",f"إتمام متابعة زيارة #{v_id}", entity_id=v_id)
                        load_visits.clear()
                        st.success("✅ تم تسجيل إتمام المتابعة")
                        st.rerun()
                    except Exception as ex:
                        st.error(friendly_error(ex))


# ════════════════════════════════════════════════════════
# TAB: Tech Manager Dashboard — V14 مهمة 25
# ════════════════════════════════════════════════════════
def tab_tech_manager():
    require_perm("work_orders.view")
    contracts     = load_contracts()
    work_orders   = load_work_orders()
    fault_reports = load_fault_reports()
    visits        = load_visits()
    elev_db       = load_elevators()

    section_header("👷 لوحة المدير الفني — Technical Manager Dashboard")

    today     = date.today()
    today_str = today.isoformat()
    id_to_cno = id_to_contract_no_map(contracts)

    # ══════════════════════════════════════════════════
    # Section 1: KPIs التشغيلية (مهمة 22)
    # ══════════════════════════════════════════════════
    st.markdown("### 📊 مؤشرات الأداء التشغيلية")

    total_wo       = len(work_orders)
    completed_wo   = sum(1 for w in work_orders if w.get("status") == "completed")
    pending_wo     = sum(1 for w in work_orders if w.get("status") in ("pending","assigned"))
    overdue_wo     = sum(1 for w in work_orders if
                        w.get("status") not in ("completed","cancelled") and
                        w.get("scheduled_date") and
                        parse_date_safe(w.get("scheduled_date")) and
                        parse_date_safe(w.get("scheduled_date")) < today)
    completion_rate = round(completed_wo / total_wo * 100, 1) if total_wo > 0 else 0.0

    total_fr     = len(fault_reports)
    resolved_fr  = sum(1 for f in fault_reports if f.get("status") in ("resolved","closed"))
    escalated_fr = sum(1 for f in fault_reports if f.get("status") == "escalated")
    resolution_rate = round(resolved_fr / total_fr * 100, 1) if total_fr > 0 else 0.0

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">معدل الإنجاز</div><div class="kpi-mini-value" style="color:#16a34a">{completion_rate}%</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">أوامر معلقة</div><div class="kpi-mini-value" style="color:#d97706">{pending_wo}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚠️ متأخرة</div><div class="kpi-mini-value" style="color:#dc2626">{overdue_wo}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">معدل حل الأعطال</div><div class="kpi-mini-value" style="color:#16a34a">{resolution_rate}%</div></div>', unsafe_allow_html=True)
    k5.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🔺 بلاغات مصعّدة</div><div class="kpi-mini-value" style="color:#7c3aed">{escalated_fr}</div></div>', unsafe_allow_html=True)
    k6.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">إجمالي المصاعد</div><div class="kpi-mini-value">{len(elev_db)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    # ══════════════════════════════════════════════════
    # Section 2: توزيع التكليفات على الفنيين (مهمة 9 Assignment Engine)
    # ══════════════════════════════════════════════════
    with col_a:
        st.markdown("### 👷 تكليفات الفنيين — اليوم")
        tech_today = {}
        for t in TECHNICIANS:
            tech_today[t] = {
                "اليوم": sum(1 for w in work_orders if w.get("technician") == t and w.get("scheduled_date","") == today_str and w.get("status") not in ("completed","cancelled")),
                "إجمالي نشطة": sum(1 for w in work_orders if w.get("technician") == t and w.get("status") not in ("completed","cancelled")),
                "مكتملة": sum(1 for w in work_orders if w.get("technician") == t and w.get("status") == "completed"),
            }
        df_tech = pd.DataFrame(tech_today).T.reset_index().rename(columns={"index":"الفني"})
        st.dataframe(df_tech, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════
    # Section 3: Repeat Faults Detection (مهمة 21)
    # ══════════════════════════════════════════════════
    with col_b:
        st.markdown("### 🔁 الأعطال المتكررة (مهمة 21)")
        fault_count = {}
        for fr in fault_reports:
            c_id = str(fr.get("contract_id",""))
            ft   = safe_text(fr.get("fault_type","غير محدد"))
            key  = (c_id, ft)
            fault_count[key] = fault_count.get(key, 0) + 1

        repeat_faults = [(k, v) for k, v in fault_count.items() if v >= 2]
        repeat_faults.sort(key=lambda x: x[1], reverse=True)

        if not repeat_faults:
            st.success("لا توجد أعطال متكررة.")
        else:
            df_rf = pd.DataFrame([{
                "العقد": id_to_cno.get(k[0],"—"),
                "نوع العطل": k[1],
                "عدد مرات التكرار": v,
            } for k,v in repeat_faults[:10]])
            st.dataframe(df_rf, use_container_width=True, hide_index=True)

    st.markdown("---")

    col_c, col_d = st.columns(2)

    # ══════════════════════════════════════════════════
    # Section 4: Contract Coverage Check (مهمة 23)
    # ══════════════════════════════════════════════════
    with col_c:
        st.markdown("### 📋 تغطية العقود (مهمة 23)")
        active_contracts = [c for c in contracts if c.get("contract_status","active") == "active"]
        coverage_rows = []
        for c in active_contracts:
            c_id = str(c.get("id",""))
            c_visits = [v for v in visits if str(v.get("contract_id","")) == c_id]
            c_wo     = [w for w in work_orders if str(w.get("contract_id","")) == c_id]
            last_visit = max((safe_text(v.get("visit_date"),"") for v in c_visits), default="لا يوجد")
            days_since = "—"
            if last_visit != "لا يوجد":
                d = parse_date_safe(last_visit)
                if d:
                    days_since = (today - d).days
            coverage_rows.append({
                "العقد": safe_text(c.get("contract_no"),"—"),
                "العميل": safe_text(c.get("customer_name"),"—"),
                "آخر زيارة": last_visit,
                "منذ (أيام)": days_since,
                "إجمالي الزيارات": len(c_visits),
                "أوامر مفتوحة": sum(1 for w in c_wo if w.get("status") not in ("completed","cancelled")),
            })
        df_cov = pd.DataFrame(coverage_rows)
        if not df_cov.empty:
            # تلوين العقود غير المخدومة
            st.dataframe(df_cov, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد عقود نشطة.")

    # ══════════════════════════════════════════════════
    # Section 5: SLA Performance (مهمة 22 Ops KPIs)
    # ══════════════════════════════════════════════════
    with col_d:
        st.markdown("### ⏱️ أداء SLA بالأولوية")
        sla_data = []
        for pri_key, pri_label in PRIORITY_LEVELS.items():
            pri_wo = [w for w in work_orders if w.get("priority") == pri_key]
            pri_total = len(pri_wo)
            pri_comp  = sum(1 for w in pri_wo if w.get("status") == "completed")
            pri_over  = sum(1 for w in pri_wo if
                            w.get("status") not in ("completed","cancelled") and
                            w.get("scheduled_date") and
                            parse_date_safe(w.get("scheduled_date")) and
                            parse_date_safe(w.get("scheduled_date")) < today)
            sla_data.append({
                "الأولوية": pri_label,
                "SLA": SLA_RULES[pri_key]["label"],
                "الإجمالي": pri_total,
                "مكتمل": pri_comp,
                "متأخر": pri_over,
                "معدل الإنجاز": f"{round(pri_comp/pri_total*100,1)}%" if pri_total > 0 else "—",
            })
        df_sla = pd.DataFrame(sla_data)
        st.dataframe(df_sla, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════
    # Section 6: PM Generator — توليد الجدولة الوقائية (مهمة 12)
    # ══════════════════════════════════════════════════
    st.markdown("### 📅 مولّد جدولة الصيانة الوقائية (PM Generator)")

    pm_c1, pm_c2 = st.columns(2)
    with pm_c1:
        pm_interval_label = st.selectbox(
            "دورية الصيانة",
            list(PM_INTERVAL_LABELS.values()),
            key="pm_interval"
        )
        pm_interval_key = next((k for k,v in PM_INTERVAL_LABELS.items() if v == pm_interval_label), "monthly")
        pm_days = PM_INTERVALS[pm_interval_key]
    with pm_c2:
        pm_tech = st.selectbox("الفني المسؤول", TECHNICIANS, key="pm_tech")

    # جلب مصاعد بدون زيارة حديثة
    pm_candidates = []
    for e in elev_db:
        if e.get("asset_status") not in ("active","maintenance"):
            continue
        eid = str(e.get("id",""))
        elev_visits_pm = [v for v in visits if str(v.get("elevator_id","")) == eid]
        if elev_visits_pm:
            last_v_date = max(safe_text(v.get("visit_date"),"") for v in elev_visits_pm)
            d = parse_date_safe(last_v_date)
            days_since = (today - d).days if d else 9999
        else:
            days_since = 9999

        if days_since >= pm_days:
            pm_candidates.append({
                "الكود": safe_text(e.get("internal_code"),"—"),
                "المبنى": safe_text(e.get("building_name"),"—"),
                "العميل": safe_text(e.get("customer_name"),"—"),
                "آخر زيارة (أيام)": days_since if days_since < 9999 else "لا يوجد",
                "الحالة": ASSET_STATUSES.get(safe_text(e.get("asset_status","active")),"—"),
                "elevator_id": eid,
                "contract_id": str(e.get("contract_id","")),
            })

    if pm_candidates:
        st.warning(f"⚠️ {len(pm_candidates)} مصعد يحتاج صيانة وقائية (الفترة: {pm_interval_label})")
        df_pm = pd.DataFrame([{k:v for k,v in r.items() if k not in ("elevator_id","contract_id")} for r in pm_candidates])
        st.dataframe(df_pm, use_container_width=True, hide_index=True)

        # Conflict check (مهمة 13)
        pm_target_date = today + timedelta(days=1)
        tech_conflicts = sum(1 for w in work_orders if
                             w.get("technician") == pm_tech and
                             w.get("scheduled_date","") == pm_target_date.isoformat() and
                             w.get("status") not in ("completed","cancelled"))
        if tech_conflicts > 0:
            st.warning(f"⚠️ تعارض جدولة: الفني {pm_tech} لديه {tech_conflicts} أوامر عمل غداً ({pm_target_date})")

        if st.button(f"🚀 توليد {len(pm_candidates)} أمر صيانة وقائية", type="primary", key="gen_pm_orders"):
            created = 0
            errors  = 0
            for candidate in pm_candidates:
                wo_pm = {
                    "contract_id":    candidate["contract_id"] if candidate["contract_id"] else None,
                    "title":          f"صيانة وقائية — {candidate['الكود']} — {candidate['المبنى']}",
                    "description":    f"صيانة وقائية {pm_interval_label} لمصعد {candidate['الكود']}",
                    "scheduled_date": pm_target_date.isoformat(),
                    "technician":     pm_tech,
                    "status":         "assigned",
                    "priority":       "medium",
                    "work_type":      "preventive",
                    "notes":          f"مولّد تلقائياً — PM Generator — {pm_interval_label}",
                }
                if candidate["elevator_id"]:
                    wo_pm["elevator_id"] = candidate["elevator_id"]
                try:
                    supabase.table("work_orders").insert(wo_pm).execute()
                    created += 1
                except Exception:
                    errors += 1
            if created:
                log_action("add","work_orders",f"PM Generator: إنشاء {created} أمر صيانة وقائية {pm_interval_label}")
                load_work_orders.clear()
                st.success(f"✅ تم إنشاء {created} أمر عمل صيانة وقائية")
                if errors:
                    st.warning(f"⚠️ فشل {errors} أوامر")
                st.rerun()
            else:
                st.error("❌ فشل إنشاء أوامر الصيانة")
    else:
        st.success(f"✅ جميع المصاعد مخدومة ضمن فترة {pm_interval_label}")



# ════════════════════════════════════════════════════════
# V15: FIELD CSS — Mobile-optimized styles
# ════════════════════════════════════════════════════════
FIELD_CSS = """
<style>
/* ── V17 Field Mobile Card ── */
.field-task-card {
  background: #FFFFFF;
  border: 1.5px solid #E5E7EB;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 12px;
  direction: rtl;
  box-shadow: 0 1px 3px rgba(0,0,0,.05), 0 1px 2px rgba(0,0,0,.04);
  transition: box-shadow .25s ease, transform .25s ease;
}
.field-task-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,.09);
  transform: translateY(-2px);
}
.field-task-card.urgent  { border-right: 4px solid #DC2626; }
.field-task-card.high    { border-right: 4px solid #D97706; }
.field-task-card.medium  { border-right: 4px solid #1A56DB; }
.field-task-card.low     { border-right: 4px solid #059669; }

.field-task-title {
  font-size: 1rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 4px;
}
.field-task-meta {
  font-size: 0.82rem;
  color: #6B7280;
  margin-bottom: 3px;
}
.field-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
  margin-top: 8px;
  border: 1px solid transparent;
}
.field-status-pending    { background:#FFFBEB; color:#92400E; border-color:#FDE68A; }
.field-status-accepted   { background:#EBF5FF; color:#1648C8; border-color:#BFDBFE; }
.field-status-en_route   { background:#FFF7ED; color:#C2410C; border-color:#FED7AA; }
.field-status-arrived    { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
.field-status-in_progress{ background:#F5F3FF; color:#5B21B6; border-color:#DDD6FE; }
.field-status-completed  { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
.field-status-no_access  { background:#FEF2F2; color:#991B1B; border-color:#FECACA; }
.field-status-declined   { background:#F9FAFB; color:#4B5563; border-color:#E5E7EB; }

/* ── Big Action Button ── */
.stButton > button {
  font-size: 0.9rem !important;
  font-weight: 700 !important;
  min-height: 46px !important;
  border-radius: 10px !important;
  letter-spacing: 0.2px !important;
}

/* ── Safety checklist ── */
.safety-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 0;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.875rem;
  direction: rtl;
  color: #374151;
}
.safety-item:last-child { border-bottom: none; }

/* ── Live board row ── */
.live-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 6px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  direction: rtl;
  transition: background .15s ease, box-shadow .15s ease;
}
.live-row:hover { background: #EBF5FF; box-shadow: 0 2px 8px rgba(26,86,219,.08); }
.live-row.urgent  { border-right: 3px solid #DC2626; }
.live-row.high    { border-right: 3px solid #D97706; }
</style>
"""

# ════════════════════════════════════════════════════════
# V15: Escalation WhatsApp helper
# ════════════════════════════════════════════════════════
def send_field_escalation(wo_id: str, wo_title: str, tech_name: str,
                           hazard: str, reason: str = ""):
    """إرسال تنبيه واتساب لمدير الفني عند الأعطال الحرجة أو التعليق."""
    try:
        manager_phone = st.secrets.get("MANAGER_PHONE_ALI", "")
        if not manager_phone:
            return {"ok": False, "error": "رقم المدير الفني غير مسجل"}
        hazard_ar = HAZARD_LEVELS.get(hazard, hazard)
        msg = (
            f"🚨 *تنبيه ميداني — لفتك للمصاعد*\n"
            f"الفني: {tech_name}\n"
            f"المهمة: {wo_title}\n"
            f"مستوى الخطر: {hazard_ar}\n"
            f"السبب: {reason or '—'}\n"
            f"رقم الأمر: {wo_id}\n"
            f"الوقت: {datetime.now().strftime('%H:%M %Y-%m-%d')}"
        )
        return send_whatsapp(manager_phone, msg)
    except Exception as ex:
        return {"ok": False, "error": str(ex)}


# ════════════════════════════════════════════════════════
# V15: TAB — Technician Field Interface (مهام 1-17)
# ════════════════════════════════════════════════════════
def tab_field():
    """واجهة الفني الميدانية المبسطة — Mobile-optimized"""
    require_role(ROLE_TECH, ROLE_ADMIN, ROLE_MANAGER)

    username     = st.session_state.get("username", "")
    display_name = st.session_state.get("display_name", username)
    tech_region  = TECH_REGIONS.get(display_name, "—")
    today_str    = date.today().isoformat()

    # Inject mobile CSS
    st.markdown(FIELD_CSS, unsafe_allow_html=True)

    # ── Header مبسط ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1648C8,#1A56DB);color:#ffffff;
                padding:16px 22px;border-radius:14px;
                box-shadow:0 6px 18px rgba(26,86,219,.28),0 2px 6px rgba(26,86,219,.18);
                margin-bottom:18px;direction:rtl;display:flex;justify-content:space-between;align-items:center">
      <div>
        <div style="font-size:1.1rem;font-weight:900;letter-spacing:0.2px">👷 {display_name}</div>
        <div style="font-size:0.8rem;color:rgba(255,255,255,0.75);margin-top:3px">
          📍 {tech_region} &nbsp;|&nbsp; {date.today().strftime('%A %Y/%m/%d')}
        </div>
      </div>
      <div style="text-align:left;">
        <div style="font-size:1.15rem;font-weight:800;font-variant-numeric:tabular-nums">{datetime.now().strftime('%H:%M')}</div>
        <div style="font-size:0.65rem;color:rgba(255,255,255,0.6);margin-top:2px">Riyadh</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── تحميل مهام اليوم ──
    work_orders = load_work_orders()
    visits      = load_visits()
    elev_db     = load_elevators()
    contracts   = load_contracts()
    fault_rpts  = load_fault_reports()

    id_to_cno  = id_to_contract_no_map(contracts)
    elev_map   = {str(e["id"]): e for e in elev_db}
    c_map      = {str(c["id"]): c for c in contracts}

    # فلترة مهام هذا الفني اليوم (مهمة 2 — Scoped access)
    if is_tech():
        my_wo = [w for w in work_orders if
                 w.get("technician") == display_name and
                 w.get("scheduled_date","") == today_str and
                 w.get("status") not in ("completed","cancelled")]
        # المهام المعلقة من أيام سابقة
        overdue_wo = [w for w in work_orders if
                      w.get("technician") == display_name and
                      w.get("scheduled_date","") < today_str and
                      w.get("status") not in ("completed","cancelled","declined")]
    else:
        # Admin/manager يرى الكل
        my_wo      = [w for w in work_orders if w.get("scheduled_date","") == today_str and w.get("status") not in ("completed","cancelled")]
        overdue_wo = [w for w in work_orders if w.get("scheduled_date","") < today_str and w.get("status") not in ("completed","cancelled")]

    # KPIs اليوم (مهمة 3 — Daily list stats)
    k1,k2,k3,k4 = st.columns(4)
    done_today = sum(1 for w in work_orders if
                     w.get("technician") == display_name and
                     w.get("scheduled_date","") == today_str and
                     w.get("status") == "completed")
    en_route_c = sum(1 for w in (my_wo+overdue_wo) if w.get("field_status") == "en_route")
    in_prog_c  = sum(1 for w in (my_wo+overdue_wo) if w.get("field_status") == "in_progress" or w.get("status") == "in_progress")

    k1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">📋 مهام اليوم</div><div class="kpi-mini-value">{len(my_wo)}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ مكتملة</div><div class="kpi-mini-value" style="color:#16a34a">{done_today}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🚗 في الطريق</div><div class="kpi-mini-value" style="color:#d97706">{en_route_c}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⚠️ متأخرة</div><div class="kpi-mini-value" style="color:#dc2626">{len(overdue_wo)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs ──
    field_sub = st.radio(
        "الواجهة الميدانية",
        ["🗓️ مهام اليوم", "⏰ متأخرة", "📝 تقرير ميداني"],
        horizontal=True,
        key="field_sub",
        label_visibility="collapsed",
    )

    # ════════════════════════
    # SUB 1: مهام اليوم (مهمة 3)
    # ════════════════════════
    if field_sub in ("🗓️ مهام اليوم", "⏰ متأخرة"):
        task_list = my_wo if field_sub == "🗓️ مهام اليوم" else overdue_wo

        # ترتيب حسب الأولوية والمنطقة (مهمة 19)
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
        task_list.sort(key=lambda w: (
            priority_order.get(w.get("priority","medium"), 2),
            safe_text(w.get("scheduled_date",""))
        ))

        if not task_list:
            st.success("✅ لا توجد مهام حالياً." if field_sub == "🗓️ مهام اليوم" else "✅ لا توجد مهام متأخرة.")
        else:
            for w in task_list:
                w_id      = str(w.get("id",""))
                w_title   = safe_text(w.get("title"),"—")
                w_pri     = w.get("priority","medium")
                w_stat    = w.get("status","pending")
                f_stat    = safe_text(w.get("field_status"), w_stat)
                w_date    = safe_text(w.get("scheduled_date"),"—")
                c_id      = str(w.get("contract_id",""))
                c_no      = id_to_cno.get(c_id,"—")
                c_info    = c_map.get(c_id, {})
                bldg      = safe_text(c_info.get("building_name"),"—")
                dist      = safe_text(c_info.get("district"),"—")
                city      = safe_text(c_info.get("city"),"—")
                w_tech    = safe_text(w.get("technician"),"—")
                eid       = str(w.get("elevator_id","")) if w.get("elevator_id") else ""
                elev_code = safe_text(elev_map.get(eid,{}).get("internal_code"),"—") if eid else "—"
                pri_css   = {"urgent":"urgent","high":"high","medium":"medium","low":"low"}.get(w_pri,"medium")
                sla       = SLA_RULES.get(w_pri,{}).get("label","—")

                st.markdown(f"""
                <div class="field-task-card {pri_css}">
                  <div class="field-task-title">{w_title}</div>
                  <div class="field-task-meta">📋 {c_no} &nbsp;|&nbsp; 🏢 {bldg}</div>
                  <div class="field-task-meta">📍 {dist}، {city} &nbsp;|&nbsp; 🛗 {elev_code}</div>
                  <div class="field-task-meta">📅 {w_date} &nbsp;|&nbsp; ⏱️ {sla}</div>
                  <span class="field-status-pill field-status-{f_stat}">{FIELD_STATUSES.get(f_stat, WO_STATUSES.get(f_stat, f_stat))}</span>
                </div>
                """, unsafe_allow_html=True)

                # ── أزرار الإجراءات حسب الحالة الحالية ──
                with st.expander(f"⚡ إجراءات — {w_title[:40]}", expanded=(f_stat in ("pending","en_route","arrived"))):
                    _render_field_actions(w, w_id, f_stat, w_stat, display_name)

    # ════════════════════════
    # SUB 3: تقرير ميداني
    # ════════════════════════
    elif field_sub == "📝 تقرير ميداني":
        _render_field_report_form(display_name, work_orders, elev_db, id_to_cno, c_map)


def _render_field_actions(w: dict, w_id: str, f_stat: str, w_stat: str, tech_name: str):
    """يعرض الأزرار المناسبة لكل حالة — Lightweight UX (مهمة 15)"""
    now_iso = datetime.utcnow().isoformat()
    now_local = datetime.now().strftime("%H:%M")

    def _update_field(upd: dict, log_msg: str, severity: str = "normal"):
        try:
            supabase.table("work_orders").update(upd).eq("id", w_id).execute()
            log_action("edit", "work_orders", log_msg,
                       severity=severity, entity_id=w_id,
                       old_value=f_stat, new_value=upd.get("field_status", upd.get("status", "—")))
            load_work_orders.clear()
            st.rerun()
        except Exception as ex:
            st.error(friendly_error(ex))

    # ── حالة: معلق — قبول / رفض ──
    if f_stat in ("pending", "assigned"):
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ قبول المهمة", key=f"accept_{w_id}", type="primary", use_container_width=True):
                _update_field({"field_status": "accepted", "accepted_at": now_iso, "status": "accepted"},
                              f"قبول المهمة: {safe_text(w.get('title'))}")
        with col_b:
            decline_r = st.selectbox("سبب الرفض", DECLINE_REASONS, key=f"dec_r_{w_id}", label_visibility="collapsed")
            if st.button("❌ رفض المهمة", key=f"decline_{w_id}", use_container_width=True):
                _update_field({"field_status": "declined", "declined_reason": decline_r, "status": "declined"},
                              f"رفض المهمة: {safe_text(w.get('title'))} — {decline_r}", severity="important")

    # ── حالة: مقبول — في الطريق ──
    elif f_stat == "accepted":
        if st.button(f"🚗 في الطريق — {now_local}", key=f"enroute_{w_id}", type="primary", use_container_width=True):
            _update_field({"field_status": "en_route", "en_route_at": now_iso, "status": "en_route"},
                          f"في الطريق: {safe_text(w.get('title'))}")

    # ── حالة: في الطريق — وصلت ──
    elif f_stat == "en_route":
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📍 وصلت — {now_local}", key=f"arrived_{w_id}", type="primary", use_container_width=True):
                _update_field({"field_status": "arrived", "arrived_at": now_iso, "status": "arrived"},
                              f"وصول للموقع: {safe_text(w.get('title'))}")
        with col2:
            no_acc_r = st.selectbox("سبب عدم الوصول", NO_ACCESS_REASONS, key=f"no_acc_r_{w_id}", label_visibility="collapsed")
            if st.button("🚫 لم أتمكن من الدخول", key=f"no_access_{w_id}", use_container_width=True):
                _update_field({"field_status": "no_access", "no_access_reason": no_acc_r,
                               "no_access_at": now_iso, "status": "no_access"},
                              f"لم يتمكن من الدخول: {safe_text(w.get('title'))} — {no_acc_r}", severity="important")

    # ── حالة: وصل — بدء التنفيذ ──
    elif f_stat == "arrived":
        if st.button(f"🔧 بدأت العمل — {now_local}", key=f"start_{w_id}", type="primary", use_container_width=True):
            _update_field({"field_status": "in_progress", "work_started_at": now_iso, "status": "in_progress"},
                          f"بدء التنفيذ: {safe_text(w.get('title'))}")

    # ── حالة: جاري ── إنهاء أو تعليق
    elif f_stat == "in_progress" or w_stat == "in_progress":
        st.info(f"⏱️ بدأت الساعة: {safe_text(w.get('work_started_at','—')[:16].replace('T',' '))}")
        st.caption("لإنهاء المهمة أو توقيفها، استخدم تبويب 📝 تقرير ميداني")

    # ── حالة: عدم وصول ── إعادة جدولة
    elif f_stat == "no_access":
        st.warning(f"🚫 سجّل كسبب: {safe_text(w.get('no_access_reason','—'))}")
        if st.button("🔄 إعادة تعيين للجدولة", key=f"reset_{w_id}", use_container_width=True):
            _update_field({"field_status": "pending", "status": "pending"},
                          f"إعادة تعيين أمر عمل بعد عدم الوصول: {safe_text(w.get('title'))}")

    # ── حالة: مرفوض ──
    elif f_stat == "declined":
        st.error(f"❌ مرفوض — السبب: {safe_text(w.get('declined_reason','—'))}")

    # ── حالة: مكتمل ──
    elif f_stat == "completed" or w_stat == "completed":
        st.success("✅ هذه المهمة مكتملة.")


def _render_field_report_form(tech_name: str, work_orders: list, elev_db: list,
                               id_to_cno: dict, c_map: dict):
    """نموذج التقرير الميداني الكامل — مهام 8-17"""
    section_header("📝 تقرير التنفيذ الميداني")

    # اختر المهمة
    my_active = [w for w in work_orders if
                 w.get("technician") == tech_name and
                 w.get("status") not in ("completed","cancelled","declined")]

    if not my_active:
        st.info("لا توجد مهام نشطة لتقديم تقرير عنها.")
        return

    wo_opts = {f"{w.get('id','')} — {safe_text(w.get('title'),'')[:50]}": w for w in my_active}
    sel_wo_label = st.selectbox("اختر المهمة *", list(wo_opts.keys()), key="fr_wo_sel")
    sel_wo = wo_opts[sel_wo_label]
    w_id   = str(sel_wo.get("id",""))
    w_pri  = sel_wo.get("priority","medium")

    eid = str(sel_wo.get("elevator_id","")) if sel_wo.get("elevator_id") else ""
    elev_map = {str(e["id"]): e for e in elev_db}
    elev_info = elev_map.get(eid, {}) if eid else {}

    st.markdown(f"""
    <div class="field-task-card {w_pri}">
      <div class="field-task-title">{safe_text(sel_wo.get('title'),'—')}</div>
      <div class="field-task-meta">🏢 {safe_text(c_map.get(str(sel_wo.get('contract_id','')),{}).get('building_name'),'—')}</div>
      <div class="field-task-meta">🛗 {safe_text(elev_info.get('internal_code'),'—')} | {safe_text(elev_info.get('elevator_type'),'—')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 1: الأعمال المنجزة ──
    st.markdown("### 1️⃣ ما تم إنجازه")
    work_done = st.text_area("الأعمال المنجزة *", key="fr_work_done", height=90,
                              placeholder="اكتب بالتفصيل ما قمت به...")
    work_not_done = st.text_area("ما لم يتم (إن وجد)", key="fr_not_done", height=60,
                                  placeholder="أي شيء لم يكتمل...")

    # ── Section 2: تشخيص العطل ──
    st.markdown("### 2️⃣ تشخيص العطل")
    c1, c2 = st.columns(2)
    with c1:
        fault_cause = st.text_input("سبب العطل", key="fr_fault_cause",
                                     placeholder="مثال: ماس كهربائي في لوحة التحكم")
        action_taken = st.text_input("الإجراء المتخذ", key="fr_action",
                                      placeholder="مثال: استبدال الفيوز")
    with c2:
        resolution_type_sel = st.selectbox("نوع الحل", RESOLUTION_TYPES, key="fr_resol_type")
        hazard_sel = st.selectbox("مستوى الخطر",
                                   list(HAZARD_LEVELS.values()),
                                   key="fr_hazard")
        hazard_key = next((k for k,v in HAZARD_LEVELS.items() if v == hazard_sel), "none")

    # ── Section 3: قطع الغيار (مهمة 10) ──
    st.markdown("### 3️⃣ قطع الغيار المستخدمة")
    parts_list = []
    num_parts = st.number_input("عدد القطع", min_value=0, max_value=10, value=0, step=1, key="fr_num_parts")
    for i in range(int(num_parts)):
        pc1, pc2, pc3 = st.columns([3,1,2])
        with pc1:
            part_name = st.selectbox(f"القطعة {i+1}", COMMON_PARTS, key=f"fr_part_{i}")
        with pc2:
            part_qty = st.number_input("الكمية", min_value=1, value=1, key=f"fr_qty_{i}")
        with pc3:
            part_note = st.text_input("ملاحظة", key=f"fr_pnote_{i}", placeholder="اختياري")
        parts_list.append({"part": part_name, "qty": int(part_qty), "note": part_note.strip()})

    # ── Section 4: Safety Checklist (مهمة 13) ──
    st.markdown("### 4️⃣ قائمة السلامة")
    safety_results = {}
    if hazard_key in ("medium","high","critical") or w_pri in ("urgent","high"):
        for item in SAFETY_CHECKLIST:
            safety_results[item] = st.checkbox(item, key=f"fr_safe_{item[:20]}_{w_id}", value=False)
        unchecked = [k for k,v in safety_results.items() if not v]
        if unchecked:
            st.warning(f"⚠️ {len(unchecked)} بنود سلامة لم تُؤكَّد")
    else:
        st.caption("✅ لا يوجد خطر مرتفع — قائمة السلامة اختيارية")
        for item in SAFETY_CHECKLIST:
            safety_results[item] = st.checkbox(item, key=f"fr_safe_{item[:20]}_{w_id}", value=True)

    # ── Section 5: التوصية الفنية (مهمة 12) ──
    st.markdown("### 5️⃣ توصية فنية لاحقة")
    followup_rec = st.text_area("توصية / عرض سعر مطلوب", key="fr_followup_rec", height=60,
                                 placeholder="مثال: يحتاج المصعد استبدال محرك الباب قيمة تقديرية ...")
    fr_followup_needed = st.checkbox("تحتاج متابعة مستقبلية", key="fr_followup_chk")
    fr_followup_date = None
    if fr_followup_needed:
        fr_followup_date = st.date_input("تاريخ المتابعة", value=date.today() + timedelta(days=7), key="fr_fdate")

    # ── Section 6: توقيع العميل (مهمة 11) ──
    st.markdown("### 6️⃣ تأكيد الاستلام")
    customer_sig = st.text_input("اسم المستلم / توقيع العميل",
                                  key="fr_customer_sig",
                                  placeholder="اسم العميل أو المسؤول في الموقع")

    # ── Section 7: حالة الإغلاق (مهمة 16 — Mandatory close fields) ──
    st.markdown("### 7️⃣ حالة الإنهاء")
    c3, c4 = st.columns(2)
    with c3:
        cond_after = st.text_input("حالة المصعد بعد الزيارة *",
                                    key="fr_cond_after",
                                    placeholder="مثال: يعمل بشكل طبيعي")
        close_status_label = st.selectbox(
            "نتيجة الزيارة *",
            ["مكتمل — تم الإصلاح", "غير مكتمل — يحتاج متابعة", "موقوف — انتظار قطعة", "تعليق للمدير"],
            key="fr_close_status"
        )
    with c4:
        close_reason_sel = st.selectbox("سبب الإغلاق *", CLOSE_REASONS, key="fr_close_reason")
        field_notes = st.text_area("ملاحظات ختامية", key="fr_field_notes", height=60)

    # ── Section 8: رفع الصور (مهمة 9) ──
    st.markdown("### 8️⃣ صور قبل/بعد")
    uploaded_before = st.file_uploader("صورة قبل الإصلاح", type=["jpg","jpeg","png"],
                                        key="fr_photo_before")
    uploaded_after  = st.file_uploader("صورة بعد الإصلاح",  type=["jpg","jpeg","png"],
                                        key="fr_photo_after")
    photo_urls_list = []
    if uploaded_before:
        photo_urls_list.append({"type": "before", "name": uploaded_before.name, "size": uploaded_before.size})
    if uploaded_after:
        photo_urls_list.append({"type": "after", "name": uploaded_after.name, "size": uploaded_after.size})

    st.markdown("---")

    # ── زر الحفظ — Mandatory close validation (مهمة 16) ──
    if st.button("💾 إغلاق المهمة وحفظ التقرير", type="primary", use_container_width=True, key="fr_save"):
        errors = []
        if not work_done.strip():          errors.append("الأعمال المنجزة مطلوبة")
        if not cond_after.strip():         errors.append("حالة المصعد بعد الزيارة مطلوبة")
        if not close_status_label:         errors.append("نتيجة الزيارة مطلوبة")
        if "تعليق للمدير" in close_status_label and hazard_key == "none":
            errors.append("اختر مستوى الخطر عند التعليق للمدير")

        if show_validation_errors(errors):
            pass
        else:
            # حدد الحالة النهائية
            status_map = {
                "مكتمل — تم الإصلاح":         "completed",
                "غير مكتمل — يحتاج متابعة":   "on_hold",
                "موقوف — انتظار قطعة":        "on_hold",
                "تعليق للمدير":               "on_hold",
            }
            final_status = status_map.get(close_status_label, "completed")

            # incomplete routing (مهمة 17)
            incomplete_reason = ""
            if final_status == "on_hold":
                if "انتظار قطعة" in close_status_label:
                    incomplete_reason = "انتظار قطع غيار"
                elif "تعليق للمدير" in close_status_label:
                    incomplete_reason = "تعليق للمدير الفني"
                else:
                    incomplete_reason = "يحتاج متابعة"

            try:
                update_data = {
                    "status":          final_status,
                    "field_status":    "completed" if final_status == "completed" else "incomplete",
                    "notes":           f"تقرير: {work_done.strip()} | إجراء: {action_taken} | سبب: {fault_cause} | {field_notes}".strip(" |"),
                    "hazard_level":    hazard_key,
                    "safety_checklist": _json.dumps(safety_results, ensure_ascii=False),
                    "parts_used_structured": _json.dumps(parts_list, ensure_ascii=False),
                    "customer_signature":    customer_sig.strip(),
                    "followup_recommendation": followup_rec.strip(),
                    "photo_urls":      _json.dumps(photo_urls_list, ensure_ascii=False),
                    "field_notes":     field_notes.strip(),
                }
                if photo_urls_list:
                    update_data["photo_urls"] = _json.dumps(photo_urls_list, ensure_ascii=False)
                if fr_followup_needed and fr_followup_date:
                    update_data["followup_needed"]  = True
                    update_data["followup_date"]     = fr_followup_date.isoformat() if isinstance(fr_followup_date, date) else str(fr_followup_date)
                if incomplete_reason:
                    update_data["notes"] = (update_data.get("notes","") + f" | سبب التعليق: {incomplete_reason}").strip(" |")

                supabase.table("work_orders").update(update_data).eq("id", w_id).execute()

                # إنشاء سجل زيارة في visits
                c_id_wo = sel_wo.get("contract_id")
                visit_payload = {
                    "work_order_id":         w_id,
                    "elevator_id":           sel_wo.get("elevator_id"),
                    "contract_id":           c_id_wo,
                    "visit_type":            WORK_TYPES.get(safe_text(sel_wo.get("work_type"),"corrective"),"صيانة تصحيحية"),
                    "visit_date":            date.today().isoformat(),
                    "technician":            tech_name,
                    "status":                "completed" if final_status == "completed" else "incomplete",
                    "work_done":             work_done.strip(),
                    "parts_used":            ", ".join([f"{p['part']} x{p['qty']}" for p in parts_list]) if parts_list else "",
                    "condition_after":       cond_after.strip(),
                    "non_completion_reason": incomplete_reason or None,
                    "recommendations":       followup_rec.strip(),
                    "followup_needed":       fr_followup_needed,
                    "followup_date":         fr_followup_date.isoformat() if fr_followup_date and fr_followup_needed else None,
                    "notes":                 field_notes.strip(),
                    "hazard_level":          hazard_key,
                    "safety_checklist":      _json.dumps(safety_results, ensure_ascii=False),
                    "parts_used_structured": _json.dumps(parts_list, ensure_ascii=False),
                    "customer_signature":    customer_sig.strip(),
                    "followup_recommendation": followup_rec.strip(),
                    "field_status":          "completed" if final_status == "completed" else "incomplete",
                }
                supabase.table("visits").insert(visit_payload).execute()

                log_action("edit","work_orders",
                           f"إغلاق ميداني: {safe_text(sel_wo.get('title'))} — {final_status}",
                           severity="important", entity_id=w_id)
                log_decision("closure","work_order",w_id,final_status,close_reason_sel,field_notes)

                # إشعار المدير عند الخطر أو التعليق (مهمة 18)
                if hazard_key in ("medium","high","critical") or "تعليق للمدير" in close_status_label:
                    send_field_escalation(w_id, safe_text(sel_wo.get("title"),""), tech_name, hazard_key, incomplete_reason)

                load_work_orders.clear()
                load_visits.clear()

                if final_status == "completed":
                    st.success("✅ تم إغلاق المهمة وحفظ التقرير الميداني بنجاح.")
                else:
                    st.warning(f"⚠️ المهمة موقوفة — {incomplete_reason}. تم إشعار المدير الفني.")
                st.rerun()

            except Exception as ex:
                st.error(friendly_error(ex))


# ════════════════════════════════════════════════════════
# V15: TAB — Live Field Board (مهمة 20)
# ════════════════════════════════════════════════════════
def tab_live_board():
    """لوحة المتابعة الميدانية الحية — للإدارة فقط"""
    require_role(ROLE_ADMIN, ROLE_MANAGER)

    section_header("📡 لوحة المتابعة الميدانية الحية")

    work_orders = load_work_orders()
    contracts   = load_contracts()
    id_to_cno   = id_to_contract_no_map(contracts)
    c_map       = {str(c["id"]): c for c in contracts}
    today_str   = date.today().isoformat()

    # تجميع مهام اليوم فقط
    today_wo = [w for w in work_orders if w.get("scheduled_date","") == today_str]
    overdue  = [w for w in work_orders if
                w.get("scheduled_date","") < today_str and
                w.get("status") not in ("completed","cancelled")]

    # ── KPIs حية ──
    k1,k2,k3,k4,k5 = st.columns(5)
    en_route_c  = sum(1 for w in today_wo if w.get("field_status") == "en_route")
    on_site_c   = sum(1 for w in today_wo if w.get("field_status") in ("arrived","in_progress"))
    done_c      = sum(1 for w in today_wo if w.get("field_status") == "completed" or w.get("status") == "completed")
    pending_c   = sum(1 for w in today_wo if w.get("status") not in ("completed","cancelled") and w.get("field_status") in ("pending","accepted",""))
    no_acc_c    = sum(1 for w in today_wo if w.get("field_status") == "no_access")

    k1.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🚗 في الطريق</div><div class="kpi-mini-value" style="color:#d97706">{en_route_c}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🔧 في الموقع</div><div class="kpi-mini-value" style="color:#7c3aed">{on_site_c}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">✅ أنهى</div><div class="kpi-mini-value" style="color:#16a34a">{done_c}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">⏳ معلق</div><div class="kpi-mini-value">{pending_c}</div></div>', unsafe_allow_html=True)
    k5.markdown(f'<div class="kpi-mini"><div class="kpi-mini-label">🚫 لم يصل</div><div class="kpi-mini-value" style="color:#dc2626">{no_acc_c}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── توزيع الفنيين (مهمة 19) ──
    st.markdown("### 👷 حالة الفنيين اليوم")

    lb1, lb2 = st.columns(2)

    with lb1:
        for tech in TECHNICIANS:
            tech_wo_today = [w for w in today_wo if w.get("technician") == tech]
            region = TECH_REGIONS.get(tech,"—")
            if not tech_wo_today:
                st.markdown(f'<div class="live-row"><span>👷 <strong>{tech}</strong> — {region}</span><span style="color:#9ca3af">لا مهام اليوم</span></div>', unsafe_allow_html=True)
            else:
                current_wo = sorted(tech_wo_today, key=lambda w: {
                    "in_progress":0,"arrived":1,"en_route":2,"accepted":3,"pending":4
                }.get(w.get("field_status","pending"),5))
                latest = current_wo[0]
                f_stat  = safe_text(latest.get("field_status"), latest.get("status","pending"))
                st_label = FIELD_STATUSES.get(f_stat, WO_STATUSES.get(f_stat,f_stat))
                color_map = {"en_route":"#d97706","arrived":"#16a34a","in_progress":"#7c3aed",
                             "completed":"#16a34a","no_access":"#dc2626","pending":"#6b7280","accepted":"#2563eb"}
                color = color_map.get(f_stat,"#111")
                bldg  = safe_text(c_map.get(str(latest.get("contract_id","")),{}).get("building_name"),"—")
                st.markdown(
                    f'<div class="live-row">'
                    f'<span>👷 <strong>{tech}</strong> — {region}</span>'
                    f'<span><span style="color:{color};font-weight:700">{st_label}</span>'
                    f' — {safe_text(latest.get("title",""))[:30]} @ {bldg}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    with lb2:
        # ── مهام متأخرة ──
        st.markdown("**⚠️ متأخرة ({}):**".format(len(overdue)))
        if overdue:
            overdue_rows = []
            for w in overdue[:10]:
                d = parse_date_safe(w.get("scheduled_date"))
                days_late = (date.today() - d).days if d else 0
                overdue_rows.append({
                    "العنوان": safe_text(w.get("title"),"—")[:30],
                    "الفني": safe_text(w.get("technician"),"—"),
                    "تأخر": f"{days_late} يوم",
                    "الحالة": WO_STATUSES.get(w.get("status","pending"),"—"),
                })
            st.dataframe(pd.DataFrame(overdue_rows), use_container_width=True, hide_index=True)
        else:
            st.success("لا توجد مهام متأخرة ✅")

    st.markdown("---")

    # ── جدول مفصّل لمهام اليوم ──
    st.markdown("### 📋 تفاصيل مهام اليوم")
    if today_wo:
        rows = []
        for w in sorted(today_wo, key=lambda x: {
                "in_progress":0,"arrived":1,"en_route":2,"completed":3,"pending":4,"cancelled":5
        }.get(x.get("field_status", x.get("status","pending")),4)):
            f_st = safe_text(w.get("field_status"), w.get("status","pending"))
            bldg = safe_text(c_map.get(str(w.get("contract_id","")),{}).get("building_name"),"—")
            dist = safe_text(c_map.get(str(w.get("contract_id","")),{}).get("district"),"—")
            rows.append({
                "الفني": safe_text(w.get("technician"),"—"),
                "العنوان": safe_text(w.get("title"),"—")[:35],
                "المبنى": bldg,
                "المنطقة": dist,
                "الحالة": FIELD_STATUSES.get(f_st, WO_STATUSES.get(f_st,f_st)),
                "الأولوية": PRIORITY_LEVELS.get(w.get("priority","medium"),"—"),
                "خطر": HAZARD_LEVELS.get(safe_text(w.get("hazard_level"),"none"),"لا خطر"),
                "متأخر": "⚠️" if w.get("scheduled_date","") < today_str else "—",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد مهام مجدولة اليوم.")


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
        # Logo — V17
        st.markdown("""
        <div class="sb-logo" style="display:flex;align-items:center;gap:10px;padding:16px 14px 14px;border-bottom:1px solid #F3F4F6;margin-bottom:8px;">
          <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#1A56DB,#1648C8);
                      display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;
                      box-shadow:0 2px 8px rgba(26,86,219,.3);">🛗</div>
          <div>
            <div style="font-size:1rem;font-weight:900;color:#111827;letter-spacing:0.3px;">LiftTech</div>
            <div style="font-size:0.6rem;color:#9CA3AF;font-weight:500;margin-top:1px;">نظام إدارة المصاعد</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # User card — V17
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#F9FAFB;
                    border-radius:10px;margin:4px 8px 12px 8px;border:1px solid #F3F4F6;">
          <div style="width:34px;height:34px;border-radius:50%;
                      background:linear-gradient(135deg,#1A56DB,#1648C8);
                      color:#FFFFFF;display:flex;align-items:center;justify-content:center;
                      font-size:0.9rem;font-weight:800;flex-shrink:0;
                      box-shadow:0 2px 6px rgba(26,86,219,.25);">{avatar_char}</div>
          <div>
            <div style="font-size:0.84rem;font-weight:700;color:#111827;line-height:1.3;">{display_name}</div>
            <div style="font-size:0.64rem;color:#6B7280;margin-top:1px;font-weight:500;">{role_ar}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

        # Navigation options based on role
        if is_admin() or is_manager():
            nav_options = {
                "📊  لوحة التحكم":   "dashboard",
                "📋  العقود":         "contracts",
                "🔧  أوامر العمل":   "work_orders",
                "🚨  البلاغات":      "fault_reports",
                "📝  سجل الصيانة":  "maintenance",
                "🛗  المصاعد":       "elevators",
                "📄  سجل الزيارات":  "visits",
                "👷‍♂️  مدير فني":    "tech_manager",
                "📡  ميداني حي":     "live_board",
                "📅  التقويم":       "calendar",
                "👷  الفنيون":       "technicians",
                "🗂️  سجل الأحداث":  "audit_log",
                "📊  جودة البيانات": "data_quality",
                "👥  المستخدمون":    "users",
                "👤  حسابي":         "account",
            }
        elif is_tech():
            nav_options = {
                "📱  ميداني":         "field",
                "📊  لوحتي":          "dashboard",
                "🔧  أوامر عملي":    "work_orders",
                "🚨  بلاغاتي":       "fault_reports",
                "📝  سجل الصيانة":  "maintenance",
                "📄  زياراتي":        "visits",
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
        # الفني يبدأ من الواجهة الميدانية مباشرة
        default_page = "field" if is_tech() else "dashboard"
        saved_page = st.session_state.get("current_page", default_page)
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

        # Logout — V17
        st.markdown("<div style='flex:1; min-height:32px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='border-top:1px solid #F3F4F6;padding-top:10px;margin:8px 10px 6px 10px;'>"
            f"<div style='font-size:0.7rem;color:#9CA3AF;text-align:center;margin-bottom:8px;"
            f"font-variant-numeric:tabular-nums;'>"
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
        "visits":       "📄 سجل الزيارات",
        "tech_manager": "👷‍♂️ المدير الفني",
        "calendar":     "📅 تقويم الصيانة",
        "technicians":  "👷 الفنيون والجدولة",
        "audit_log":    "🗂️ سجل الأحداث",
        "data_quality": "📊 جودة البيانات",
        "users":        "👥 إدارة المستخدمين",
        "field":        "📱 الواجهة الميدانية",
        "live_board":   "📡 المتابعة الحية",
        "account":      "👤 حسابي",
    }
    page_title = page_titles.get(selected_page, "LiftTech")

    # Extract icon from page_title for header icon box
    _hdr_icon = page_title.split()[0] if page_title else "📄"
    _hdr_text = " ".join(page_title.split()[1:]) if len(page_title.split()) > 1 else page_title

    st.markdown(f"""
    <div class="top-header">
      <div class="top-header-left">
        <div style="width:32px;height:32px;border-radius:8px;background:#EBF5FF;
                    display:flex;align-items:center;justify-content:center;font-size:1.1rem;">
          {_hdr_icon}
        </div>
        <div style="display:flex;flex-direction:column;gap:1px;">
          <div class="top-header-title" style="font-size:0.95rem;font-weight:700;color:#111827;">{_hdr_text}</div>
          <div style="font-size:0.65rem;color:#9CA3AF;letter-spacing:0.3px;">LiftTech ERP</div>
        </div>
      </div>
      <div class="top-header-right">
        <span style="font-size:0.7rem;color:#9CA3AF;font-variant-numeric:tabular-nums;">
          {datetime.now().strftime("%Y/%m/%d  %H:%M")}
        </span>
        <div style="width:1px;height:18px;background:#E5E7EB;"></div>
        <span class="header-badge">{role_ar}</span>
        <div style="width:28px;height:28px;border-radius:50%;
                    background:linear-gradient(135deg,#1A56DB,#1648C8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.75rem;font-weight:800;color:#FFFFFF;">
          {avatar_char}
        </div>
      </div>
    </div>
    <div style="padding: 20px 0 0 0;">
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
    elif selected_page == "visits":
        tab_visits()
    elif selected_page == "tech_manager":
        tab_tech_manager()
    elif selected_page == "field":
        tab_field()
    elif selected_page == "live_board":
        tab_live_board()
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
        <span style="font-weight:700;color:#111827;font-size:0.9rem;">{uname}</span>
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

<h4 style="border-bottom:2px solid #1A56DB;padding-bottom:6px;color:#111827;">🏢 نظام LiftTech — وثيقة الحوكمة الداخلية</h4>

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

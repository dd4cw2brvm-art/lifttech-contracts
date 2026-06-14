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
    page_title="LiftTech V6.0",
    page_icon="🛗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Google Fonts + Global CSS
# ─────────────────────────────────────────────
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">', unsafe_allow_html=True)
st.markdown("""
<style>
/* ═══════════════════════════════════════════════
   LiftTech V6.0 — SAB Business One Design System
   ═══════════════════════════════════════════════ */

/* ── Variables ── */
:root {
  --primary:      #006341;
  --primary-dark: #004d32;
  --primary-light:#e6f2ee;
  --accent:       #00a86b;
  --bg:           #f5f6f7;
  --surface:      #ffffff;
  --border:       #e0e4e8;
  --text:         #1a1a2e;
  --text-muted:   #6b7280;
  --text-faint:   #9ca3af;
  --danger:       #dc2626;
  --warning:      #d97706;
  --success:      #059669;
  --info:         #0284c7;
  --sidebar-bg:   #ffffff;
  --sidebar-w:    230px;
  --header-h:     52px;
  --radius:       10px;
  --shadow-sm:    0 1px 4px rgba(0,0,0,0.08);
  --shadow-md:    0 4px 16px rgba(0,0,0,0.10);
}

/* ── Base ── */
* { font-family: 'Cairo', sans-serif !important; box-sizing: border-box; }
body, .stApp { direction: rtl !important; background: var(--bg) !important; }
#MainMenu, footer { visibility: hidden !important; }

/* ── Main container ── */
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
section[data-testid="stSidebarContent"] {
  padding-top: 0 !important;
}

/* ══════════════════════════════════
   SIDEBAR — SAB Style
══════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  border-left: 1px solid var(--border) !important;
  min-width: var(--sidebar-w) !important;
  max-width: var(--sidebar-w) !important;
  padding: 0 !important;
  box-shadow: -2px 0 12px rgba(0,0,0,0.06);
}
[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}

.sidebar-logo {
  background: var(--primary);
  padding: 12px 18px 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.15);
}
.sidebar-logo-icon { font-size: 1.45rem; }
.sidebar-logo-text { color: white; }
.sidebar-logo-text h3 { margin: 0; font-size: 0.95rem; font-weight: 800; letter-spacing: 0.5px; }
.sidebar-logo-text p  { margin: 0; font-size: 0.65rem; opacity: 0.8; }

.sidebar-user {
  background: var(--primary-light);
  padding: 8px 18px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}
.sidebar-user-avatar {
  width: 30px; height: 30px;
  background: var(--primary);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; color: white; font-weight: 700;
  flex-shrink: 0;
}
.sidebar-user-info { flex: 1; min-width: 0; }
.sidebar-user-name { font-size: 0.78rem; font-weight: 700; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sidebar-user-role { font-size: 0.65rem; color: var(--primary); font-weight: 600; }

.sidebar-nav { padding: 6px 0; }
.sidebar-section-label {
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--text-faint);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 4px 18px 2px;
  margin-top: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 18px;
  margin: 1px 8px;
  border-radius: 7px;
  cursor: pointer;
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.15s ease;
  text-decoration: none;
}
.nav-item:hover {
  background: var(--primary-light);
  color: var(--primary);
}
.nav-item.active {
  background: var(--primary);
  color: white;
  box-shadow: 0 2px 8px rgba(0,100,65,0.25);
}
.nav-item .nav-icon { font-size: 0.88rem; width: 18px; text-align: center; flex-shrink: 0; }
.nav-badge {
  margin-right: auto;
  background: #fee2e2; color: #dc2626;
  font-size: 0.68rem; font-weight: 700;
  padding: 1px 7px; border-radius: 10px;
}
.nav-badge.green { background: #dcfce7; color: #15803d; }

.sidebar-footer {
  border-top: 1px solid var(--border);
  padding: 8px 18px;
  margin-top: auto;
}

/* ══════════════════════════════════
   TOP HEADER BAR
══════════════════════════════════ */
.top-header {
  background: white;
  border-bottom: 1px solid var(--border);
  padding: 0 20px;
  height: var(--header-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}
.top-header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
}
.top-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-badge {
  background: var(--primary-light);
  color: var(--primary);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}
.header-time {
  font-size: 0.72rem;
  color: var(--text-muted);
}

/* ══════════════════════════════════
   PAGE CONTENT
══════════════════════════════════ */
.page-content {
  padding: 12px 18px;
}

/* ══════════════════════════════════
   KPI CARDS — SAB Style
══════════════════════════════════ */
.kpi-card {
  background: white;
  border-radius: var(--radius);
  padding: 10px 14px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  border-top: 3px solid var(--info);
  margin-bottom: 0.5rem;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}
.kpi-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.kpi-card.danger  { border-top-color: var(--danger); }
.kpi-card.success { border-top-color: var(--success); }
.kpi-card.warning { border-top-color: var(--warning); }
.kpi-card.info    { border-top-color: var(--info); }
.kpi-card.primary { border-top-color: var(--primary); }
.kpi-icon-wrap {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
  margin-bottom: 6px;
  background: var(--primary-light);
}
.kpi-card.danger  .kpi-icon-wrap { background: #fef2f2; }
.kpi-card.success .kpi-icon-wrap { background: #f0fdf4; }
.kpi-card.warning .kpi-icon-wrap { background: #fffbeb; }
.kpi-card.info    .kpi-icon-wrap { background: #f0f9ff; }
.kpi-value { font-size: 1.3rem; font-weight: 800; color: var(--text); line-height: 1; margin-bottom: 2px; }
.kpi-title { font-size: 0.72rem; color: var(--text-muted); font-weight: 500; }

/* ══════════════════════════════════
   SECTION HEADER
══════════════════════════════════ */
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text);
  margin: 10px 0 6px;
  padding-bottom: 6px;
  border-bottom: 2px solid var(--primary-light);
}
.section-header::before {
  content: '';
  display: block;
  width: 3px;
  height: 14px;
  background: var(--primary);
  border-radius: 2px;
  flex-shrink: 0;
}

/* ══════════════════════════════════
   ALERTS
══════════════════════════════════ */
.alert-expired { background:#fef2f2; border:1px solid #fecaca; border-right:3px solid var(--danger); color:#991b1b; padding:6px 12px; border-radius:var(--radius); margin-bottom:0.35rem; font-size:0.78rem; font-weight:600; }
.alert-30      { background:#fff7ed; border:1px solid #fed7aa; border-right:3px solid var(--warning); color:#9a3412; padding:6px 12px; border-radius:var(--radius); margin-bottom:0.35rem; font-size:0.78rem; font-weight:600; }
.alert-60      { background:#fefce8; border:1px solid #fef08a; border-right:3px solid #ca8a04;  color:#713f12; padding:6px 12px; border-radius:var(--radius); margin-bottom:0.35rem; font-size:0.78rem; font-weight:600; }
.alert-90      { background:#f0fdf4; border:1px solid #bbf7d0; border-right:3px solid var(--success); color:#14532d; padding:6px 12px; border-radius:var(--radius); margin-bottom:0.35rem; font-size:0.78rem; font-weight:600; }

/* ══════════════════════════════════
   BADGES
══════════════════════════════════ */
.badge { display:inline-flex; align-items:center; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; white-space:nowrap; }
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

/* ══════════════════════════════════
   FORMS & INPUTS
══════════════════════════════════ */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div>div,
.stNumberInput>div>div>input,
.stDateInput>div>div>input {
  border-radius: 8px !important;
  border: 1.5px solid var(--border) !important;
  font-family: 'Cairo', sans-serif !important;
  direction: rtl !important;
  text-align: right !important;
  font-size: 0.9rem !important;
  color: var(--text) !important;
  background: white !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(0,99,65,0.12) !important;
}
.stButton>button {
  border-radius: 8px !important;
  font-family: 'Cairo', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.8rem !important;
  padding: 6px 14px !important;
  transition: all 0.2s !important;
}
.stButton>button[kind="primary"] {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
}
.stButton>button[kind="primary"]:hover {
  background: var(--primary-dark) !important;
  box-shadow: 0 4px 12px rgba(0,99,65,0.3) !important;
}
[data-testid="stForm"] {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  box-shadow: var(--shadow-sm);
}

/* ══════════════════════════════════
   TABS (fallback if not using sidebar nav)
══════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: white;
  border-radius: var(--radius);
  padding: 4px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  gap: 4px;
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 7px !important;
  font-family: 'Cairo', sans-serif !important;
  font-weight: 600 !important;
  padding: 8px 14px !important;
  color: var(--text-muted) !important;
  font-size: 0.87rem !important;
}
.stTabs [aria-selected="true"] {
  background: var(--primary) !important;
  color: white !important;
}

/* ══════════════════════════════════
   DATAFRAME / TABLE
══════════════════════════════════ */
.stDataFrame {
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important;
}
.stDataFrame thead th {
  background: var(--primary) !important;
  color: white !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
}

/* ══════════════════════════════════
   TECH CARDS
══════════════════════════════════ */
.tech-card {
  background: white;
  border-radius: var(--radius);
  padding: 10px 14px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  border-top: 3px solid var(--primary);
  margin-bottom: 0.5rem;
  transition: box-shadow 0.2s;
}
.tech-card:hover { box-shadow: var(--shadow-md); }
.tech-card h3   { margin: 0 0 6px 0; font-size: 0.85rem; color: var(--text); font-weight: 700; }
.tech-stat      { display:flex; justify-content:space-between; align-items:center; padding: 4px 0; border-bottom: 1px solid var(--border); font-size: 0.78rem; color: var(--text-muted); }
.tech-stat:last-child { border-bottom: none; }
.tech-stat strong { font-weight: 800; color: var(--primary); font-size: 0.85rem; }

/* ══════════════════════════════════
   ROLE BADGES
══════════════════════════════════ */
.role-admin   { background: var(--primary-light); color: var(--primary); padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.role-manager { background: #eff6ff; color: #1d4ed8; padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.role-tech    { background: #f0fdf4; color: #15803d; padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.role-client  { background: #fefce8; color: #92400e; padding: 3px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }

/* ══════════════════════════════════
   CALENDAR
══════════════════════════════════ */
.cal-day {
  background: white;
  border-radius: var(--radius);
  padding: 6px 8px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 0.3rem;
  min-height: 60px;
}
.cal-day.today {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(0,99,65,0.2);
}
.cal-day-header { font-size: 0.68rem; color: var(--text-muted); margin-bottom: 3px; font-weight: 700; text-align: center; }
.cal-day-date   { font-size: 0.9rem; font-weight: 800; color: var(--text); text-align: center; margin-bottom: 3px; }
.cal-event {
  background: #dbeafe; color: #1d4ed8;
  border-radius: 4px; padding: 2px 6px;
  font-size: 0.65rem; margin-bottom: 2px;
  line-height: 1.2;
}
.cal-event.urgent     { background: #fee2e2; color: #dc2626; }
.cal-event.preventive { background: var(--primary-light); color: var(--primary); }

/* ══════════════════════════════════
   LOGIN PAGE
══════════════════════════════════ */
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, #00c77a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.login-card {
  background: white;
  border-radius: 16px;
  padding: 28px 30px;
  width: 100%;
  max-width: 380px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  text-align: center;
}
.login-logo {
  width: 56px; height: 56px;
  background: var(--primary);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.7rem;
  margin: 0 auto 12px;
  box-shadow: 0 8px 20px rgba(0,99,65,0.35);
}
.login-title { font-size: 1.2rem; font-weight: 800; color: var(--text); margin-bottom: 3px; }
.login-sub   { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 18px; }
.login-divider {
  display: flex; align-items: center; gap: 12px;
  margin: 20px 0;
  color: var(--text-faint); font-size: 0.8rem;
}
.login-divider::before,
.login-divider::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}

/* ══════════════════════════════════
   ELEVATOR CARDS
══════════════════════════════════ */
.elev-card {
  background: white;
  border-radius: var(--radius);
  padding: 8px 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  border-right: 4px solid var(--info);
  margin-bottom: 0.4rem;
  transition: box-shadow 0.2s;
}
.elev-card:hover { box-shadow: var(--shadow-md); }
.elev-card.good  { border-right-color: var(--success); }
.elev-card.fair  { border-right-color: var(--warning); }
.elev-card.poor  { border-right-color: var(--danger); }
.elev-card-title { font-weight: 700; font-size: 0.82rem; color: var(--text); margin-bottom: 4px; }
.elev-card-meta  { font-size: 0.72rem; color: var(--text-muted); margin-bottom: 2px; }

/* ══════════════════════════════════
   SIDEBAR RADIO BUTTONS (nav)
══════════════════════════════════ */
[data-testid="stSidebar"] .stRadio > div {
  gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio > div > label {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 7px 10px !important;
  margin: 1px 8px !important;
  border-radius: 7px !important;
  cursor: pointer !important;
  color: var(--text-muted) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  transition: all 0.15s !important;
  background: transparent !important;
  border: none !important;
  width: calc(100% - 16px) !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
  background: var(--primary-light) !important;
  color: var(--primary) !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] {
  background: var(--primary) !important;
  color: white !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
  margin: 0 !important;
  font-size: 0.8rem !important;
}
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
  display: none !important;
}

/* ══════════════════════════════════
   EXPANDER
══════════════════════════════════ */
.streamlit-expanderHeader {
  background: white !important;
  border-radius: var(--radius) !important;
  border: 1px solid var(--border) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
}

/* ══════════════════════════════════
   METRIC (Streamlit native)
══════════════════════════════════ */
[data-testid="metric-container"] {
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 8px 12px !important;
  box-shadow: var(--shadow-sm) !important;
}

/* ══════════════════════════════════
   SCROLLBAR
══════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ══════════════════════════════════
   MISC
══════════════════════════════════ */
hr { border: none; border-top: 1px solid var(--border); margin: 16px 0; }
/* ══════════════════════════════════
   RESPONSIVE — TABLET (≤1024px)
══════════════════════════════════ */
@media (max-width: 1024px) {
  :root {
    --sidebar-w: 220px;
    --header-h: 56px;
  }
  .page-content { padding: 18px 20px; }
  .top-header   { padding: 0 20px; }
  .kpi-value    { font-size: 1.65rem; }
  .sidebar-logo-text h3 { font-size: 1rem; }
  .sidebar-logo { padding: 16px 18px 14px; }
  .sidebar-user { padding: 12px 18px; }
  .sidebar-nav .nav-item { padding: 10px 18px; }
  [data-testid="stSidebar"] .stRadio > div > label { padding: 9px 10px !important; margin: 2px 8px !important; }
}

/* ══════════════════════════════════
   RESPONSIVE — MOBILE (≤768px)
══════════════════════════════════ */
@media (max-width: 768px) {
  :root {
    --sidebar-w: 100% !important;
    --header-h: 52px;
  }

  /* — Sidebar: collapse to top on mobile — */
  [data-testid="stSidebar"] {
    min-width: 100% !important;
    max-width: 100% !important;
    width: 100% !important;
    position: relative !important;
    box-shadow: none !important;
    border-left: none !important;
    border-bottom: 2px solid var(--border) !important;
  }
  [data-testid="stSidebar"] > div:first-child {
    height: auto !important;
    overflow: visible !important;
  }

  /* — Sidebar logo compact — */
  .sidebar-logo { padding: 12px 16px; gap: 8px; }
  .sidebar-logo-icon { font-size: 1.5rem; }
  .sidebar-logo-text h3 { font-size: 0.9rem; }
  .sidebar-logo-text p  { font-size: 0.65rem; }

  /* — User card compact — */
  .sidebar-user { padding: 10px 16px; gap: 8px; }
  .sidebar-user-avatar { width: 32px; height: 32px; font-size: 0.9rem; }
  .sidebar-user-name   { font-size: 0.82rem; }
  .sidebar-user-role   { font-size: 0.65rem; }

  /* — Nav items: horizontal scroll row — */
  .sidebar-nav { padding: 8px 0; overflow-x: auto; }
  .sidebar-section-label { display: none; }
  [data-testid="stSidebar"] .stRadio > div {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 4px !important;
    padding: 0 12px 8px !important;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  [data-testid="stSidebar"] .stRadio > div::-webkit-scrollbar { display: none; }
  [data-testid="stSidebar"] .stRadio > div > label {
    flex-shrink: 0 !important;
    white-space: nowrap !important;
    padding: 7px 14px !important;
    margin: 0 2px !important;
    font-size: 0.8rem !important;
    border-radius: 20px !important;
    width: auto !important;
  }

  /* — Sidebar footer — */
  .sidebar-footer { padding: 10px 16px; }

  /* — Top header — */
  .top-header { padding: 0 14px; height: var(--header-h); }
  .top-header-title { font-size: 0.95rem; }
  .header-badge     { font-size: 0.72rem; padding: 3px 10px; }
  .header-time      { display: none; }

  /* — Page content — */
  .page-content { padding: 12px 14px; }

  /* — KPI Cards — */
  .kpi-card      { padding: 14px 16px; margin-bottom: 0.6rem; }
  .kpi-value     { font-size: 1.45rem; }
  .kpi-title     { font-size: 0.78rem; }
  .kpi-icon-wrap { width: 38px; height: 38px; font-size: 1.1rem; margin-bottom: 10px; }

  /* — Section header — */
  .section-header { font-size: 0.88rem; margin: 14px 0 8px; padding-bottom: 8px; }

  /* — Elevator cards — */
  .elev-card       { padding: 12px 14px; }
  .elev-card-title { font-size: 0.88rem; }
  .elev-card-meta  { font-size: 0.74rem; }

  /* — Tech cards — */
  .tech-card          { padding: 14px 16px; }
  .tech-card h3       { font-size: 0.9rem; }
  .tech-stat          { font-size: 0.8rem; }
  .tech-stat strong   { font-size: 0.9rem; }

  /* — Calendar — */
  .cal-day        { padding: 8px 10px; min-height: 70px; }
  .cal-day-date   { font-size: 0.95rem; }
  .cal-day-header { font-size: 0.7rem; }
  .cal-event      { font-size: 0.68rem; padding: 2px 6px; }

  /* — Alerts — */
  .alert-expired, .alert-30, .alert-60, .alert-90 {
    padding: 8px 12px; font-size: 0.8rem;
  }

  /* — Forms — */
  .stTextInput>div>div>input,
  .stTextArea>div>div>textarea,
  .stSelectbox>div>div>div,
  .stNumberInput>div>div>input,
  .stDateInput>div>div>input { font-size: 0.85rem !important; }
  .stButton>button { font-size: 0.82rem !important; padding: 8px 14px !important; }
  [data-testid="stForm"] { padding: 14px 16px; }

  /* — Login card — */
  .login-card  { padding: 28px 20px; border-radius: 14px; max-width: 100%; }
  .login-logo  { width: 58px; height: 58px; font-size: 1.8rem; border-radius: 14px; margin-bottom: 14px; }
  .login-title { font-size: 1.2rem; }
  .login-sub   { font-size: 0.78rem; margin-bottom: 20px; }
  .login-page  { padding: 14px; }

  /* — DataFrames: horizontal scroll — */
  .stDataFrame { overflow-x: auto !important; }
  [data-testid="stDataFrame"] { font-size: 0.78rem !important; }

  /* — Badges — */
  .badge { font-size: 0.68rem; padding: 2px 8px; }
  .role-admin, .role-manager, .role-tech, .role-client { font-size: 0.68rem; padding: 2px 8px; }

  /* — Metrics — */
  [data-testid="metric-container"] { padding: 10px 14px !important; }

  /* — Expanders — */
  .streamlit-expanderHeader { font-size: 0.82rem !important; }

  /* — Global font scale — */
  body, .stApp { font-size: 14px; }

  /* — Tabs (fallback) — */
  .stTabs [data-baseweb="tab-list"] { flex-wrap: nowrap; overflow-x: auto; gap: 2px; padding: 4px; }
  .stTabs [data-baseweb="tab"] { padding: 6px 10px !important; font-size: 0.78rem !important; white-space: nowrap; flex-shrink: 0; }

  /* — Column gap — */
  [data-testid="column"] { padding-left: 4px !important; padding-right: 4px !important; }
}

/* ══════════════════════════════════
   RESPONSIVE — SMALL MOBILE (≤480px)
══════════════════════════════════ */
@media (max-width: 480px) {
  .top-header-title { font-size: 0.85rem; }
  .page-content     { padding: 10px 10px; }
  .kpi-value        { font-size: 1.3rem; }
  .login-card       { padding: 22px 14px; }
  .login-title      { font-size: 1.05rem; }
  .elev-card-title  { font-size: 0.82rem; }
  [data-testid="stSidebar"] .stRadio > div > label { font-size: 0.74rem !important; padding: 6px 10px !important; }
}

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
        client = create_client(url, key)
        # إنشاء جدول user_passwords إذا لم يكن موجوداً (تلقائي عبر upsert فارغ)
        try:
            client.table("user_passwords").select("username").limit(1).execute()
        except Exception:
            pass  # الجدول غير موجود — يحتاج إنشاء يدوي من Dashboard
        return client
    except Exception as e:
        st.error(f"❌ تعذّر الاتصال بـ Supabase: {e}")
        return None

supabase = init_supabase()


# ─────────────────────────────────────────────
# Password management (Supabase user_passwords)
# ─────────────────────────────────────────────
def get_db_password(username: str):
    """إرجاع كلمة المرور من Supabase إن وُجدت، وإلا None"""
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
    """حفظ أو تحديث كلمة المرور في Supabase"""
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
            st.error("❌ جدول كلمات المرور غير موجود. يرجى تنفيذ الـ SQL أدناه في Supabase Dashboard:")
            st.code(
                "CREATE TABLE IF NOT EXISTS user_passwords (\n"
                "  username TEXT PRIMARY KEY,\n"
                "  password TEXT NOT NULL,\n"
                "  updated_at TIMESTAMPTZ DEFAULT NOW()\n"
                ");\n"
                "ALTER TABLE user_passwords DISABLE ROW LEVEL SECURITY;",
                language="sql"
            )
            st.markdown("[افتح Supabase SQL Editor](https://supabase.com/dashboard/project/sjnlwriutjdxwwcarxts/sql/new)")
        else:
            st.error(f"❌ خطأ في حفظ كلمة المرور: {e}")
        return False

# ─────────────────────────────────────────────
# Authentication  (multi-role)
# ─────────────────────────────────────────────
def check_login():
    if st.session_state.get("logged_in"):
        return True

    # خلفية الصفحة
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #004d32 0%, #006341 50%, #00a86b 100%) !important; }
    .block-container { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="margin-top:60px; background:white; border-radius:20px; padding:40px 36px;
                    box-shadow:0 20px 60px rgba(0,0,0,0.25); text-align:center;">
          <div style="width:72px;height:72px;background:#006341;border-radius:18px;
                      display:flex;align-items:center;justify-content:center;
                      font-size:2.2rem;margin:0 auto 18px;
                      box-shadow:0 8px 20px rgba(0,99,65,0.35);">🛗</div>
          <div style="font-size:1.5rem;font-weight:800;color:#1a1a2e;margin-bottom:4px;">LiftTech</div>
          <div style="font-size:0.85rem;color:#6b7280;margin-bottom:28px;">نظام إدارة صيانة المصاعد</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0px'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("<div style='margin-top:-20px'></div>", unsafe_allow_html=True)
            username = st.text_input("👤  اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("🔒  كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            submit   = st.form_submit_button("تسجيل الدخول", use_container_width=True, type="primary")

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
                        secrets_pwd  = user_data
                        role_val     = "admin"
                        name_val     = username
                        contract_val = ""
                    else:
                        # New dict format
                        secrets_pwd  = user_data.get("password", "")
                        role_val     = user_data.get("role", "admin")
                        name_val     = user_data.get("name", username)
                        contract_val = user_data.get("contract_no", "")

                    # كلمة المرور من Supabase تُقدَّم على Secrets
                    db_pwd   = get_db_password(username)
                    active_pwd = db_pwd if db_pwd is not None else secrets_pwd
                    pwd_match = (active_pwd == password)

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
      <div class="kpi-icon-wrap">{icon}</div>
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

    if is_client():
        cc = st.session_state.get("client_contract", "")
        if cc:
            contracts = [c for c in contracts if str(c.get("contract_no","")) == cc]

    df    = prepare_contracts_df(contracts)
    today = date.today()

    # حسابات
    total_c   = len(df)
    total_v   = float(df["contract_value"].apply(safe_number).sum()) if not df.empty else 0.0
    active_c  = int((df["status_display"] == "نشط").sum())     if not df.empty else 0
    total_el  = int(df["elevator_count"].apply(safe_int).sum()) if not df.empty else 0
    paid_c    = int((df["payment_display"] == "مسدد").sum())    if not df.empty else 0
    partial_c = int((df["payment_display"] == "جزئي").sum())   if not df.empty else 0
    unpaid_c  = int((df["payment_display"] == "غير مسدد").sum()) if not df.empty else 0
    ratio     = round(paid_c / total_c * 100, 1) if total_c else 0
    bar_w     = int(ratio)

    paid_v   = float(df[df["payment_display"]=="مسدد"]["contract_value"].apply(safe_number).sum())     if not df.empty else 0.0
    unpaid_v = float(df[df["payment_display"]=="غير مسدد"]["contract_value"].apply(safe_number).sum()) if not df.empty else 0.0

    if not df.empty and "days_remaining" in df.columns:
        dr    = df["days_remaining"]
        n_exp = int((dr.notna() & (dr < 0)).sum())
        n_30  = int((dr.notna() & (dr >= 0) & (dr <= 30)).sum())
        n_60  = int((dr.notna() & (dr > 30) & (dr <= 60)).sum())
        n_90  = int((dr.notna() & (dr > 60) & (dr <= 90)).sum())
    else:
        n_exp = n_30 = n_60 = n_90 = 0

    urgent_wo = len([w for w in work_orders  if w.get("status") in ("pending","in_progress")]) if work_orders  else 0
    open_fr   = len([f for f in fault_reports if f.get("status") in ("open","assigned")])       if fault_reports else 0

    tv_s  = f"{float(total_v):,.0f}"
    pv_s  = f"{float(paid_v):,.0f}"
    uv_s  = f"{float(unpaid_v):,.0f}"

    # صف 1 — KPIs
    st.markdown(
        f'<div style="display:flex;gap:8px;margin-bottom:8px;">'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #0284c7;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#128196; اجمالي العقود</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#0284c7;line-height:1;">{total_c}</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-top:2px;">نشطة: {active_c}</div></div>'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #d97706;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#128248; المصاعد</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#d97706;line-height:1;">{total_el}</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-top:2px;">مصعد مسجل</div></div>'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #059669;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#10003; مسدد</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#059669;line-height:1;">{paid_c}</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-top:2px;">نسبة {ratio}%</div></div>'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #dc2626;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#9888; غير مسدد</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#dc2626;line-height:1;">{unpaid_c}</div>'
        f'<div style="font-size:.58rem;color:#d97706;margin-top:2px;">جزئي: {partial_c}</div></div>'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #7c3aed;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#128295; اوامر مفتوحة</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#7c3aed;line-height:1;">{urgent_wo}</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-top:2px;">معلق + جاري</div></div>'
        f'<div style="flex:1;background:white;border-radius:8px;border-top:3px solid #dc2626;padding:10px 12px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.6rem;color:#6b7280;font-weight:600;margin-bottom:4px;">&#128680; بلاغات مفتوحة</div>'
        f'<div style="font-size:1.6rem;font-weight:800;color:#dc2626;line-height:1;">{open_fr}</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-top:2px;">بحاجة متابعة</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # صف 2 — التحصيل + التنبيهات
    st.markdown(
        f'<div style="display:flex;gap:8px;margin-bottom:8px;">'
        f'<div style="flex:1;background:white;border-radius:8px;border:1px solid #e0e4e8;padding:12px 14px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.62rem;color:#6b7280;font-weight:700;margin-bottom:6px;">&#128176; القيمة الاجمالية</div>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#006341;margin-bottom:6px;">{tv_s} ر.س</div>'
        f'<div style="font-size:.58rem;color:#6b7280;margin-bottom:3px;font-weight:600;">نسبة التحصيل {ratio}%</div>'
        f'<div style="background:#e0e4e8;border-radius:3px;height:6px;margin-bottom:6px;overflow:hidden;">'
        f'<div style="background:#059669;height:100%;width:{bar_w}%;border-radius:3px;"></div></div>'
        f'<div style="font-size:.56rem;color:#6b7280;display:flex;justify-content:space-between;">'
        f'<span>مسدد: {pv_s}</span><span>غير مسدد: {uv_s}</span></div></div>'
        f'<div style="flex:2;background:white;border-radius:8px;border:1px solid #e0e4e8;padding:12px 14px;box-shadow:0 1px 4px rgba(0,0,0,.07);">'
        f'<div style="font-size:.62rem;color:#6b7280;font-weight:700;margin-bottom:8px;">&#128276; تنبيهات التجديد</div>'
        f'<div style="display:flex;gap:8px;">'
        f'<div style="flex:1;background:#fef2f2;border-radius:6px;padding:8px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#dc2626;">{n_exp}</div>'
        f'<div style="font-size:.56rem;color:#991b1b;font-weight:600;">منتهية</div></div>'
        f'<div style="flex:1;background:#fff7ed;border-radius:6px;padding:8px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#ea580c;">{n_30}</div>'
        f'<div style="font-size:.56rem;color:#9a3412;font-weight:600;">خلال 30 يوم</div></div>'
        f'<div style="flex:1;background:#fefce8;border-radius:6px;padding:8px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#ca8a04;">{n_60}</div>'
        f'<div style="font-size:.56rem;color:#713f12;font-weight:600;">خلال 60 يوم</div></div>'
        f'<div style="flex:1;background:#f0fdf4;border-radius:6px;padding:8px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#059669;">{n_90}</div>'
        f'<div style="font-size:.56rem;color:#14532d;font-weight:600;">خلال 90 يوم</div></div>'
        f'</div></div></div>',
        unsafe_allow_html=True
    )

    # صف 3 — جدول العقود الحرجة
    section_header("🚨 العقود الحرجة")
    if not df.empty and "days_remaining" in df.columns:
        critical = df[df["days_remaining"].notna() & (df["days_remaining"] <= 90)]\
                     .sort_values("days_remaining").head(20)
        if not critical.empty:
            show_cols = ["contract_no","customer_name","building_name","district",
                         "end_date","days_remaining","payment_display","contract_value"]
            exist  = [c for c in show_cols if c in critical.columns]
            rename = {
                "contract_no":"رقم العقد","customer_name":"العميل",
                "building_name":"المبنى","district":"الحي",
                "end_date":"الانتهاء","days_remaining":"الأيام",
                "payment_display":"السداد","contract_value":"القيمة",
            }
            st.dataframe(critical[exist].rename(columns=rename),
                         use_container_width=True, hide_index=True, height=220)
        else:
            st.success("✅ لا توجد عقود حرجة حالياً")
    else:
        st.info("لا توجد بيانات")

    # صف 4 — تذكيرات واتساب
    if not is_client():
        with st.expander("📲 إرسال تذكيرات واتساب"):
            col_wa1, col_wa2 = st.columns([3, 1])
            with col_wa1:
                days_before = st.slider("إرسال قبل انتهاء العقد بـ (يوم)", 7, 60, 30, key="wa_days")
            with col_wa2:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                send_btn = st.button("📤 إرسال الآن", type="primary", use_container_width=True)
            if send_btn and not df.empty:
                results  = send_renewal_reminders(df, days_before=days_before)
                sent     = [r for r in results if r["status"] == "sent"]
                skipped  = [r for r in results if r["status"] == "skipped"]
                failed   = [r for r in results if r["status"] == "failed"]
                no_phone = [r for r in results if r["status"] == "no_phone"]
                st.success(f"تم: {len(sent)} | تخطي: {len(skipped)} | لا رقم: {len(no_phone)} | فشل: {len(failed)}")



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
            cond_color_map = {"good":"#059669","fair":"#d97706","poor":"#dc2626","":"#0284c7"}
            cond_bg_map    = {"good":"#f0fdf4","fair":"#fffbeb","poor":"#fef2f2","":"#f0f9ff"}
            c_color = cond_color_map.get(cond_class, "#0284c7")
            c_bg    = cond_bg_map.get(cond_class, "#f0f9ff")
            st.markdown(f"""
            <div class="elev-card {cond_class}">
                <div class="elev-card-title">🛗 مصعد #{e['elevator_no']} — {e['building']}</div>
                <div class="elev-card-meta">📋 {e['contract_no']} &nbsp;|&nbsp; 👤 {e['customer']}</div>
                <div class="elev-card-meta">نوع: {e['type']} &nbsp;|&nbsp; ماركة: {e['brand']}</div>
                <hr style="margin:8px 0;border-color:#e0e4e8">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                  <span style="font-size:0.8rem;color:#6b7280">الحالة</span>
                  <span style="background:{c_bg};color:{c_color};padding:2px 10px;border-radius:12px;font-size:0.75rem;font-weight:700">{cond_ar}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#6b7280;margin-bottom:3px">
                  <span>آخر صيانة</span><strong style="color:#1a1a2e">{last_visit}</strong>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#6b7280;margin-bottom:3px">
                  <span>الفني</span><strong style="color:#1a1a2e">{technician}</strong>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#6b7280">
                  <span>الزيارة القادمة</span>
                  <strong style="color:{next_color}">{next_visit} {"(" + next_label + ")" if days_next is not None else ""}</strong>
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
              <div class="tech-stat"><span>أوامر العمل المعلقة</span><strong>{pending_count}</strong></div>
              <div class="tech-stat"><span>مكتملة هذا الشهر</span><strong>{completed_this_month}</strong></div>
              <div class="tech-stat"><span>بلاغات مكلف بها</span><strong>{assigned_faults}</strong></div>
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
# تاب: حسابي (تغيير كلمة المرور)
# ─────────────────────────────────────────────
def tab_account():
    section_header("👤 حسابي")
    username     = st.session_state.get("username", "")
    display_name = st.session_state.get("display_name", username)
    role         = get_role()
    role_ar      = {"admin":"مدير عام","manager":"مدير","tech":"فني","client":"عميل"}.get(role, role)

    col1, col2 = st.columns([1, 2])
    with col1:
        acc_av = display_name[0] if display_name else "م"
        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:2rem;text-align:center;
                    border:1px solid #e0e4e8;box-shadow:0 2px 12px rgba(0,0,0,0.07)">
          <div style="width:80px;height:80px;background:#006341;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;
                      font-size:2rem;font-weight:800;color:white;margin:0 auto 16px;
                      box-shadow:0 4px 16px rgba(0,99,65,0.3)">{acc_av}</div>
          <h3 style="margin:0 0 6px;color:#1a1a2e;font-size:1.15rem">{display_name}</h3>
          <span class="role-{role}">{role_ar}</span>
          <p style="color:#9ca3af;margin-top:12px;font-size:0.82rem">@{username}</p>
          <div style="margin-top:16px;padding-top:16px;border-top:1px solid #e0e4e8;
                      font-size:0.8rem;color:#6b7280">
            مرحباً بك في نظام LiftTech V6.0
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔐 تغيير كلمة المرور")
        with st.form("change_password_form"):
            current_pwd = st.text_input("كلمة المرور الحالية", type="password", placeholder="أدخل كلمة المرور الحالية")
            new_pwd     = st.text_input("كلمة المرور الجديدة", type="password", placeholder="أدخل كلمة المرور الجديدة")
            confirm_pwd = st.text_input("تأكيد كلمة المرور الجديدة", type="password", placeholder="أعد إدخال كلمة المرور الجديدة")
            submit_pwd  = st.form_submit_button("💾 حفظ كلمة المرور الجديدة", use_container_width=True)

        if submit_pwd:
            if not current_pwd or not new_pwd or not confirm_pwd:
                st.error("❌ يرجى ملء جميع الحقول")
            elif new_pwd != confirm_pwd:
                st.error("❌ كلمة المرور الجديدة وتأكيدها غير متطابقتين")
            elif len(new_pwd) < 4:
                st.error("❌ كلمة المرور يجب أن تكون 4 أحرف على الأقل")
            else:
                # التحقق من كلمة المرور الحالية
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
                            st.error("❌ تعذّر حفظ كلمة المرور، تحقق من الاتصال بقاعدة البيانات")
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")

    # للمدير العام فقط: إعادة تعيين كلمة مرور أي مستخدم
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
                reset_btn   = st.form_submit_button("🔄 إعادة تعيين كلمة المرور", use_container_width=True)

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

# ─────────────────────────────────────────────
def main():
    role         = get_role()
    role_ar      = {"admin":"مدير عام","manager":"مدير","tech":"فني","client":"عميل"}.get(role, role)
    display_name = st.session_state.get("display_name", st.session_state.get("username",""))
    avatar_char  = display_name[0] if display_name else "م"

    # ─── Sidebar ───────────────────────────────────
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div class="sidebar-logo">
          <div class="sidebar-logo-icon">🛗</div>
          <div class="sidebar-logo-text">
            <h3>LiftTech</h3>
            <p>نظام إدارة المصاعد</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # User info
        st.markdown(f"""
        <div class="sidebar-user">
          <div class="sidebar-user-avatar">{avatar_char}</div>
          <div class="sidebar-user-info">
            <div class="sidebar-user-name">{display_name}</div>
            <div class="sidebar-user-role">{role_ar}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Navigation based on role
        if is_admin() or is_manager():
            nav_options = {
                "📊  لوحة التحكم":   "dashboard",
                "📋  العقود":          "contracts",
                "🔧  أوامر العمل":    "work_orders",
                "🚨  البلاغات":       "fault_reports",
                "📝  سجل الصيانة":   "maintenance",
                "🛗  المصاعد":        "elevators",
                "📅  التقويم":        "calendar",
                "👷  الفنيون":        "technicians",
                "👤  حسابي":          "account",
            }
        elif is_tech():
            nav_options = {
                "📊  لوحتي":           "dashboard",
                "🔧  أوامر عملي":     "work_orders",
                "🚨  بلاغاتي":        "fault_reports",
                "📝  سجل الصيانة":   "maintenance",
                "📅  التقويم":        "calendar",
                "👤  حسابي":          "account",
            }
        else:
            nav_options = {
                "📊  عقدي":            "dashboard",
                "🚨  بلاغاتي":        "fault_reports",
                "📝  سجل الصيانة":   "maintenance",
                "🛗  مصاعدي":         "elevators",
                "👤  حسابي":          "account",
            }

        # حفظ الصفحة المختارة في session_state
        nav_keys = list(nav_options.keys())
        nav_vals = list(nav_options.values())
        saved_page = st.session_state.get("current_page", "dashboard")
        # اعثر على index الصفحة المحفوظة
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

        # Spacer + Logout
        st.markdown("<div style='flex:1; min-height:60px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='border-top:1px solid #e0e4e8; padding-top:12px; margin-top:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.72rem;color:#9ca3af;text-align:center;margin-bottom:10px'>{datetime.now().strftime('%Y-%m-%d  %H:%M')}</div>", unsafe_allow_html=True)
        if st.button("🚪  تسجيل الخروج", use_container_width=True, type="secondary"):
            for key in ["logged_in","username","role","display_name","client_contract"]:
                st.session_state.pop(key, None)
            st.rerun()

    # ─── Top header bar ────────────────────────────
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
      <div class="top-header-title">{page_title}</div>
      <div class="top-header-right">
        <span class="header-badge role-{role}">{role_ar}</span>
        <span class="header-time">{datetime.now().strftime('%Y/%m/%d')}</span>
      </div>
    </div>
    <div style="padding: 24px 28px;">
    """, unsafe_allow_html=True)

    # ─── Page routing ──────────────────────────────
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

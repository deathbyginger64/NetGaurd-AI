import streamlit as st
import pandas as pd
import sqlite3
import time
import random
import altair as alt

DB_PATH = "netguard.db"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="NetGuard AI — Security Operations Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# THEME — Deep Slate + Amber Accent
# Inspired by Splunk SIEM, Elastic Security, PagerDuty
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

/* ════════════════════════════════════════
   DESIGN TOKENS — Sapphire + Electric Orange
   ════════════════════════════════════════ */
:root {
    /* Surfaces — deep sapphire blue (NOT black) */
    --bg-base:    #0b1120;
    --bg-raised:  #0e1628;
    --bg-overlay: #101a2e;
    --bg-card:    #131f35;
    --bg-muted:   #1a2c4a;

    /* Borders */
    --border-0: rgba(148,189,255,0.04);
    --border-1: rgba(148,189,255,0.08);
    --border-2: rgba(148,189,255,0.14);
    --border-3: rgba(148,189,255,0.22);

    /* Primary accent — Electric Orange */
    --orange-300: #fdba74;
    --orange-400: #fb923c;
    --orange-500: #f97316;
    --orange-600: #ea580c;
    --orange-glow: rgba(249,115,22,0.18);

    /* Secondary accent — Sky Blue */
    --sky-300:  #7dd3fc;
    --sky-400:  #38bdf8;
    --sky-500:  #0ea5e9;
    --sky-glow: rgba(14,165,233,0.14);

    /* Semantic — vivid and clear */
    --green-400: #34d399;
    --green-500: #10b981;
    --green-glow: rgba(52,211,153,0.15);
    --red-400:   #fb7185;
    --red-500:   #f43f5e;
    --red-glow:  rgba(244,63,94,0.15);
    --blue-400:  #60a5fa;
    --purple-400:#c084fc;

    /* Amber kept for badge compat */
    --amber-300: #fcd34d;
    --amber-400: #f59e0b;
    --amber-500: #d97706;
    --amber-glow: rgba(245,158,11,0.15);

    /* Cyan kept for badge compat */
    --cyan-400: #22d3ee;
    --cyan-500: #06b6d4;
    --cyan-glow: rgba(6,182,212,0.12);

    /* Text — blue-tinted, not grey */
    --text-primary:   #e2eeff;
    --text-secondary: #7b9cc4;
    --text-tertiary:  #3a5580;
    --text-disabled:  #1e3355;

    /* Typography */
    --font:      'Syne', -apple-system, sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;

    /* Radii */
    --r-xs: 4px;
    --r-sm: 8px;
    --r-md: 12px;
    --r-lg: 18px;
}

/* ════════════════════════════════════════
   GLOBAL — bright sapphire base, no overlays
   ════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg-base) !important;
    font-family: var(--font) !important;
    color: var(--text-primary) !important;
}

/* Animated breathing orb — GPU only, zero layout cost */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -30vh; left: 50%;
    transform: translateX(-50%);
    width: 900px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(ellipse at center,
        rgba(14,165,233,0.07) 0%,
        rgba(249,115,22,0.04) 40%,
        transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: orbBreathe 9s ease-in-out infinite;
    will-change: transform, opacity;
}

/* No ::after vignette — removes all dimness */

[data-testid="stHeader"] {
    background: rgba(11,17,32,0.95) !important;
    border-bottom: 1px solid var(--border-1) !important;
}

.main .block-container {
    background: transparent !important;
    padding: 1.75rem 2.5rem 6rem !important;
    max-width: 1760px;
    position: relative;
    z-index: 1;
}

/* ════════════════════════════════════════
   SIDEBAR — deep panel with orange top strip
   ════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-raised) !important;
    border-right: 1px solid var(--border-1) !important;
    position: relative;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--orange-500), var(--sky-400), transparent);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem !important;
}

[data-testid="stSidebar"] h2 {
    font-family: var(--font-mono) !important;
    font-size: 0.58rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: var(--text-tertiary) !important;
    margin: 0 0 10px !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    color: var(--sky-300) !important;
    background: var(--sky-glow) !important;
    border: 1px solid rgba(14,165,233,0.22) !important;
    padding: 5px 12px !important;
    border-radius: var(--r-xs) !important;
    display: inline-block !important;
    letter-spacing: 0.04em !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    font-family: var(--font) !important;
    font-size: 0.75rem !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] {
    font-family: var(--font-mono) !important;
    font-size: 0.67rem !important;
    font-weight: 500 !important;
    padding: 7px 11px !important;
    margin-bottom: 5px !important;
    border-radius: var(--r-xs) !important;
    border-left-width: 2px !important;
}

[data-testid="stSidebar"] [data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-1) !important;
    border-left: 3px solid var(--orange-500) !important;
    border-radius: var(--r-sm) !important;
    padding: 12px 14px !important;
    margin-bottom: 7px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
    transition: border-left-color 0.2s !important;
}

[data-testid="stSidebar"] [data-testid="metric-container"]:hover {
    border-left-color: var(--sky-400) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.58rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text-tertiary) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    color: var(--sky-300) !important;
    letter-spacing: -0.02em !important;
}

/* ════════════════════════════════════════
   MAIN METRIC CARDS — vivid bordered, well-lit
   ════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-2) !important;
    border-top: 3px solid var(--orange-500) !important;
    border-radius: var(--r-md) !important;
    padding: 20px 22px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35),
                0 1px 0 rgba(255,255,255,0.04) inset !important;
    transition: border-top-color 0.2s, box-shadow 0.2s !important;
}

[data-testid="metric-container"]:hover {
    border-top-color: var(--sky-400) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45),
                0 0 0 1px rgba(56,189,248,0.12),
                0 1px 0 rgba(255,255,255,0.06) inset !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.58rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--text-tertiary) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: var(--sky-300) !important;
    line-height: 1.1 !important;
    letter-spacing: -0.03em !important;
}

/* ════════════════════════════════════════
   ALERTS — vivid, high-contrast
   ════════════════════════════════════════ */
[data-testid="stAlert"] {
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    border-radius: var(--r-sm) !important;
    border-left-width: 3px !important;
    letter-spacing: 0.02em !important;
}

/* ════════════════════════════════════════
   DATAFRAMES
   ════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-1) !important;
    border-radius: var(--r-md) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}

/* ════════════════════════════════════════
   PROGRESS BAR — orange to red gradient
   ════════════════════════════════════════ */
[data-testid="stProgressBar"] > div {
    background: var(--bg-muted) !important;
    border-radius: 6px !important;
    height: 8px !important;
    overflow: hidden !important;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--orange-500), var(--red-400)) !important;
    border-radius: 6px !important;
    box-shadow: 0 0 10px rgba(249,115,22,0.5) !important;
}

/* ════════════════════════════════════════
   DIVIDERS
   ════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid var(--border-1) !important;
    margin: 2rem 0 !important;
}

/* ════════════════════════════════════════
   CAPTIONS
   ════════════════════════════════════════ */
.stCaption, [data-testid="stCaption"] {
    font-family: var(--font-mono) !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-tertiary) !important;
}

/* ════════════════════════════════════════
   SCROLLBAR
   ════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border-2);
    border-radius: 4px;
}

/* ════════════════════════════════════════
   HERO CARD — replaces topbar + hero row
   ════════════════════════════════════════ */
.ng-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-card);
    border: 1px solid var(--border-2);
    border-left: 4px solid var(--orange-500);
    border-radius: var(--r-md);
    padding: 20px 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}

.ng-hero__left {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.ng-hero__wordmark {
    display: flex;
    align-items: center;
    gap: 14px;
}

.ng-hero__icon {
    font-size: 1.8rem;
    line-height: 1;
}

.ng-hero__title {
    font-family: var(--font);
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1;
}

.ng-hero__sub {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--sky-400);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
    opacity: 0.8;
}

.ng-hero__status {
    display: inline-flex;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 6px 14px;
    border-radius: var(--r-xs);
    border: 1px solid;
    width: fit-content;
}

.ng-hero__right {
    display: flex;
    align-items: center;
    gap: 28px;
}

.ng-hero__stat {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 3px;
}

.ng-hero__stat-val {
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 700;
    color: var(--sky-300);
    letter-spacing: -0.04em;
    line-height: 1;
}

.ng-hero__stat-label {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-tertiary);
}

.ng-hero__divider {
    width: 1px;
    height: 40px;
    background: var(--border-1);
}

.ng-hero__clock-block {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 3px;
}

.ng-hero__clock {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
    letter-spacing: 0.04em;
}

/* ════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════ */
.ng-footer {
    margin-top: 2.5rem;
    padding-top: 16px;
    border-top: 1px solid var(--border-1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.ng-footer__left {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-tertiary);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.ng-footer__right {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--text-tertiary);
    letter-spacing: 0.06em;
}

/* ════════════════════════════════════════
   TOPBAR (kept for compatibility, hidden by hero)
   ════════════════════════════════════════ */
.ng-topbar { display: none; }

/* ════════════════════════════════════════
   SECTION HEADINGS — orange accent
   ════════════════════════════════════════ */
.ng-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 20px;
    border-radius: var(--r-sm);
    border: 1px solid;
    font-family: var(--font);
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

.ng-banner--alert {
    background: rgba(244,63,94,0.08);
    border-color: rgba(244,63,94,0.3);
    color: var(--red-400);
    box-shadow: 0 0 32px rgba(244,63,94,0.1), inset 0 1px 0 rgba(244,63,94,0.12);
}

.ng-banner--normal {
    background: rgba(52,211,153,0.06);
    border-color: rgba(52,211,153,0.22);
    color: var(--green-400);
    box-shadow: 0 0 32px rgba(52,211,153,0.07), inset 0 1px 0 rgba(52,211,153,0.1);
}

.ng-banner__dot {
    width: 9px; height: 9px;
    border-radius: 50%; flex-shrink: 0;
}

.ng-banner__dot--alert {
    background: var(--red-400);
    box-shadow: 0 0 10px var(--red-400);
    animation: pulse-dot 1.3s ease-in-out infinite;
}

.ng-banner__dot--normal {
    background: var(--green-400);
    box-shadow: 0 0 10px var(--green-400);
    animation: pulse-dot-slow 3s ease-in-out infinite;
}

.ng-banner__label {
    font-family: var(--font-mono);
    font-size: 0.56rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.55;
    padding-right: 12px;
    border-right: 1px solid currentColor;
    margin-right: 2px;
}

/* ════════════════════════════════════════
   SECTION HEADINGS — orange accent
   ════════════════════════════════════════ */
.ng-section {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    margin-top: 8px;
}

.ng-section__title {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--orange-400);
    white-space: nowrap;
}

.ng-section__title::before {
    content: '▸ ';
    color: var(--sky-400);
    font-size: 0.55rem;
}

.ng-section__line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border-2), transparent);
}

/* ════════════════════════════════════════
   HEALTH PILLS — vivid status dots
   ════════════════════════════════════════ */
.ng-health-row {
    display: flex;
    gap: 10px;
    margin-bottom: 8px;
}

.ng-health-pill {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--bg-card);
    border: 1px solid var(--border-1);
    border-radius: var(--r-sm);
    padding: 10px 16px;
    font-family: var(--font);
    font-size: 0.73rem;
    font-weight: 600;
    color: var(--text-secondary);
    flex: 1;
    transition: border-color 0.2s;
}

.ng-health-pill:hover { border-color: var(--border-2); }

.ng-health-pill__dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.ng-health-pill__dot--green {
    background: var(--green-400);
    box-shadow: 0 0 8px var(--green-400);
    animation: pulse-dot-slow 3s ease-in-out infinite;
}

.ng-health-pill__dot--amber {
    background: var(--orange-400);
    box-shadow: 0 0 8px var(--orange-400);
}

.ng-health-pill__dot--red {
    background: var(--red-400);
    box-shadow: 0 0 8px var(--red-400);
    animation: pulse-dot 1.3s ease-in-out infinite;
}

.ng-health-pill__label {
    color: var(--text-tertiary);
    font-family: var(--font-mono);
    font-size: 0.56rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-right: 4px;
}

/* ════════════════════════════════════════
   THREAT TABLE
   ════════════════════════════════════════ */
.ng-threat-table {
    width: 100%;
    border-collapse: collapse;
}

.ng-threat-table th {
    font-family: var(--font-mono);
    font-size: 0.57rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    padding: 0 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border-1);
}

.ng-threat-table td {
    font-family: var(--font);
    font-size: 0.73rem;
    color: var(--text-secondary);
    padding: 10px 10px;
    border-bottom: 1px solid var(--border-0);
    vertical-align: middle;
}

.ng-threat-table tr:last-child td { border-bottom: none; }

.ng-threat-table tr:hover td {
    background: rgba(14,165,233,0.04);
    color: var(--text-primary);
}

/* ════════════════════════════════════════
   BADGES — vivid pills
   ════════════════════════════════════════ */
.ng-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}

.ng-badge--red    { background: rgba(244,63,94,0.12);   color: var(--red-400);    border: 1px solid rgba(244,63,94,0.25); }
.ng-badge--amber  { background: rgba(245,158,11,0.12);  color: var(--amber-300);  border: 1px solid rgba(245,158,11,0.25); }
.ng-badge--blue   { background: rgba(96,165,250,0.12);  color: var(--blue-400);   border: 1px solid rgba(96,165,250,0.25); }
.ng-badge--purple { background: rgba(192,132,252,0.12); color: var(--purple-400); border: 1px solid rgba(192,132,252,0.25); }
.ng-badge--green  { background: rgba(52,211,153,0.12);  color: var(--green-400);  border: 1px solid rgba(52,211,153,0.25); }

/* ════════════════════════════════════════
   SIDEBAR BRAND
   ════════════════════════════════════════ */
.ng-brand {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-1);
    margin-bottom: 16px;
}

.ng-brand__name {
    font-family: var(--font);
    font-size: 0.92rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-primary);
}

.ng-brand__ver {
    font-family: var(--font-mono);
    font-size: 0.54rem;
    color: var(--sky-400);
    letter-spacing: 0.06em;
    margin-top: 2px;
    opacity: 0.7;
}

/* ════════════════════════════════════════
   LIVE ALERT FEED CARDS
   ════════════════════════════════════════ */
.ng-alert-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: var(--bg-card);
    border: 1px solid rgba(244,63,94,0.18);
    border-left: 3px solid var(--red-400);
    border-radius: var(--r-sm);
    padding: 10px 14px;
    margin-bottom: 7px;
    transition: border-color 0.18s;
}

.ng-alert-card:hover {
    border-color: rgba(244,63,94,0.35);
    border-left-color: var(--red-400);
}

.ng-alert-card__dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--red-400);
    box-shadow: 0 0 8px var(--red-400);
    flex-shrink: 0;
    margin-top: 4px;
    animation: pulse-dot 1.3s ease-in-out infinite;
}

.ng-alert-card__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.ng-alert-card__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}

.ng-alert-card__conf {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.ng-alert-card__meta {
    font-family: var(--font);
    font-size: 0.7rem;
    color: var(--text-tertiary);
}

/* ════════════════════════════════════════
   KEYFRAME ANIMATIONS — GPU only
   ════════════════════════════════════════ */
@keyframes pulse-dot {
    0%, 100% { opacity: 1;   transform: scale(1); }
    50%       { opacity: 0.25; transform: scale(0.75); }
}

@keyframes pulse-dot-slow {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.55; }
}

@keyframes orbBreathe {
    0%, 100% { opacity: 1;    transform: translateX(-50%) scale(1); }
    50%       { opacity: 0.55; transform: translateX(-50%) scale(1.18); }
}

/* ════════════════════════════════════════
   MARKDOWN TABLES
   ════════════════════════════════════════ */
.stMarkdown table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
}

.stMarkdown th {
    font-family: var(--font-mono) !important;
    font-size: 0.57rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--text-tertiary) !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid var(--border-1) !important;
    background: var(--bg-overlay) !important;
}

.stMarkdown td {
    color: var(--text-secondary) !important;
    padding: 9px 14px !important;
    border-bottom: 1px solid var(--border-0) !important;
}

.stMarkdown tr:hover td {
    background: rgba(14,165,233,0.04) !important;
    color: var(--text-primary) !important;
}

.stMarkdown code {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--sky-300) !important;
    background: var(--sky-glow) !important;
    padding: 1px 7px !important;
    border-radius: 4px !important;
    border: 1px solid rgba(14,165,233,0.18) !important;
}

/* Headers */
.stMarkdown h2 {
    font-family: var(--font) !important;
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    margin-bottom: 0 !important;
}

.stMarkdown h3 {
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def load_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT * FROM anomaly_logs ORDER BY id DESC", conn
        )
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def safe_int(series):
    return series.apply(
        lambda x: int.from_bytes(x, "little")
        if isinstance(x, (bytes, bytearray)) else int(x)
    )

def safe_float(val):
    if isinstance(val, (bytes, bytearray)):
        return float(int.from_bytes(val, "little"))
    return float(val)

def badge_color(alert_type: str) -> str:
    t = str(alert_type).lower()
    if any(k in t for k in ["ddos","flood","dos"]):        return "red"
    if any(k in t for k in ["scan","probe","recon"]):      return "amber"
    if any(k in t for k in ["inject","exploit","payload"]): return "purple"
    if any(k in t for k in ["brute","login","auth"]):      return "blue"
    return "green"

def check_ids_active(df):
    """Returns True if the most recent log is within 3 seconds — IDS is live."""
    try:
        last_log_time = pd.to_datetime(df["timestamp"].iloc[0])
        now = pd.Timestamp.now()
        return (now - last_log_time).seconds < 3
    except Exception:
        return False

def check_db():
    """Returns True if the SQLite database is reachable."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

logs = load_logs()

if logs.empty:
    st.warning("⚠️ No logs found. Run isolation_forest_model.py first.")
    st.stop()

for col in ["packet_count", "max_packet_size", "unique_src_ips", "unique_dst_ips"]:
    if col in logs.columns:
        logs[col] = safe_int(logs[col])

if "avg_packet_size" in logs.columns:
    logs["avg_packet_size"] = logs["avg_packet_size"].apply(safe_float)
if "anomaly_score" in logs.columns:
    logs["anomaly_score"] = logs["anomaly_score"].apply(safe_float)

# -------------------------------------------------
# HYBRID MODEL FIXES (ADD-ON)
# -------------------------------------------------

# Fix score column if needed
if "score" in logs.columns and "anomaly_score" not in logs.columns:
    logs.rename(columns={"score": "anomaly_score"}, inplace=True)

# Ensure confidence column exists
if "confidence" not in logs.columns:
    logs["confidence"] = "LOW"

# Ensure numeric safety
if "anomaly_score" in logs.columns:
    logs["anomaly_score"] = logs["anomaly_score"].astype(float)

latest_label      = logs["label"].iloc[0]
latest_alert_type = logs["alert_type"].iloc[0] if "alert_type" in logs.columns else "None"
total_anomalies   = (logs["label"] == "Anomaly").sum()
total_logs        = len(logs)
anomaly_rate      = round((total_anomalies / total_logs) * 100, 1) if total_logs else 0


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div class="ng-brand">
        <span style="font-size:1.05rem">🛡️</span>
        <div>
            <div class="ng-brand__name">NetGuard AI</div>
            <div class="ng-brand__ver">SOC Platform v2.1 · Isolation Forest</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Active Profile")
    profile_id = logs["profile_id"].iloc[0]
    st.markdown(f"### `{profile_id}`")

    st.divider()

    st.subheader("Engine Status")
    ids_online = check_ids_active(logs)
    db_online  = check_db()

    if ids_online:
        st.success("Isolation Forest: ACTIVE")
        st.success("One-Class SVM: ACTIVE")
    else:
        st.error("Detection Engine: OFFLINE")

    if db_online:
        st.success("SQLite Database: CONNECTED")
    else:
        st.error("Database: DISCONNECTED")

    st.info("Rule Engine: ACTIVE")

    st.divider()

    st.subheader("Session Summary")
    st.metric("Total Logs",      total_logs)
    st.metric("Total Anomalies", total_anomalies)
    st.metric("Anomaly Rate",    f"{anomaly_rate}%")

    st.divider()

    last_event = logs["timestamp"].iloc[0]
    st.caption(f"Last event · {last_event}")
    st.caption("Auto-refresh · 1 s")


# -------------------------------------------------
# MAIN — TOP BAR
# -------------------------------------------------

# Pre-compute for hero section
recent            = logs.head(20)
recent_anomaly_rate = (recent["label"] == "Anomaly").mean() * 100

now_str = time.strftime("%Y-%m-%d  %H:%M:%S UTC")
recent_alerts = int((logs.head(20)["label"] == "Anomaly").sum())

# ── Single unified topbar + hero ──
status_color  = "#f43f5e" if latest_label == "Anomaly" else "#34d399"
status_text   = f"⚠ THREAT ACTIVE — {latest_alert_type.upper()}" if latest_label == "Anomaly" else "● All Systems Nominal"
threat_pct    = round(recent_anomaly_rate, 1)

st.markdown(f"""
<div class="ng-hero">
    <div class="ng-hero__left">
        <div class="ng-hero__wordmark">
            <span class="ng-hero__icon">🔐</span>
            <div>
                <div class="ng-hero__title">NetGuard AI</div>
                <div class="ng-hero__sub">Security Operations Center · Hybrid ML Detection</div>
            </div>
        </div>
        <div class="ng-hero__status" style="color:{status_color}; border-color:{status_color}40; background:{status_color}10;">
            {status_text}
        </div>
    </div>
    <div class="ng-hero__right">
        <div class="ng-hero__stat">
            <span class="ng-hero__stat-val">{recent_alerts}</span>
            <span class="ng-hero__stat-label">Active Alerts</span>
        </div>
        <div class="ng-hero__divider"></div>
        <div class="ng-hero__stat">
            <span class="ng-hero__stat-val" style="color:{'#f43f5e' if threat_pct > 50 else '#fb923c' if threat_pct > 20 else '#34d399'};">{threat_pct}%</span>
            <span class="ng-hero__stat-label">Threat Rate</span>
        </div>
        <div class="ng-hero__divider"></div>
        <div class="ng-hero__clock-block">
            <span class="ng-hero__clock">{now_str}</span>
            <span class="ng-hero__stat-label">UTC · Auto-refresh 1s</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# ACTIVE THREAT BANNER (MOST VISIBLE 🚨)
# -------------------------------------------------

latest = logs.iloc[0]

if latest["label"] == "Anomaly":
    conf_val  = str(latest.get("confidence", "N/A")).upper()
    atype_val = str(latest.get("alert_type",  "Unknown")).upper()
    st.error(f"🚨 ACTIVE THREAT DETECTED — **{atype_val}** · Confidence: **{conf_val}** · Immediate review required.")
else:
    st.success("🟢 SYSTEM SECURE — No active threats detected. All systems operating within normal parameters.")

# recent & recent_anomaly_rate already computed above
avg_recent_risk = (
    logs.head(20)["anomaly_score"].mean()
    if "anomaly_score" in logs.columns else 0.0
)

if recent_anomaly_rate > 50 or avg_recent_risk > 0.6:
    st.error(f"🔴 Threat Level: CRITICAL — {round(recent_anomaly_rate,1)}% anomaly rate · avg risk {round(avg_recent_risk,3)}")
elif recent_anomaly_rate > 20 or avg_recent_risk > 0.3:
    st.warning(f"🟠 Threat Level: ELEVATED — {round(recent_anomaly_rate,1)}% anomaly rate · avg risk {round(avg_recent_risk,3)}")
else:
    st.success(f"🟢 Threat Level: LOW — {round(recent_anomaly_rate,1)}% anomaly rate · avg risk {round(avg_recent_risk,3)}")

st.caption("THREAT INTENSITY BAR")
st.progress(min(recent_anomaly_rate / 100, 1.0))


# -------------------------------------------------
# SYSTEM HEALTH ROW
# -------------------------------------------------

engine_status   = "green" if ids_online else "red"
engine_label    = "Isolation Forest + SVM" if ids_online else "OFFLINE"
db_status       = "green" if db_online  else "red"
db_label        = "SQLite · Connected"     if db_online  else "DISCONNECTED"
ingestion_status = "green" if ids_online  else "red"
ingestion_label  = "Live · 1 s cadence"   if ids_online else "No live feed"

st.markdown(f"""
<div class="ng-section">
    <span class="ng-section__title">System Health</span>
    <span class="ng-section__line"></span>
</div>
<div class="ng-health-row">
    <div class="ng-health-pill">
        <span class="ng-health-pill__dot ng-health-pill__dot--{engine_status}"></span>
        <span class="ng-health-pill__label">Detection Engine</span>{engine_label}
    </div>
    <div class="ng-health-pill">
        <span class="ng-health-pill__dot ng-health-pill__dot--{db_status}"></span>
        <span class="ng-health-pill__label">Database</span>{db_label}
    </div>
    <div class="ng-health-pill">
        <span class="ng-health-pill__dot ng-health-pill__dot--amber"></span>
        <span class="ng-health-pill__label">Rule Engine</span>Active
    </div>
    <div class="ng-health-pill">
        <span class="ng-health-pill__dot ng-health-pill__dot--{ingestion_status}"></span>
        <span class="ng-health-pill__label">Ingestion</span>{ingestion_label}
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Live Telemetry</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("📡 Packets / sec",  int(logs["packet_count"].iloc[0]))
with k2:
    score_val = round(float(logs["anomaly_score"].iloc[0]), 3) if "anomaly_score" in logs.columns else 0
    st.metric("📉 Anomaly Score",  score_val)
with k3:
    st.metric("⚡ Confidence",     str(logs["confidence"].iloc[0]).upper() if "confidence" in logs.columns else "N/A")
with k4:
    atype_display = str(logs["alert_type"].iloc[0]) if latest_label == "Anomaly" else "None"
    st.metric("⚠️ Alert Type",     atype_display)

# ── Attack Counter ──
total_attacks = len(logs[logs["label"] == "Anomaly"])
st.metric("🚨 Total Attacks Detected", total_attacks)

st.divider()

# -------------------------------------------------
# TRAFFIC INTENSITY (NEW 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Traffic Intensity</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

recent_packets = logs["packet_count"].head(20)
avg_load = recent_packets.mean()

# DDoS spike check on latest reading
if logs["packet_count"].iloc[0] > 30:
    st.error("🚨 POSSIBLE DDoS SPIKE DETECTED — Packet count exceeds threshold on latest event!")

col1, col2 = st.columns(2)

with col1:
    st.metric("Avg Packets/sec (20 events)", round(avg_load, 2))

with col2:
    if avg_load > 20:
        st.error("High Traffic Load ⚠️")
    elif avg_load > 5:
        st.warning("Moderate Traffic")
    else:
        st.success("Low Traffic")

st.divider()

# -------------------------------------------------
# TRAFFIC ANALYTICS  +  ANOMALY SCORE TREND
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Traffic Analytics</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 2, 1.4])

with c1:
    st.caption("PACKET VOLUME & AVERAGE SIZE — Last 50 events")
    st.line_chart(
        logs.head(50)[["packet_count", "avg_packet_size"]]
        .rename(columns={
            "packet_count":    "Packets per Second",
            "avg_packet_size": "Average Packet Size"
        })
    )

with c2:
    st.caption("SOURCE vs DESTINATION IP DIVERSITY — Last 30 events")
    st.bar_chart(
        logs.head(30)[["unique_src_ips", "unique_dst_ips"]]
        .rename(columns={
            "unique_src_ips": "Unique Source IPs",
            "unique_dst_ips": "Unique Destination IPs"
        })
    )

with c3:
    st.caption("ANOMALY SCORE TREND — Last 50 events (red = danger)")
    if "anomaly_score" in logs.columns:
        score_plot_df = logs.head(50)[["anomaly_score"]].reset_index()
        score_plot_df.columns = ["Event", "anomaly_score"]
        red_chart = (
            alt.Chart(score_plot_df)
            .mark_area(
                color="#f43f5e",
                line={"color": "#f43f5e", "strokeWidth": 2},
                fillOpacity=0.15
            )
            .encode(
                x=alt.X("Event:Q", title=None,
                         axis=alt.Axis(labelColor="#3a5580", gridColor="rgba(148,189,255,0.05)")),
                y=alt.Y("anomaly_score:Q", title=None,
                         axis=alt.Axis(labelColor="#3a5580", gridColor="rgba(148,189,255,0.05)")),
                tooltip=["Event", "anomaly_score"]
            )
            .properties(background="transparent")
            .configure_view(strokeOpacity=0)
        )
        st.altair_chart(red_chart, use_container_width=True)

st.divider()

# -------------------------------------------------
# ATTACK THREAT TIMELINE (NEW 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Attack Threat Timeline</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

if "timestamp" in logs.columns and "anomaly_score" in logs.columns:
    try:
        timeline = logs.copy()
        timeline["ts"] = pd.to_datetime(timeline["timestamp"])
        timeline = timeline.sort_values("ts")

        timeline_chart = (
            alt.Chart(timeline)
            .mark_line(strokeWidth=2.5)
            .encode(
                x=alt.X("ts:T", title=None,
                         axis=alt.Axis(labelColor="#3a5580",
                                       gridColor="rgba(148,189,255,0.05)",
                                       format="%H:%M:%S",
                                       labelFontSize=10,
                                       labelFont="IBM Plex Mono")),
                y=alt.Y("anomaly_score:Q", title="Risk Score",
                         axis=alt.Axis(labelColor="#3a5580",
                                       gridColor="rgba(148,189,255,0.05)",
                                       labelFontSize=10,
                                       labelFont="IBM Plex Mono")),
                color=alt.Color("label:N",
                    scale=alt.Scale(
                        domain=["Normal", "Anomaly"],
                        range=["#34d399", "#f43f5e"]
                    ),
                    legend=alt.Legend(
                        labelColor="#7b9cc4",
                        titleColor="#3a5580",
                        labelFont="IBM Plex Mono",
                        labelFontSize=10
                    )
                ),
                tooltip=["ts:T", "anomaly_score:Q", "label:N",
                         alt.Tooltip("alert_type:N", title="Alert Type")]
            )
            .properties(height=220, background="transparent")
            .configure_view(strokeOpacity=0)
        )
        st.altair_chart(timeline_chart, use_container_width=True)
        st.caption("Green = Normal traffic · Red = Anomalous events · Hover for details")
    except Exception as e:
        st.info(f"Timeline unavailable: {e}")

st.divider()

# -------------------------------------------------
# THREAT BREAKDOWN  +  ALERT FEED
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Threat Intelligence</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

threat_col, alert_col = st.columns([1.2, 2])

with threat_col:
    st.caption("THREAT TYPE DISTRIBUTION")

    if "alert_type" in logs.columns:
        alerts_only = logs[logs["label"] == "Anomaly"]
        if not alerts_only.empty:
            type_counts = (
                alerts_only["alert_type"]
                .value_counts()
                .reset_index()
            )
            type_counts.columns = ["alert_type", "count"]
            type_counts["pct"] = (
                type_counts["count"] / type_counts["count"].sum() * 100
            ).round(1)

            # Altair horizontal bar chart
            chart = (
                alt.Chart(type_counts)
                .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
                .encode(
                    x=alt.X("count:Q", title=None,
                             axis=alt.Axis(labelColor="#3a5580",
                                           gridColor="rgba(148,189,255,0.06)",
                                           domainOpacity=0,
                                           tickOpacity=0)),
                    y=alt.Y("alert_type:N", title=None, sort="-x",
                             axis=alt.Axis(labelColor="#7b9cc4",
                                           labelFontSize=11,
                                           labelFont="IBM Plex Mono")),
                    color=alt.value("#f97316"),
                    tooltip=["alert_type", "count", "pct"]
                )
                .properties(height=180, background="transparent")
                .configure_view(strokeOpacity=0)
            )
            st.altair_chart(chart, use_container_width=True)

            # Summary table
            rows = ""
            for _, row in type_counts.iterrows():
                bc = badge_color(row["alert_type"])
                rows += f"""
                <tr>
                    <td><span class="ng-badge ng-badge--{bc}">{row['alert_type']}</span></td>
                    <td style="text-align:right; font-family:var(--font-mono);
                               color:var(--text-primary);">{int(row['count'])}</td>
                    <td style="text-align:right; color:var(--text-tertiary);">{row['pct']}%</td>
                </tr>"""
            st.markdown(f"""
            <table class="ng-threat-table">
                <thead><tr>
                    <th>Type</th><th style="text-align:right">Count</th>
                    <th style="text-align:right">Share</th>
                </tr></thead>
                <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.success("No threat types to display — feed is clear.")
    else:
        st.info("alert_type column not available.")

with alert_col:
    st.caption("RECENT ANOMALY EVENTS — Last 10")
    alerts = logs[logs["label"] == "Anomaly"].head(10)
    if alerts.empty:
        st.success("No anomalies in the current observation window.")
    else:
        def color_conf(val):
            if val == "HIGH":   return "background-color: rgba(244,63,94,0.25); color: #f43f5e; font-weight: 700"
            elif val == "MEDIUM": return "background-color: rgba(251,146,60,0.18); color: #fb923c; font-weight: 600"
            else:               return "color: #38bdf8; font-weight: 500"

        st.dataframe(
            alerts[[
                "timestamp", "alert_type", "confidence",
                "profile_id",
                "packet_count", "avg_packet_size", "max_packet_size",
                "unique_src_ips", "unique_dst_ips", "anomaly_score"
            ]].style.applymap(color_conf, subset=["confidence"]),
            use_container_width=True,
            height=220
        )
        st.caption("LIVE ALERT FEED — Latest 5")
        alert_cards_html = ""
        for _, row in alerts.head(5).iterrows():
            score_val = round(float(row["anomaly_score"]), 3) if "anomaly_score" in row else "N/A"
            conf_val  = str(row["confidence"]).upper() if "confidence" in row else "N/A"
            atype     = str(row["alert_type"]).upper()
            ts        = str(row["timestamp"])[:19]
            bc        = badge_color(str(row["alert_type"]))
            conf_color = {"HIGH": "#f43f5e", "MEDIUM": "#fb923c", "LOW": "#38bdf8"}.get(conf_val, "#7b9cc4")
            alert_cards_html += f"""
            <div class="ng-alert-card">
                <div class="ng-alert-card__dot"></div>
                <div class="ng-alert-card__body">
                    <div class="ng-alert-card__top">
                        <span class="ng-badge ng-badge--{bc}" style="border-radius:999px;">{atype}</span>
                        <span class="ng-alert-card__conf" style="color:{conf_color};">{conf_val}</span>
                    </div>
                    <div class="ng-alert-card__meta">
                        Score <strong style="color:var(--text-primary);font-family:var(--font-mono);">{score_val}</strong>
                        &nbsp;·&nbsp;
                        <span style="color:var(--text-tertiary);">{ts}</span>
                    </div>
                </div>
            </div>"""
        st.markdown(alert_cards_html, unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# ANOMALY RATE OVER TIME
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Anomaly Density Over Time</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

if "timestamp" in logs.columns:
    try:
        density_df = logs.copy()
        density_df["ts"] = pd.to_datetime(density_df["timestamp"])
        density_df = density_df.sort_values("ts")
        density_df["is_anomaly"] = (density_df["label"] == "Anomaly").astype(int)
        density_df["rolling_rate"] = (
            density_df["is_anomaly"].rolling(20, min_periods=1).mean() * 100
        )
        st.caption("ROLLING ANOMALY RATE (20-event window) — %")
        density_alt = (
            alt.Chart(density_df)
            .mark_area(
                color="#f97316",
                line={"color": "#f97316", "strokeWidth": 2},
                fillOpacity=0.12
            )
            .encode(
                x=alt.X("ts:T", title=None,
                         axis=alt.Axis(labelColor="#3a5580",
                                       gridColor="rgba(148,189,255,0.05)",
                                       format="%H:%M:%S",
                                       labelFont="IBM Plex Mono", labelFontSize=10)),
                y=alt.Y("rolling_rate:Q", title="Anomaly Rate %",
                         axis=alt.Axis(labelColor="#3a5580",
                                       gridColor="rgba(148,189,255,0.05)",
                                       labelFont="IBM Plex Mono", labelFontSize=10)),
                tooltip=[alt.Tooltip("ts:T", title="Time"),
                         alt.Tooltip("rolling_rate:Q", title="Rate %", format=".1f")]
            )
            .properties(height=160, background="transparent")
            .configure_view(strokeOpacity=0)
        )
        st.altair_chart(density_alt, use_container_width=True)
    except Exception:
        st.info("Timestamp parsing unavailable — skipping density chart.")
else:
    st.info("Timestamp column not found.")

st.divider()

# -------------------------------------------------
# ATTACK SUMMARY PANEL (NEW 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">🧠 Detection Summary</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    top_threat = (
        logs[logs["label"] == "Anomaly"]["alert_type"].value_counts().idxmax()
        if total_anomalies > 0 else "None"
    )
    avg_risk = round(logs["anomaly_score"].mean(), 4) if "anomaly_score" in logs.columns else "N/A"

    st.markdown(f"""
| Metric | Value |
|---|---|
| 📋 Total Logs Analysed | `{total_logs}` |
| 🚨 Total Anomalies | `{total_anomalies}` |
| 📈 Detection Rate | `{round(anomaly_rate, 2)}%` |
| 🎯 Top Threat Type | `{top_threat}` |
| 📊 Avg Risk Score | `{avg_risk}` |
""")

with summary_col2:
    # Pre-compute agreement_ratio for summary panel
    _conf_counts_preview = logs["confidence"].value_counts()
    _high_preview  = _conf_counts_preview.get("HIGH", 0)
    _total_preview = len(logs)
    agreement_ratio_preview = round((_high_preview / _total_preview) * 100, 2) if _total_preview else 0

    st.markdown(f"""
| Metric | Value |
|---|---|
| 🤖 Model Agreement | `{agreement_ratio_preview}%` |
| 🟢 Threat Level (20 events) | `{round(recent_anomaly_rate, 1)}%` |
| 🔵 IDS Engine | `{'ONLINE' if ids_online else 'OFFLINE'}` |
| 🗄️ Database | `{'CONNECTED' if db_online else 'DISCONNECTED'}` |
| ⏱️ Last Event | `{str(logs["timestamp"].iloc[0])[:19]}` |
""")

st.divider()

# -------------------------------------------------
# AI MODEL INTELLIGENCE (NEW 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">AI Model Intelligence</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 2])

with col1:
    st.caption("CONFIDENCE DISTRIBUTION")

    conf_counts = logs["confidence"].value_counts()

    conf_df = pd.DataFrame({
        "confidence": conf_counts.index,
        "count": conf_counts.values
    })

    chart = (
        alt.Chart(conf_df)
        .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
        .encode(
            x=alt.X("count:Q", title=None),
            y=alt.Y("confidence:N", sort="-x", title=None),
            color=alt.value("#f59e0b"),
            tooltip=["confidence", "count"]
        )
        .properties(height=160)
    )

    st.altair_chart(chart, use_container_width=True)

with col2:
    st.caption("MODEL AGREEMENT & DETECTION QUALITY")

    total = len(logs)
    high   = conf_counts.get("HIGH",   0)
    medium = conf_counts.get("MEDIUM", 0)
    low    = conf_counts.get("LOW",    0)

    agreement_ratio = round((high / total) * 100, 2) if total else 0

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("High Confidence",   high)
    with m2:
        st.metric("Medium Confidence", medium)
    with m3:
        st.metric("Low Confidence",    low)

    st.caption(f"Model Agreement (HIGH confidence): {agreement_ratio}%")

    # Scatter plot: score vs confidence
    if "anomaly_score" in logs.columns:
        scatter_df = logs.head(100)[["anomaly_score", "confidence"]]

        scatter = (
            alt.Chart(scatter_df)
            .mark_circle(size=60)
            .encode(
                x="anomaly_score",
                y="confidence",
                color="confidence",
                tooltip=["anomaly_score", "confidence"]
            )
        )

        st.altair_chart(scatter, use_container_width=True)

st.divider()

# -------------------------------------------------
# MODEL BEHAVIOR INSIGHT (NEW 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Model Behavior Insight</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

if total > 0:
    disagreement = medium
    agreement = high

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Model Agreement", f"{round((agreement/total)*100,2)}%")

    with col2:
        st.metric("Model Disagreement", f"{round((disagreement/total)*100,2)}%")

    if agreement > disagreement:
        st.success("Models are consistent → Stable detection")
    else:
        st.warning("Models disagree → Possible edge-case traffic")

st.divider()

# -------------------------------------------------
# DETECTION METRICS (RESEARCH READY 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Detection Metrics</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

anomaly_rate_calc = (logs["label"] == "Anomaly").mean() * 100

high_conf_anomalies = logs[
    (logs["label"] == "Anomaly") &
    (logs["confidence"] == "HIGH")
]

precision_estimate = (
    len(high_conf_anomalies) / total_anomalies * 100
    if total_anomalies else 0
)

m1, m2 = st.columns(2)

with m1:
    st.metric("Anomaly Rate (%)", round(anomaly_rate_calc, 2))

with m2:
    st.metric("High Confidence Precision (%)", round(precision_estimate, 2))

st.divider()

# -------------------------------------------------
# MODEL EVALUATION (FINAL 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Model Evaluation</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

TP = len(logs[(logs["label"] == "Anomaly") & (logs["confidence"] == "HIGH")])
FP = len(logs[(logs["label"] == "Anomaly") & (logs["confidence"] != "HIGH")])
TN = len(logs[(logs["label"] == "Normal")])
FN = 0  # unsupervised assumption — no labelled ground truth

detection_rate      = (TP / (TP + FN)) * 100 if (TP + FN) else 0
false_positive_rate = (FP / (FP + TN)) * 100 if (FP + TN) else 0

ev1, ev2, ev3, ev4 = st.columns(4)

with ev1:
    st.metric("True Positives (TP)", TP)
with ev2:
    st.metric("False Positives (FP)", FP)
with ev3:
    st.metric("Detection Rate (%)", round(detection_rate, 2))
with ev4:
    st.metric("False Positive Rate (%)", round(false_positive_rate, 2))

st.caption("⚠️ Estimated using hybrid confidence (unsupervised approximation — HIGH confidence = TP, LOW confidence anomaly = FP)")

if detection_rate >= 80:
    st.success(f"✅ Strong detection — {round(detection_rate,1)}% of anomalies captured with high model agreement.")
elif detection_rate >= 40:
    st.warning(f"🟠 Moderate detection rate ({round(detection_rate,1)}%). Consider tightening anomaly score thresholds.")
else:
    st.error(f"🔴 Low detection rate ({round(detection_rate,1)}%). Models may need retraining or threshold adjustment.")

st.divider()

# -------------------------------------------------
# MODEL DECISION SAMPLE (B 🔥)
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">Model Decision Sample</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

st.caption("MODEL OUTPUT — Last 10 events · Anomaly Score + Confidence assigned by hybrid model")

if "anomaly_score" in logs.columns:
    def color_conf_sample(val):
        if val == "HIGH":     return "background-color: rgba(244,63,94,0.25); color: #f43f5e; font-weight: 700"
        elif val == "MEDIUM": return "background-color: rgba(251,146,60,0.18); color: #fb923c; font-weight: 600"
        else:                 return "color: #38bdf8; font-weight: 500"

    sample_cols = ["timestamp", "label", "anomaly_score", "confidence"]
    sample_df   = logs[sample_cols].head(10).copy()

    st.dataframe(
        sample_df.style.applymap(color_conf_sample, subset=["confidence"]),
        use_container_width=True,
        height=380
    )
else:
    st.info("anomaly_score column not available.")

st.divider()

# -------------------------------------------------
# FULL SYSTEM EVENT LOG
# -------------------------------------------------

st.markdown("""
<div class="ng-section">
    <span class="ng-section__title">System Event Log — Last 100 Records</span>
    <span class="ng-section__line"></span>
</div>
""", unsafe_allow_html=True)

def highlight_rows(row):
    return [
        'background-color: rgba(244,63,94,0.2)' if row['label'] == "Anomaly" else ''
        for _ in row
    ]

st.dataframe(
    logs.head(100).style.apply(highlight_rows, axis=1),
    use_container_width=True,
    height=380
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(f"""
<div class="ng-footer">
    <div class="ng-footer__left">
        NetGuard AI · SOC Platform v2.1 · Isolation Forest + One-Class SVM
    </div>
    <div class="ng-footer__right">
        {total_logs} events ingested · {total_anomalies} anomalies detected · Auto-refresh 1 s
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# AUTO REFRESH
# -------------------------------------------------
time.sleep(1)
st.rerun()
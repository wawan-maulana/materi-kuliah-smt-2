"""
APP.PY — FRONTEND STREAMLIT
Hanya konfigurasi halaman + pemanggilan fungsi dari backend.py.
Tidak ada def sama sekali.

Jalankan:
    streamlit run app.py
"""

import streamlit as st
from backend import (
    init_state,
    inject_css,
    render_header,
    render_metrik,
    render_banner_audio,
    render_notif,
    render_form_pesan,
    render_antrian,
    render_panel_chef,
    render_riwayat,
)

# ── Konfigurasi halaman ───────────────────────────────
st.set_page_config(
    page_title="ANTRIAN_MAKANAN",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Bootstrap ─────────────────────────────────────────
inject_css()
init_state()

antrian = st.session_state.antrian

# ── Header ────────────────────────────────────────────
render_header()

# ── Broadcast + notifikasi ────────────────────────────
render_banner_audio()
render_notif()

# ── Metrik ────────────────────────────────────────────
render_metrik(antrian)

# ── Navigasi tab ──────────────────────────────────────
tab_pesan, tab_dapur, tab_riwayat = st.tabs([
    "ORDER",
    "CHEF STATION",
    "HISTORY",
])

with tab_pesan:
    kiri, kanan = st.columns([1, 1], gap="large")
    with kiri:
        render_form_pesan(antrian)
    with kanan:
        render_antrian(antrian)

with tab_dapur:
    kiri, kanan = st.columns([1, 1], gap="large")
    with kiri:
        render_panel_chef(antrian)
    with kanan:
        render_antrian(antrian)

with tab_riwayat:
    render_riwayat(antrian)

# ── Footer ────────────────────────────────────────────
st.markdown(
    "<div style='padding:24px 0 8px;font-family:\"Share Tech Mono\",monospace;"
    "font-size:0.58rem;letter-spacing:2px;color:#1e2a24;text-align:center'>"
    "FOOD QUEUE SYS &nbsp;//&nbsp; PYTHON + STREAMLIT + GTTS &nbsp;//&nbsp; "
    "FIFO :: COLLECTIONS.DEQUE</div>",
    unsafe_allow_html=True,
)

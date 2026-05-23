"""
BACKEND — SISTEM ANTRIAN PEMESANAN MAKANAN
Model · Queue · TTS · Session State · Render UI

Semua logika (bisnis + render Streamlit) ada di sini.
app.py hanya memanggil fungsi dari modul ini.
"""

import base64
import io
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime

import streamlit as st
from gtts import gTTS


# ════════════════════════════════════════════════════════
#  KONSTANTA
# ════════════════════════════════════════════════════════

MENU_TERSEDIA: dict[str, int] = {
    "Nasi Goreng":  15_000,
    "Mie Ayam":     12_000,
    "Ayam Bakar":   20_000,
    "Soto Ayam":    13_000,
    "Nasi Padang":  18_000,
    "Gado-Gado":    10_000,
    "Sate Ayam":    14_000,
    "Bakso":        11_000,
    "Es Teh Manis":  5_000,
    "Kopi Hitam":    8_000,
}

STATUS_LABEL: dict[str, str] = {
    "menunggu": "WAIT",
    "diproses": "COOK",
    "selesai":  "DONE",
}

STATUS_COLOR: dict[str, str] = {
    "menunggu": "#f0c040",
    "diproses": "#00ffe0",
    "selesai":  "#39ff80",
}


# ════════════════════════════════════════════════════════
#  MODEL DATA
# ════════════════════════════════════════════════════════

@dataclass
class Pesanan:
    nomor:       int
    nama:        str
    menu:        list[str]
    waktu_pesan: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    status:      str = "menunggu"

    @property
    def total_harga(self) -> int:
        return sum(MENU_TERSEDIA.get(m, 0) for m in self.menu)

    @property
    def menu_str(self) -> str:
        return ", ".join(self.menu)

    @property
    def harga_str(self) -> str:
        return f"Rp {self.total_harga:,}".replace(",", ".")

    def teks_pengumuman(self) -> str:
        menu_ucap = " dan ".join(m.strip() for m in self.menu)
        return (
            f"Perhatian! Nomor antrian {self.nomor}, "
            f"atas nama {self.nama}, "
            f"pesanan {menu_ucap} sudah siap. "
            f"Silakan ambil pesanan Anda. Terima kasih."
        )


# ════════════════════════════════════════════════════════
#  QUEUE ENGINE
# ════════════════════════════════════════════════════════

class AntrianPesanan:
    def __init__(self) -> None:
        self._queue:   deque[Pesanan] = deque()
        self._selesai: list[Pesanan]  = []
        self._counter: int            = 1

    def tambah_pesanan(self, nama: str, menu: list[str]) -> Pesanan:
        p = Pesanan(nomor=self._counter, nama=nama, menu=menu)
        self._counter += 1
        self._queue.append(p)
        return p

    def pesanan_terdepan(self) -> Pesanan | None:
        return self._queue[0] if self._queue else None

    def mulai_proses(self) -> Pesanan | None:
        if not self._queue:
            return None
        self._queue[0].status = "diproses"
        return self._queue[0]

    def selesaikan_dan_panggil(self) -> Pesanan | None:
        if not self._queue:
            return None
        p = self._queue.popleft()
        p.status = "selesai"
        self._selesai.append(p)
        return p

    @property
    def antrian(self) -> list[Pesanan]:
        return list(self._queue)

    @property
    def riwayat(self) -> list[Pesanan]:
        return list(reversed(self._selesai))

    @property
    def kosong(self) -> bool:
        return len(self._queue) == 0

    @property
    def jumlah_antrian(self) -> int:
        return len(self._queue)

    @property
    def jumlah_selesai(self) -> int:
        return len(self._selesai)

    @property
    def omzet(self) -> int:
        return sum(p.total_harga for p in self._selesai)


# ════════════════════════════════════════════════════════
#  gTTS
# ════════════════════════════════════════════════════════

def buat_audio_b64(pesanan: Pesanan) -> str:
    tts = gTTS(text=pesanan.teks_pengumuman(), lang="id", slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


# ════════════════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════════════════

def init_state() -> None:
    defaults = {
        "antrian":      AntrianPesanan(),
        "notif":        None,
        "audio_b64":    None,
        "banner_teks":  None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ════════════════════════════════════════════════════════
#  CSS GLOBAL — INDUSTRIAL BRUTALIST + ABSTRACT GLITCH
# ════════════════════════════════════════════════════════

def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap');

    :root {
        --bg:        #050608;
        --surface:   #0a0c10;
        --surface2:  #0f1218;
        --border:    rgba(255,255,255,0.06);
        --border-hi: rgba(57,255,128,0.3);
        --neon:      #39ff80;
        --neon-dim:  rgba(57,255,128,0.15);
        --amber:     #f0c040;
        --cyan:      #00ffe0;
        --red:       #ff3b5c;
        --text:      #c8d4cc;
        --muted:     #3a4a40;
        --mono:      'Share Tech Mono', monospace;
        --display:   'Bebas Neue', sans-serif;
        --body:      'DM Mono', monospace;
    }

    html, body, .stApp {
        background: var(--bg) !important;
        font-family: var(--body) !important;
        color: var(--text) !important;
    }

    /* noise overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.6;
    }

    /* scanlines */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,0,0,0.08) 2px,
            rgba(0,0,0,0.08) 4px
        );
        pointer-events: none;
        z-index: 1;
    }

    .block-container {
        max-width: 1280px !important;
        padding: 0 2rem 3rem !important;
        position: relative;
        z-index: 2;
    }

    /* ── HEADER ── */
    .app-header {
        padding: 3rem 0 0.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 0;
        position: relative;
    }
    .app-header-sys {
        font-family: var(--mono);
        font-size: 0.62rem;
        letter-spacing: 3px;
        color: var(--neon);
        text-transform: uppercase;
        margin-bottom: 6px;
        opacity: 0.7;
    }
    .app-header h1 {
        font-family: var(--display) !important;
        font-size: 4.5rem !important;
        line-height: 1 !important;
        letter-spacing: 4px !important;
        color: #fff !important;
        margin: 0 !important;
        -webkit-text-fill-color: initial !important;
    }
    .app-header h1 span {
        color: var(--neon);
    }
    .app-header-sub {
        font-family: var(--mono);
        font-size: 0.65rem;
        color: var(--muted);
        letter-spacing: 2px;
        margin-top: 10px;
        padding-bottom: 1.5rem;
    }

    /* corner decoration */
    .corner-tl {
        position: absolute;
        top: 3rem; left: 0;
        width: 40px; height: 40px;
        border-top: 1px solid var(--neon);
        border-left: 1px solid var(--neon);
        opacity: 0.4;
    }
    .corner-br {
        position: absolute;
        bottom: 0; right: 0;
        width: 40px; height: 40px;
        border-bottom: 1px solid var(--neon);
        border-right: 1px solid var(--neon);
        opacity: 0.4;
    }

    /* ── METRIK ── */
    .metric-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 1px;
        background: var(--border);
        margin: 0;
        border: 1px solid var(--border);
    }
    .metric-cell {
        background: var(--surface);
        padding: 20px 24px;
        position: relative;
        overflow: hidden;
    }
    .metric-cell::after {
        content: '';
        position: absolute;
        bottom: 0; left: 24px; right: 24px;
        height: 1px;
    }
    .metric-cell.c-antrian::after  { background: var(--amber); }
    .metric-cell.c-proses::after   { background: var(--cyan); }
    .metric-cell.c-selesai::after  { background: var(--neon); }
    .metric-cell.c-omzet::after    { background: var(--red); }
    .metric-lbl {
        font-family: var(--mono);
        font-size: 0.58rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--muted);
    }
    .metric-val {
        font-family: var(--display);
        font-size: 3.2rem;
        line-height: 1.1;
        letter-spacing: 2px;
        margin-top: 4px;
    }
    .metric-cell.c-antrian .metric-val  { color: var(--amber); }
    .metric-cell.c-proses  .metric-val  { color: var(--cyan); font-size: 1.2rem; font-family: var(--body); margin-top: 10px; }
    .metric-cell.c-selesai .metric-val  { color: var(--neon); }
    .metric-cell.c-omzet   .metric-val  { color: var(--red); font-size: 1.4rem; font-family: var(--mono); }

    /* ── TAB ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid var(--border) !important;
        gap: 0 !important;
        padding: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-right: 1px solid var(--border) !important;
        border-radius: 0 !important;
        color: var(--muted) !important;
        font-family: var(--mono) !important;
        font-size: 0.68rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        padding: 14px 28px !important;
        transition: color 0.2s !important;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; }
    .stTabs [aria-selected="true"] {
        color: var(--neon) !important;
        border-bottom: 2px solid var(--neon) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 1.5rem 0 !important;
    }

    /* ── ANTRIAN CARDS ── */
    .q-card {
        display: grid;
        grid-template-columns: 70px 1fr auto;
        gap: 0;
        border: 1px solid var(--border);
        margin-bottom: 4px;
        background: var(--surface);
        transition: border-color 0.2s;
        animation: entrySlide 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    @keyframes entrySlide {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .q-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 2px;
    }
    .q-card.s-menunggu::before { background: var(--amber); }
    .q-card.s-diproses::before { background: var(--cyan); }
    .q-card.s-selesai::before  { background: var(--neon); }
    .q-card.top {
        border-color: rgba(0,255,224,0.25);
    }
    .q-card.top.s-diproses {
        border-color: rgba(0,255,224,0.4);
        animation: entrySlide 0.25s ease, glow 2.5s ease-in-out infinite;
    }
    @keyframes glow {
        0%,100% { box-shadow: inset 0 0 0 0 rgba(0,255,224,0); }
        50%      { box-shadow: inset 0 0 20px 0 rgba(0,255,224,0.04); }
    }
    .q-num {
        font-family: var(--display);
        font-size: 2rem;
        letter-spacing: 1px;
        color: var(--muted);
        display: flex;
        align-items: center;
        justify-content: center;
        border-right: 1px solid var(--border);
        padding: 0 10px;
    }
    .q-card.top .q-num { color: var(--cyan); }
    .q-body {
        padding: 12px 16px;
    }
    .q-nama {
        font-family: var(--body);
        font-weight: 500;
        font-size: 0.9rem;
        color: #e0ece4;
    }
    .q-menu {
        font-family: var(--mono);
        font-size: 0.68rem;
        color: var(--muted);
        margin-top: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 280px;
    }
    .q-harga {
        font-family: var(--mono);
        font-size: 0.7rem;
        color: var(--neon);
        margin-top: 3px;
    }
    .q-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: center;
        padding: 12px 16px;
        gap: 6px;
        border-left: 1px solid var(--border);
    }
    .status-badge {
        font-family: var(--mono);
        font-size: 0.6rem;
        letter-spacing: 2px;
        padding: 3px 8px;
        border: 1px solid;
    }
    .sb-menunggu { color: var(--amber); border-color: var(--amber); background: rgba(240,192,64,0.06); }
    .sb-diproses { color: var(--cyan);  border-color: var(--cyan);  background: rgba(0,255,224,0.06); }
    .sb-selesai  { color: var(--neon);  border-color: var(--neon);  background: rgba(57,255,128,0.06); }
    .q-time {
        font-family: var(--mono);
        font-size: 0.58rem;
        color: var(--muted);
    }

    /* ── CHEF PANEL ── */
    .chef-wrap {
        border: 1px solid var(--border);
        background: var(--surface);
        position: relative;
        padding: 28px 32px;
    }
    .chef-wrap::before {
        content: 'ACTIVE ORDER';
        position: absolute;
        top: -1px; left: 28px;
        background: var(--neon);
        color: #000;
        font-family: var(--mono);
        font-size: 0.55rem;
        letter-spacing: 3px;
        padding: 3px 10px;
    }
    .chef-num {
        font-family: var(--display);
        font-size: 6rem;
        line-height: 1;
        letter-spacing: 4px;
        color: rgba(255,255,255,0.06);
        position: absolute;
        right: 24px;
        top: 20px;
        user-select: none;
    }
    .chef-nama {
        font-family: var(--display);
        font-size: 2.2rem;
        letter-spacing: 3px;
        color: #fff;
        margin-top: 24px;
    }
    .chef-detail-row {
        display: grid;
        grid-template-columns: 60px 1fr;
        gap: 4px 12px;
        margin-top: 14px;
        font-family: var(--mono);
        font-size: 0.72rem;
    }
    .chef-key { color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
    .chef-val { color: var(--text); }
    .chef-status-bar {
        margin-top: 20px;
        height: 2px;
        background: var(--border);
        position: relative;
        overflow: hidden;
    }
    .chef-status-bar-fill {
        position: absolute;
        left: 0; top: 0; bottom: 0;
        transition: width 0.5s ease;
    }
    .fill-menunggu { width: 20%; background: var(--amber); }
    .fill-diproses { width: 60%; background: var(--cyan); animation: scan 1.8s linear infinite; }
    .fill-selesai  { width: 100%; background: var(--neon); }
    @keyframes scan {
        0%   { width: 40%; margin-left: 0; }
        50%  { width: 20%; margin-left: 80%; }
        100% { width: 40%; margin-left: 0; }
    }

    /* ── FORM ── */
    .form-wrap {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 24px;
        position: relative;
    }
    .form-wrap::before {
        content: 'NEW ORDER';
        position: absolute;
        top: -1px; left: 20px;
        background: var(--amber);
        color: #000;
        font-family: var(--mono);
        font-size: 0.55rem;
        letter-spacing: 3px;
        padding: 3px 10px;
    }
    .stTextInput input {
        background: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
        color: var(--text) !important;
        font-family: var(--mono) !important;
        font-size: 0.85rem !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus {
        border-color: var(--neon) !important;
        box-shadow: 0 0 0 1px var(--neon-dim) !important;
    }
    .stTextInput label { font-family: var(--mono) !important; font-size: 0.65rem !important; letter-spacing: 2px !important; color: var(--muted) !important; }

    /* menu checkbox grid */
    .menu-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2px;
        margin: 14px 0;
    }
    .stCheckbox label {
        font-family: var(--mono) !important;
        font-size: 0.72rem !important;
        color: var(--text) !important;
        gap: 8px !important;
    }
    .stCheckbox [data-baseweb="checkbox"] {
        border-radius: 0 !important;
    }

    /* total bar */
    .total-display {
        border: 1px solid var(--neon-dim);
        background: rgba(57,255,128,0.04);
        padding: 14px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 10px 0;
    }
    .total-lbl { font-family: var(--mono); font-size: 0.62rem; letter-spacing: 2px; color: var(--muted); }
    .total-val { font-family: var(--display); font-size: 1.6rem; letter-spacing: 2px; color: var(--neon); }

    /* ── BUTTONS ── */
    .stButton > button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
        color: var(--text) !important;
        font-family: var(--mono) !important;
        font-size: 0.68rem !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        padding: 12px 20px !important;
        width: 100% !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        border-color: var(--neon) !important;
        color: var(--neon) !important;
        background: var(--neon-dim) !important;
    }
    .stButton > button[kind="primary"] {
        border-color: var(--neon) !important;
        color: var(--neon) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: rgba(57,255,128,0.12) !important;
        box-shadow: 0 0 16px rgba(57,255,128,0.1) !important;
    }

    /* ── BANNER CALL ── */
    .call-banner {
        border: 1px solid var(--cyan);
        background: rgba(0,255,224,0.04);
        padding: 18px 24px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
        animation: flashBorder 0.5s ease 5;
    }
    @keyframes flashBorder {
        0%,100% { border-color: var(--cyan); }
        50%      { border-color: transparent; }
    }
    .call-banner::before {
        content: 'BROADCAST';
        position: absolute;
        top: -1px; left: 16px;
        background: var(--cyan);
        color: #000;
        font-family: var(--mono);
        font-size: 0.55rem;
        letter-spacing: 3px;
        padding: 3px 10px;
    }
    .call-text {
        font-family: var(--display);
        font-size: 1.4rem;
        letter-spacing: 3px;
        color: var(--cyan);
        margin-top: 8px;
    }

    /* ── NOTIF override ── */
    div[data-testid="stNotification"],
    .stAlert {
        border-radius: 0 !important;
        border-left: 2px solid var(--neon) !important;
        background: rgba(57,255,128,0.04) !important;
        font-family: var(--mono) !important;
        font-size: 0.75rem !important;
    }

    /* ── RIWAYAT ── */
    .hist-row {
        display: grid;
        grid-template-columns: 50px 1fr auto auto;
        gap: 0 16px;
        align-items: center;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border);
        font-family: var(--mono);
        font-size: 0.72rem;
        transition: background 0.15s;
    }
    .hist-row:hover { background: var(--surface2); }
    .hist-num { color: var(--muted); }
    .hist-nama { color: var(--text); }
    .hist-menu { color: var(--muted); font-size: 0.62rem; }
    .hist-harga { color: var(--neon); text-align: right; }
    .hist-time { color: var(--muted); font-size: 0.6rem; text-align: right; }

    .omzet-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 16px;
        border: 1px solid var(--border);
        background: var(--surface);
        margin-bottom: 2px;
    }
    .omzet-lbl { font-family: var(--mono); font-size: 0.62rem; letter-spacing: 2px; color: var(--muted); }
    .omzet-val { font-family: var(--display); font-size: 1.8rem; letter-spacing: 2px; color: var(--red); }

    /* ── SECTION LABEL ── */
    .sec-label {
        font-family: var(--mono);
        font-size: 0.6rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: var(--muted);
        padding: 10px 0 8px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 10px;
    }

    /* hide streamlit chrome */
    footer, header { display: none !important; }
    .stDivider { border-color: var(--border) !important; }
    div[data-testid="stVerticalBlock"] > div > .element-container { margin-bottom: 0 !important; }
    </style>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  RENDER: HEADER
# ════════════════════════════════════════════════════════

def render_header() -> None:
    st.markdown("""
    <div class="app-header">
        <div class="corner-tl"></div>
        <div class="app-header-sys">SYS // FOOD-QUEUE-v2 // FIFO ACTIVE</div>
        <h1>ANTRIAN<span>_</span>MAKANAN</h1>
        <div class="app-header-sub">
            COLLECTIONS.DEQUE &nbsp;&bull;&nbsp; GTTS ID &nbsp;&bull;&nbsp; STREAMLIT
        </div>
        <div class="corner-br"></div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  RENDER: METRIK
# ════════════════════════════════════════════════════════

def render_metrik(antrian: AntrianPesanan) -> None:
    terdepan  = antrian.pesanan_terdepan()
    nama_aktif = terdepan.nama.upper() if terdepan else "—"
    omzet_str  = f"Rp {antrian.omzet:,}".replace(",", ".")

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-cell c-antrian">
            <div class="metric-lbl">Queue&nbsp;&nbsp;/&nbsp;&nbsp;menunggu</div>
            <div class="metric-val">{antrian.jumlah_antrian:02d}</div>
        </div>
        <div class="metric-cell c-proses">
            <div class="metric-lbl">Aktif&nbsp;&nbsp;/&nbsp;&nbsp;diproses</div>
            <div class="metric-val">{nama_aktif}</div>
        </div>
        <div class="metric-cell c-selesai">
            <div class="metric-lbl">Done&nbsp;&nbsp;/&nbsp;&nbsp;selesai</div>
            <div class="metric-val">{antrian.jumlah_selesai:02d}</div>
        </div>
        <div class="metric-cell c-omzet">
            <div class="metric-lbl">Revenue&nbsp;&nbsp;/&nbsp;&nbsp;total</div>
            <div class="metric-val">{omzet_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  RENDER: BANNER + AUDIO
# ════════════════════════════════════════════════════════

def render_banner_audio() -> None:
    if not st.session_state.audio_b64:
        return

    teks = st.session_state.banner_teks or "Pesanan siap diambil"
    st.markdown(f"""
    <div class="call-banner">
        <div class="call-text">{teks.upper()}</div>
    </div>
    <audio autoplay="true">
        <source src="data:audio/mp3;base64,{st.session_state.audio_b64}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

    st.session_state.audio_b64   = None
    st.session_state.banner_teks = None


# ════════════════════════════════════════════════════════
#  RENDER: NOTIFIKASI
# ════════════════════════════════════════════════════════

def render_notif() -> None:
    if st.session_state.notif:
        tipe, pesan = st.session_state.notif
        getattr(st, tipe)(pesan)
        st.session_state.notif = None


# ════════════════════════════════════════════════════════
#  RENDER: ANTRIAN
# ════════════════════════════════════════════════════════

def render_antrian(antrian: AntrianPesanan) -> None:
    st.markdown('<div class="sec-label">QUEUE MONITOR</div>', unsafe_allow_html=True)

    if antrian.kosong:
        st.markdown("""
        <div style="padding:28px 20px;border:1px dashed rgba(255,255,255,0.05);
                    text-align:center;font-family:'Share Tech Mono',monospace;
                    font-size:0.68rem;letter-spacing:2px;color:#3a4a40;">
            NO ORDERS IN QUEUE
        </div>
        """, unsafe_allow_html=True)
        return

    for idx, p in enumerate(antrian.antrian):
        top_cls  = "top" if idx == 0 else ""
        st_cls   = f"s-{p.status}"
        sb_cls   = f"sb-{p.status}"
        badge    = STATUS_LABEL.get(p.status, p.status)
        posisi   = "HEAD" if idx == 0 else f"Q{idx+1:02d}"

        st.markdown(f"""
        <div class="q-card {top_cls} {st_cls}">
            <div class="q-num">
                <span style="font-size:0.6rem;font-family:'Share Tech Mono',monospace;
                             letter-spacing:1px;color:#3a4a40;display:block;text-align:center">
                    {posisi}
                </span>
                #{p.nomor:03d}
            </div>
            <div class="q-body">
                <div class="q-nama">{p.nama.upper()}</div>
                <div class="q-menu">{p.menu_str}</div>
                <div class="q-harga">{p.harga_str}</div>
            </div>
            <div class="q-meta">
                <span class="status-badge {sb_cls}">{badge}</span>
                <span class="q-time">{p.waktu_pesan}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  RENDER: FORM PESAN
# ════════════════════════════════════════════════════════

def render_form_pesan(antrian: AntrianPesanan) -> None:
    st.markdown('<div class="sec-label">INPUT ORDER</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-wrap">', unsafe_allow_html=True)

    nama = st.text_input(
        "NAMA PELANGGAN",
        placeholder="masukkan nama...",
        key="input_nama",
    )

    st.markdown(
        "<div style='font-family:\"Share Tech Mono\",monospace;font-size:0.62rem;"
        "letter-spacing:2px;color:#3a4a40;margin:14px 0 8px'>PILIH MENU</div>",
        unsafe_allow_html=True
    )

    menu_dipilih: list[str] = []
    cols = st.columns(2)
    for i, (item, harga) in enumerate(MENU_TERSEDIA.items()):
        harga_fmt = f"Rp {harga:,}".replace(",", ".")
        with cols[i % 2]:
            if st.checkbox(f"{item}  [{harga_fmt}]", key=f"menu_{i}"):
                menu_dipilih.append(item)

    if menu_dipilih:
        total     = sum(MENU_TERSEDIA[m] for m in menu_dipilih)
        total_fmt = f"Rp {total:,}".replace(",", ".")
        st.markdown(f"""
        <div class="total-display">
            <span class="total-lbl">{len(menu_dipilih)} ITEM &nbsp;/&nbsp; TOTAL</span>
            <span class="total-val">{total_fmt}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("TAMBAH KE ANTRIAN", key="btn_pesan", type="primary"):
        if not nama.strip():
            st.session_state.notif = ("error", "NAMA PELANGGAN TIDAK BOLEH KOSONG")
        elif not menu_dipilih:
            st.session_state.notif = ("error", "PILIH MINIMAL SATU MENU")
        else:
            p = antrian.tambah_pesanan(nama.strip(), menu_dipilih)
            st.session_state.notif = (
                "success",
                f"ORDER #{p.nomor:03d} — {p.nama.upper()} — MASUK ANTRIAN",
            )
            st.rerun()


# ════════════════════════════════════════════════════════
#  RENDER: PANEL CHEF
# ════════════════════════════════════════════════════════

def render_panel_chef(antrian: AntrianPesanan) -> None:
    st.markdown('<div class="sec-label">CHEF STATION</div>', unsafe_allow_html=True)
    p = antrian.pesanan_terdepan()

    if not p:
        st.markdown("""
        <div style="padding:48px 20px;border:1px dashed rgba(255,255,255,0.05);
                    text-align:center;font-family:'Share Tech Mono',monospace;
                    font-size:0.68rem;letter-spacing:3px;color:#3a4a40;">
            IDLE — NO ACTIVE ORDER
        </div>
        """, unsafe_allow_html=True)
        return

    fill_cls = f"fill-{p.status}"
    st.markdown(f"""
    <div class="chef-wrap">
        <div class="chef-num">{p.nomor:03d}</div>
        <div class="chef-nama">{p.nama.upper()}</div>
        <div class="chef-detail-row">
            <span class="chef-key">MENU</span>
            <span class="chef-val">{p.menu_str}</span>
            <span class="chef-key">TOTAL</span>
            <span class="chef-val">{p.harga_str}</span>
            <span class="chef-key">WAKTU</span>
            <span class="chef-val">{p.waktu_pesan}</span>
            <span class="chef-key">STATUS</span>
            <span class="chef-val" style="color:var(--{'cyan' if p.status=='diproses' else 'amber' if p.status=='menunggu' else 'neon'})">
                {STATUS_LABEL.get(p.status, p.status)}
            </span>
        </div>
        <div class="chef-status-bar">
            <div class="chef-status-bar-fill {fill_cls}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        if st.button("MULAI PROSES", key="btn_proses"):
            hasil = antrian.mulai_proses()
            if hasil:
                st.session_state.notif = (
                    "info",
                    f"PROCESSING — #{hasil.nomor:03d} {hasil.nama.upper()}",
                )
                st.rerun()

    with c2:
        if st.button("SELESAI + PANGGIL", key="btn_selesai", type="primary"):
            selesai = antrian.selesaikan_dan_panggil()
            if selesai:
                with st.spinner("generating announcement..."):
                    try:
                        st.session_state.audio_b64 = buat_audio_b64(selesai)
                        st.session_state.banner_teks = (
                            f"No. {selesai.nomor:03d} — {selesai.nama} — "
                            f"pesanan siap diambil"
                        )
                    except Exception as err:
                        st.session_state.notif = (
                            "warning",
                            f"AUDIO ERROR: {err} — order tetap selesai",
                        )
                st.session_state.notif = (
                    "success",
                    f"ORDER #{selesai.nomor:03d} — {selesai.nama.upper()} — SELESAI",
                )
                st.rerun()


# ════════════════════════════════════════════════════════
#  RENDER: RIWAYAT
# ════════════════════════════════════════════════════════

def render_riwayat(antrian: AntrianPesanan) -> None:
    st.markdown('<div class="sec-label">COMPLETED ORDERS</div>', unsafe_allow_html=True)

    if not antrian.riwayat:
        st.markdown("""
        <div style="padding:40px 20px;border:1px dashed rgba(255,255,255,0.05);
                    text-align:center;font-family:'Share Tech Mono',monospace;
                    font-size:0.68rem;letter-spacing:2px;color:#3a4a40;">
            NO COMPLETED ORDERS YET
        </div>
        """, unsafe_allow_html=True)
        return

    omzet_str = f"Rp {antrian.omzet:,}".replace(",", ".")
    st.markdown(f"""
    <div class="omzet-bar">
        <span class="omzet-lbl">TOTAL REVENUE / HARI INI</span>
        <span class="omzet-val">{omzet_str}</span>
    </div>
    """, unsafe_allow_html=True)

    rows_html = ""
    for p in antrian.riwayat:
        rows_html += f"""
        <div class="hist-row">
            <span class="hist-num">#{p.nomor:03d}</span>
            <div>
                <div class="hist-nama">{p.nama.upper()}</div>
                <div class="hist-menu">{p.menu_str}</div>
            </div>
            <span class="hist-harga">{p.harga_str}</span>
            <span class="hist-time">{p.waktu_pesan}</span>
        </div>
        """
    st.markdown(f'<div style="border:1px solid var(--border)">{rows_html}</div>', unsafe_allow_html=True)

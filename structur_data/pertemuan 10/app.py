import streamlit as st
from stack_backend import StackLinkedList, cek_kurung, balik_string

st.set_page_config(
    page_title="Stack Visualizer",
    page_icon="🗡️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }

    .stApp {
        background-color: #0a0a0f;
        background-image:
            radial-gradient(ellipse at 20% 20%, rgba(255, 80, 0, 0.06) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 80%, rgba(0, 200, 255, 0.05) 0%, transparent 60%);
    }

    .main-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2.8rem;
        color: #ff5000;
        text-align: center;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 4px;
        text-shadow: 0 0 30px rgba(255,80,0,0.5);
    }

    .sub-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        color: #444;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 40px;
    }

    .section-header {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #ff5000;
        letter-spacing: 4px;
        text-transform: uppercase;
        border-bottom: 1px solid #1a1a2e;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }

    .stack-container {
        background: #0d0d1a;
        border: 1px solid #1a1a2e;
        border-radius: 4px;
        padding: 20px;
        min-height: 400px;
        position: relative;
    }

    .stack-item {
        background: linear-gradient(135deg, #12122a, #1a1a35);
        border: 1px solid #2a2a4a;
        border-left: 3px solid #ff5000;
        border-radius: 3px;
        padding: 12px 18px;
        margin: 6px 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1rem;
        color: #e0e0ff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s;
    }

    .stack-item:first-child {
        border-left-color: #00c8ff;
        background: linear-gradient(135deg, #0a1a2a, #0d1f35);
        box-shadow: 0 0 15px rgba(0,200,255,0.1);
    }

    .stack-top-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #00c8ff;
        letter-spacing: 3px;
        background: rgba(0,200,255,0.1);
        padding: 2px 8px;
        border-radius: 2px;
    }

    .stack-index {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #333;
    }

    .stack-empty {
        text-align: center;
        color: #222;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 3px;
        padding: 60px 0;
    }

    .stat-card {
        background: #0d0d1a;
        border: 1px solid #1a1a2e;
        border-radius: 4px;
        padding: 16px;
        text-align: center;
    }

    .stat-value {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2rem;
        color: #ff5000;
        line-height: 1;
    }

    .stat-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #444;
        letter-spacing: 3px;
        margin-top: 6px;
    }

    .log-item {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.78rem;
        padding: 6px 12px;
        border-radius: 3px;
        margin: 4px 0;
    }

    .log-push { background: rgba(255,80,0,0.08); color: #ff8040; border-left: 2px solid #ff5000; }
    .log-pop  { background: rgba(0,200,255,0.08); color: #40c8ff; border-left: 2px solid #00c8ff; }
    .log-info { background: rgba(255,255,255,0.03); color: #555; border-left: 2px solid #222; }
    .log-ok   { background: rgba(0,255,100,0.06); color: #40ff80; border-left: 2px solid #00c864; }
    .log-err  { background: rgba(255,0,0,0.08); color: #ff4040; border-left: 2px solid #ff0000; }

    .result-box {
        background: #0d0d1a;
        border: 1px solid #1a1a2e;
        border-radius: 4px;
        padding: 20px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1rem;
        color: #e0e0ff;
        text-align: center;
        margin-top: 12px;
    }

    .result-ok   { border-color: #00c864; color: #40ff80; }
    .result-fail { border-color: #ff0000; color: #ff4040; }

    div[data-testid="stButton"] button {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 3px;
        border: 1px solid #ff5000;
        background: transparent;
        color: #ff5000;
        padding: 8px 20px;
        transition: all 0.2s;
        width: 100%;
    }

    div[data-testid="stButton"] button:hover {
        background: rgba(255,80,0,0.15);
        box-shadow: 0 0 12px rgba(255,80,0,0.3);
    }

    div[data-testid="stTextInput"] input {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        background: #0d0d1a;
        border: 1px solid #1a1a2e;
        border-radius: 3px;
        color: #e0e0ff;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #ff5000;
        box-shadow: 0 0 8px rgba(255,80,0,0.2);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #0a0a0f;
        border-bottom: 1px solid #1a1a2e;
        gap: 0;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 3px;
        color: #444;
        background: transparent;
        border: none;
        padding: 12px 24px;
        text-transform: uppercase;
    }

    .stTabs [aria-selected="true"] {
        color: #ff5000 !important;
        border-bottom: 2px solid #ff5000 !important;
        background: transparent !important;
    }

    hr { border-color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

if "stack" not in st.session_state:
    st.session_state.stack = StackLinkedList()
if "log" not in st.session_state:
    st.session_state.log = []

def add_log(msg, kind="info"):
    st.session_state.log.insert(0, (msg, kind))
    if len(st.session_state.log) > 30:
        st.session_state.log.pop()


st.markdown('<div class="main-title">⚔ STACK VISUALIZER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">LINKED LIST · DATA STRUCTURE · VISUALIZER</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["STACK OPERATIONS", "CEK KURUNG", "BALIK STRING"])

with tab1:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-header">// OPERASI</div>', unsafe_allow_html=True)

        push_val = st.text_input("", placeholder="Masukkan nilai...", key="push_input", label_visibility="collapsed")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬆ PUSH"):
                if push_val.strip():
                    st.session_state.stack.push(push_val.strip())
                    add_log(f"PUSH → '{push_val.strip()}'", "push")
                else:
                    add_log("Input kosong, push dibatalkan", "err")

        with c2:
            if st.button("⬇ POP"):
                try:
                    val = st.session_state.stack.pop()
                    add_log(f"POP ← '{val}'", "pop")
                except IndexError as e:
                    add_log(str(e), "err")

        c3, c4 = st.columns(2)
        with c3:
            if st.button("👁 PEEK"):
                try:
                    val = st.session_state.stack.peek()
                    add_log(f"PEEK → '{val}' (top)", "info")
                except IndexError as e:
                    add_log(str(e), "err")

        with c4:
            if st.button("🗑 CLEAR"):
                st.session_state.stack.clear()
                add_log("Stack dikosongkan", "info")

        if st.button("🔁 REVERSE"):
            if not st.session_state.stack.is_empty():
                st.session_state.stack.reverse()
                add_log("Stack dibalik", "info")
            else:
                add_log("Stack kosong, tidak bisa reverse", "err")

        search_val = st.text_input("", placeholder="Cari nilai...", key="search_input", label_visibility="collapsed")
        if st.button("🔍 SEARCH"):
            if search_val.strip():
                found = st.session_state.stack.contains(search_val.strip())
                if found:
                    add_log(f"'{search_val.strip()}' DITEMUKAN di stack", "ok")
                else:
                    add_log(f"'{search_val.strip()}' TIDAK ditemukan", "err")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">// STATISTIK</div>', unsafe_allow_html=True)

        s = st.session_state.stack
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{s.size()}</div>
                <div class="stat-label">SIZE</div>
            </div>""", unsafe_allow_html=True)
        with sc2:
            top_val = s.peek() if not s.is_empty() else "-"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="font-size:1.4rem">{top_val}</div>
                <div class="stat-label">TOP</div>
            </div>""", unsafe_allow_html=True)
        with sc3:
            status = "YES" if s.is_empty() else "NO"
            color = "#00c864" if s.is_empty() else "#ff5000"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color:{color};font-size:1.4rem">{status}</div>
                <div class="stat-label">EMPTY?</div>
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">// VISUALISASI STACK</div>', unsafe_allow_html=True)

        items = st.session_state.stack.to_list()
        stack_html = '<div class="stack-container">'

        if not items:
            stack_html += '<div class="stack-empty">[ STACK KOSONG ]</div>'
        else:
            for i, item in enumerate(items):
                if i == 0:
                    stack_html += f"""
                    <div class="stack-item">
                        <span>{item}</span>
                        <span class="stack-top-label">TOP</span>
                    </div>"""
                else:
                    stack_html += f"""
                    <div class="stack-item">
                        <span>{item}</span>
                        <span class="stack-index">#{i}</span>
                    </div>"""

        stack_html += '</div>'
        st.markdown(stack_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">// ACTIVITY LOG</div>', unsafe_allow_html=True)

        log_html = ""
        for msg, kind in st.session_state.log[:8]:
            log_html += f'<div class="log-item log-{kind}">{msg}</div>'

        if not log_html:
            log_html = '<div class="log-item log-info">Belum ada aktivitas...</div>'

        st.markdown(log_html, unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="section-header">// CEK KURUNG SEIMBANG</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        ekspresi = st.text_input("", placeholder="Contoh: ({[]})", key="kurung_input", label_visibility="collapsed")

        if st.button("🔎 CEK SEKARANG"):
            if ekspresi.strip():
                valid, sisa = cek_kurung(ekspresi.strip())
                st.session_state["kurung_result"] = (ekspresi.strip(), valid, sisa)
            else:
                st.warning("Masukkan ekspresi terlebih dahulu!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">// CONTOH EKSPRESI</div>', unsafe_allow_html=True)
        contoh = ["({[]})", "((()))", "({[})", "((())", "{[()]}"]
        for c in contoh:
            valid, _ = cek_kurung(c)
            icon = "✓" if valid else "✗"
            color = "#40ff80" if valid else "#ff4040"
            st.markdown(f'<div class="log-item" style="color:{color}; border-left: 2px solid {color}; background: rgba(255,255,255,0.02)">{icon} &nbsp; <code>{c}</code></div>', unsafe_allow_html=True)

    with col_b:
        if "kurung_result" in st.session_state:
            eksp, valid, sisa = st.session_state["kurung_result"]
            status_class = "result-ok" if valid else "result-fail"
            status_text  = "✓ SEIMBANG" if valid else "✗ TIDAK SEIMBANG"
            st.markdown(f"""
            <div class="result-box {status_class}">
                <div style="font-size:0.75rem;letter-spacing:3px;opacity:0.6;margin-bottom:8px">EKSPRESI</div>
                <div style="font-size:1.4rem;margin-bottom:16px">{eksp}</div>
                <div style="font-size:1.8rem">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)

            if sisa:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">// SISA DI STACK</div>', unsafe_allow_html=True)
                for item in sisa:
                    st.markdown(f'<div class="stack-item"><span>{item}</span><span class="stack-index">sisa</span></div>', unsafe_allow_html=True)


with tab3:
    st.markdown('<div class="section-header">// BALIK STRING DENGAN STACK</div>', unsafe_allow_html=True)

    col_x, col_y = st.columns([1, 1], gap="large")

    with col_x:
        teks_input = st.text_input("", placeholder="Masukkan teks...", key="balik_input", label_visibility="collapsed")

        if st.button("🔄 BALIK SEKARANG"):
            if teks_input.strip():
                hasil = balik_string(teks_input)
                st.session_state["balik_result"] = (teks_input, hasil)
            else:
                st.warning("Masukkan teks terlebih dahulu!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">// CARA KERJA</div>', unsafe_allow_html=True)
        steps = [
            "1. Setiap karakter di-PUSH ke stack",
            "2. Stack bersifat LIFO (Last In First Out)",
            "3. POP semua elemen → urutan terbalik",
            "4. Gabungkan hasil POP menjadi string"
        ]
        for s in steps:
            st.markdown(f'<div class="log-item log-info">{s}</div>', unsafe_allow_html=True)

    with col_y:
        if "balik_result" in st.session_state:
            asli, hasil = st.session_state["balik_result"]
            st.markdown(f"""
            <div class="result-box">
                <div style="font-size:0.75rem;letter-spacing:3px;opacity:0.5;margin-bottom:6px">INPUT</div>
                <div style="font-size:1.3rem;margin-bottom:20px;color:#e0e0ff">{asli}</div>
                <div style="font-size:0.75rem;letter-spacing:3px;opacity:0.5;margin-bottom:6px">OUTPUT</div>
                <div style="font-size:1.3rem;color:#ff5000">{hasil}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">// PROSES PUSH</div>', unsafe_allow_html=True)
            for i, char in enumerate(asli):
                st.markdown(f'<div class="log-item log-push">PUSH [{i}] → "{char}"</div>', unsafe_allow_html=True)
            st.markdown('<div class="log-item log-pop">POP ALL → hasil dibalik ✓</div>', unsafe_allow_html=True)

import streamlit as st
from gtts import gTTS
import base64
import io

# ========================
# FUNGSI gTTS → BROWSER
# ========================

def bicara(teks):
    tts = gTTS(text=teks, lang='id')
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    audio_html = f"""
        <audio autoplay style="display:none">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# ========================
# BACKEND: NODE & QUEUE
# ========================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.ukuran = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        node_baru = Node(data)
        if self.rear is None:
            self.front = node_baru
            self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self.ukuran += 1

    def dequeue(self):
        if self.is_empty():
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.ukuran -= 1
        return data

    def peek(self):
        if self.is_empty():
            return None
        return self.front.data

    def size(self):
        return self.ukuran

    def to_list(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result


# ========================
# STREAMLIT CONFIG
# ========================

st.set_page_config(
    page_title="Queue Visualizer",
    page_icon="🔗",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0d0d0d; color: #f0f0f0; }
h1, h2, h3 { font-family: 'JetBrains Mono', monospace !important; color: #00ff88 !important; }

.queue-container {
    display: flex; align-items: center; flex-wrap: wrap;
    padding: 20px 10px; min-height: 100px;
    background: #1a1a1a; border-radius: 12px;
    border: 1px solid #2a2a2a; margin: 10px 0;
}
.queue-node { display: flex; align-items: center; }
.node-box {
    background: #1e1e2e; border: 2px solid #00ff88;
    border-radius: 8px; padding: 10px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px; font-weight: 700; color: #00ff88;
    box-shadow: 0 0 12px rgba(0,255,136,0.2);
}
.node-box.front { border-color: #ff6b6b; color: #ff6b6b; box-shadow: 0 0 12px rgba(255,107,107,0.3); }
.node-box.rear  { border-color: #ffd93d; color: #ffd93d; box-shadow: 0 0 12px rgba(255,217,61,0.3); }
.node-box.both  { border-color: #c084fc; color: #c084fc; box-shadow: 0 0 12px rgba(192,132,252,0.3); }
.arrow { font-size: 20px; color: #555; padding: 0 4px; }
.node-label { font-size: 11px; font-family: 'JetBrains Mono', monospace; text-align: center; margin-top: 4px; }
.label-front { color: #ff6b6b; } .label-rear { color: #ffd93d; } .label-both { color: #c084fc; }

.stat-card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 10px; padding: 14px 18px; text-align: center; }
.stat-value { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700; color: #00ff88; }
.stat-label { font-size: 12px; color: #666; margin-top: 4px; }

.log-entry { font-family: 'JetBrains Mono', monospace; font-size: 13px; padding: 6px 12px; border-radius: 6px; margin-bottom: 4px; }
.log-enqueue { background: rgba(0,255,136,0.08); color: #00ff88; border-left: 3px solid #00ff88; }
.log-dequeue { background: rgba(255,107,107,0.08); color: #ff6b6b; border-left: 3px solid #ff6b6b; }
.log-info    { background: rgba(100,100,100,0.1); color: #888; border-left: 3px solid #444; }
.empty-state { text-align: center; color: #444; font-family: 'JetBrains Mono', monospace; font-size: 14px; padding: 20px; width: 100%; }
</style>
""", unsafe_allow_html=True)


# ========================
# SESSION STATE
# ========================

if "queue" not in st.session_state:
    st.session_state.queue = Queue()
if "log" not in st.session_state:
    st.session_state.log = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

q = st.session_state.queue


# ========================
# HEADER
# ========================

st.markdown("## 🔗 Queue — Linked List")
st.markdown("<p style='color:#666; font-family:JetBrains Mono; font-size:13px;'>Visualisasi struktur data queue berbasis linked list dengan suara gTTS</p>", unsafe_allow_html=True)
st.divider()


# ========================
# STATISTIK
# ========================

items = q.to_list()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-value">{q.size()}</div>
        <div class="stat-label">Ukuran Queue</div>
    </div>""", unsafe_allow_html=True)

with col2:
    front_val = q.peek() if not q.is_empty() else "—"
    st.markdown(f"""<div class="stat-card">
        <div class="stat-value" style="color:#ff6b6b">{front_val}</div>
        <div class="stat-label">Front (Depan)</div>
    </div>""", unsafe_allow_html=True)

with col3:
    rear_val = items[-1] if items else "—"
    st.markdown(f"""<div class="stat-card">
        <div class="stat-value" style="color:#ffd93d">{rear_val}</div>
        <div class="stat-label">Rear (Belakang)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ========================
# VISUALISASI QUEUE
# ========================

st.markdown("### Visualisasi")

if q.is_empty():
    st.markdown("""<div class="queue-container">
        <div class="empty-state">[ Queue Kosong ]</div>
    </div>""", unsafe_allow_html=True)
else:
    nodes_html = ""
    for i, item in enumerate(items):
        is_front = i == 0
        is_rear = i == len(items) - 1

        if is_front and is_rear:
            css_class, label_class, label_text = "both", "label-both", "FRONT & REAR"
        elif is_front:
            css_class, label_class, label_text = "front", "label-front", "FRONT"
        elif is_rear:
            css_class, label_class, label_text = "rear", "label-rear", "REAR"
        else:
            css_class, label_class, label_text = "", "", ""

        nodes_html += f"""
        <div class="queue-node">
            <div>
                <div class="node-box {css_class}">{item}</div>
                <div class="node-label {label_class}">{label_text}</div>
            </div>
        """
        if i < len(items) - 1:
            nodes_html += '<span class="arrow">→</span>'
        nodes_html += "</div>"

    st.markdown(f'<div class="queue-container">{nodes_html}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ========================
# PUTAR AUDIO (setelah rerun)
# ========================

if st.session_state.last_audio:
    bicara(st.session_state.last_audio)
    st.session_state.last_audio = None


# ========================
# KONTROL
# ========================

st.markdown("### Operasi")
tab1, tab2, tab3 = st.tabs(["➕ Enqueue", "➖ Dequeue", "🔄 Lainnya"])

with tab1:
    input_data = st.text_input("Masukkan nilai:", placeholder="contoh: A, 42, Hello")
    if st.button("Enqueue", type="primary", use_container_width=True):
        if input_data.strip():
            val = input_data.strip()
            q.enqueue(val)
            st.session_state.log.insert(0, ("enqueue", f"✓ Enqueue: {val}"))
            st.session_state.last_audio = f"Enqueue {val} berhasil ditambahkan ke queue"
            st.rerun()
        else:
            st.warning("Masukkan nilai terlebih dahulu!")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Dequeue (Hapus dari Depan)", type="secondary", use_container_width=True):
        if q.is_empty():
            st.session_state.log.insert(0, ("info", "✗ Dequeue gagal — queue kosong"))
            st.session_state.last_audio = "Queue sedang kosong, tidak bisa dequeue"
        else:
            data = q.dequeue()
            st.session_state.log.insert(0, ("dequeue", f"✗ Dequeue: {data}"))
            st.session_state.last_audio = f"Dequeue {data} berhasil dikeluarkan dari queue"
        st.rerun()

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Isi Contoh Data", use_container_width=True):
            for item in ["A", "B", "C", "D", "E"]:
                q.enqueue(item)
                st.session_state.log.insert(0, ("enqueue", f"✓ Enqueue: {item}"))
            st.session_state.last_audio = "Contoh data A B C D E berhasil ditambahkan ke queue"
            st.rerun()
    with col_b:
        if st.button("Reset Queue", use_container_width=True):
            st.session_state.queue = Queue()
            st.session_state.log.insert(0, ("info", "↺ Queue direset"))
            st.session_state.last_audio = "Queue telah direset"
            st.rerun()


# ========================
# LOG AKTIVITAS
# ========================

st.divider()
st.markdown("### Log Aktivitas")

if not st.session_state.log:
    st.markdown("<p style='color:#444; font-family:JetBrains Mono; font-size:13px;'>Belum ada aktivitas.</p>", unsafe_allow_html=True)
else:
    for kind, msg in st.session_state.log[:10]:
        css = "log-enqueue" if kind == "enqueue" else ("log-dequeue" if kind == "dequeue" else "log-info")
        st.markdown(f'<div class="log-entry {css}">{msg}</div>', unsafe_allow_html=True)
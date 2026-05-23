# app.py — Backend Graf + Frontend Streamlit (1 file)
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ╔══════════════════════════════════════════════════════╗
# ║                  BACKEND — CLASS GRAF                ║
# ╚══════════════════════════════════════════════════════╝

class Graf:
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph.add_node(vertex)
            return True
        return False
        
    def add_edge(self, v1, v2, w):
        if self.graph.has_node(v1) and self.graph.has_node(v2):
            self.graph.add_edge(v1, v2, weight=w)
        return False
    
    def get_graph(self):
        return self.graph
    
    def get_all_vertex(self):
        return self.graph.nodes()
    
    def get_all_edges(self):
        return self.graph.edges()
    
    def get_all_vertex_with_weight(self):
        return self.graph.edges(data='weight', default=1)
    
    def find_shortest_path(self, start, end):
        try:
            path = nx.shortest_path(self.graph, source=start, target=end, weight='weight')
            cost = nx.shortest_path_length(self.graph, source=start, target=end, weight='weight')
            return path, cost
        except nx.NetworkXNoPath:
            return None, 0
        except nx.NodeNotFound:
            return None, 0

    @property
    def adj_list(self):
        return nx.to_dict_of_dicts(self.graph)

    # ── Visualisasi ────────────────────────────────────
    def draw(self, highlight_path=None, title="Visualisasi Graf"):
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#0F172A")

        if self.graph.number_of_nodes() == 0:
            ax.text(0.5, 0.5, "Graf kosong.\nTambahkan simpul terlebih dahulu.",
                    ha="center", va="center", color="white", fontsize=13,
                    transform=ax.transAxes)
            ax.set_title(title, color="white", fontsize=14, fontweight="bold")
            ax.axis("off")
            return fig

        pos = nx.spring_layout(self.graph, seed=42)

        path_nodes = set(highlight_path) if highlight_path else set()
        start_node = highlight_path[0]  if highlight_path else None
        end_node   = highlight_path[-1] if highlight_path else None

        node_colors = []
        for node in self.graph.nodes():
            if node == start_node:   node_colors.append("#22C55E")
            elif node == end_node:   node_colors.append("#F59E0B")
            elif node in path_nodes: node_colors.append("#EF4444")
            else:                    node_colors.append("#3B82F6")

        path_edge_set = set()
        if highlight_path and len(highlight_path) > 1:
            for i in range(len(highlight_path) - 1):
                a, b = highlight_path[i], highlight_path[i+1]
                path_edge_set.add((a, b)); path_edge_set.add((b, a))

        edge_colors = []
        edge_widths = []
        for u, v in self.graph.edges():
            if (u, v) in path_edge_set:
                edge_colors.append("#EF4444"); edge_widths.append(3.5)
            else:
                edge_colors.append("#475569"); edge_widths.append(1.5)

        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors,
                               width=edge_widths, ax=ax, alpha=0.9)
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors,
                               node_size=700, ax=ax)
        nx.draw_networkx_labels(self.graph, pos, font_color="white",
                                font_size=11, font_weight="bold", ax=ax)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels,
                                     font_color="#FCD34D", font_size=9, ax=ax)

        legend_items = [mpatches.Patch(color="#3B82F6", label="Simpul biasa")]
        if highlight_path:
            legend_items += [
                mpatches.Patch(color="#22C55E", label=f"Awal  ({start_node})"),
                mpatches.Patch(color="#F59E0B", label=f"Akhir ({end_node})"),
                mpatches.Patch(color="#EF4444", label="Jalur terpendek"),
            ]
        ax.legend(handles=legend_items, loc="upper left", facecolor="#1E293B",
                  labelcolor="white", fontsize=9, framealpha=0.8)
        ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        plt.tight_layout()
        return fig


# ╔══════════════════════════════════════════════════════╗
# ║              FRONTEND — STREAMLIT UI                 ║
# ╚══════════════════════════════════════════════════════╝

st.set_page_config(page_title="Visualisasi Graf", page_icon="🔵", layout="wide")

st.markdown("""
<style>
    body, .stApp { background-color: #0F172A; color: #F1F5F9; }
    section[data-testid="stSidebar"] { background-color: #1E293B; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
        background-color: #334155; color: white; border: 1px solid #475569; border-radius: 8px;
    }
    .stButton>button {
        width: 100%; background-color: #3B82F6; color: white;
        border: none; border-radius: 8px; padding: 0.5rem; font-weight: bold;
    }
    .stButton>button:hover { background-color: #2563EB; }
    .metric-box {
        background: #1E293B; border: 1px solid #334155; border-radius: 10px;
        padding: 1rem; text-align: center;
    }
    .metric-val { font-size: 2rem; font-weight: 800; color: #3B82F6; }
    .metric-lbl { font-size: 0.8rem; color: #94A3B8; margin-top: 4px; }
    h1, h2, h3 { color: #F1F5F9 !important; }
    .path-box {
        background: #1E293B; border-left: 4px solid #22C55E;
        border-radius: 8px; padding: 1rem; margin-top: 0.5rem;
    }
    .stDataFrame { background-color: #1E293B; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────
if "graf" not in st.session_state:
    st.session_state.graf = Graf()
if "path_result" not in st.session_state:
    st.session_state.path_result = None
if "cost_result" not in st.session_state:
    st.session_state.cost_result = 0

g: Graf = st.session_state.graf

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔵 Graf Manager")
    st.divider()

    # ── Tambah Simpul ──────────────────────────────────
    st.markdown("### ➕ Tambah Simpul")
    new_vertex = st.text_input("Nama simpul", key="inp_vertex",
                               placeholder="Contoh: A, B, Kota1 …")
    if st.button("Tambah Simpul"):
        if new_vertex.strip():
            ok = g.add_vertex(new_vertex.strip().upper())
            if ok:
                st.success(f"Simpul **{new_vertex.upper()}** ditambahkan!")
                st.session_state.path_result = None
            else:
                st.warning(f"Simpul **{new_vertex.upper()}** sudah ada.")
        else:
            st.error("Nama simpul tidak boleh kosong.")

    st.divider()

    # ── Tambah Sisi ────────────────────────────────────
    st.markdown("### 🔗 Tambah Sisi")
    vertices = list(g.get_all_vertex())
    if len(vertices) < 2:
        st.info("Tambahkan minimal 2 simpul terlebih dahulu.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            v1 = st.selectbox("Dari", vertices, key="sel_v1")
        with col2:
            v2 = st.selectbox("Ke", vertices, key="sel_v2")
        weight = st.number_input("Bobot", min_value=1, max_value=999,
                                 value=1, step=1, key="inp_weight")
        if st.button("Tambah Sisi"):
            if v1 == v2:
                st.error("Simpul awal dan akhir tidak boleh sama.")
            elif g.graph.has_edge(v1, v2):
                st.warning(f"Sisi **{v1}–{v2}** sudah ada.")
            else:
                g.graph.add_edge(v1, v2, weight=weight)
                st.success(f"Sisi **{v1}–{v2}** (bobot {weight}) ditambahkan!")
                st.session_state.path_result = None

    st.divider()

    # ── Cari Jalur Terpendek ───────────────────────────
    st.markdown("### 🔍 Cari Jalur Terpendek")
    if len(vertices) < 2:
        st.info("Tambahkan simpul dan sisi terlebih dahulu.")
    else:
        start = st.selectbox("Simpul Awal", vertices, key="sel_start")
        end   = st.selectbox("Simpul Akhir", vertices, key="sel_end")
        if st.button("🚀 Cari Jalur"):
            if start == end:
                st.error("Simpul awal dan akhir tidak boleh sama.")
            else:
                path, cost = g.find_shortest_path(start, end)
                st.session_state.path_result = path
                st.session_state.cost_result = cost

    st.divider()

    # ── Reset ──────────────────────────────────────────
    if st.button("🗑️ Reset Graf"):
        st.session_state.graf = Graf()
        st.session_state.path_result = None
        st.session_state.cost_result = 0
        st.rerun()

# ══════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════
st.markdown("# 🔵 Visualisasi Graf — Algoritma Dijkstra")
st.divider()

# ── Statistik ──────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="metric-box">
        <div class="metric-val">{g.graph.number_of_nodes()}</div>
        <div class="metric-lbl">Jumlah Simpul</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="metric-box">
        <div class="metric-val">{g.graph.number_of_edges()}</div>
        <div class="metric-lbl">Jumlah Sisi</div>
    </div>""", unsafe_allow_html=True)
with c3:
    connected = nx.is_connected(g.graph) if g.graph.number_of_nodes() > 0 else False
    status = "✅ Ya" if connected else "❌ Tidak"
    st.markdown(f"""<div class="metric-box">
        <div class="metric-val" style="font-size:1.4rem">{status}</div>
        <div class="metric-lbl">Graf Terhubung</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Visualisasi Graf ───────────────────────────────────
col_graph, col_info = st.columns([3, 2])

with col_graph:
    path = st.session_state.path_result
    if path:
        title = f"Jalur Terpendek: {' → '.join(path)}  (Biaya: {st.session_state.cost_result})"
    else:
        title = "Visualisasi Graf"
    fig = g.draw(highlight_path=path, title=title)
    st.pyplot(fig)
    plt.close(fig)

with col_info:
    # Hasil jalur terpendek
    if st.session_state.path_result is not None:
        st.markdown("### 📍 Hasil Jalur Terpendek")
        p = st.session_state.path_result
        if p:
            st.markdown(f"""<div class="path-box">
                <b>Rute :</b> {" → ".join(p)}<br>
                <b>Total Biaya :</b> <span style="color:#22C55E;font-size:1.2rem">
                    {st.session_state.cost_result}
                </span>
            </div>""", unsafe_allow_html=True)
            st.markdown("**Langkah per langkah:**")
            edges_w = g.get_all_vertex_with_weight()
            edge_dict = {(u, v): w for u, v, w in edges_w}
            edge_dict.update({(v, u): w for u, v, w in g.get_all_vertex_with_weight()})
            for i in range(len(p) - 1):
                w = edge_dict.get((p[i], p[i+1]), "?")
                st.markdown(f"&nbsp;&nbsp;`{p[i]}` → `{p[i+1]}` &nbsp; **(bobot: {w})**")
        else:
            st.error("❌ Tidak ada jalur yang menghubungkan kedua simpul.")

    st.markdown("### 📋 Daftar Sisi")
    edges = list(g.get_all_vertex_with_weight())
    if edges:
        for u, v, w in edges:
            st.markdown(f"- `{u}` ─ `{v}` &nbsp;&nbsp; bobot **{w}**")
    else:
        st.info("Belum ada sisi.")

    st.markdown("### 🗺️ Adjacency List")
    adj = g.adj_list
    if adj:
        for node, neighbors in adj.items():
            nbr_str = ", ".join(
                f"{nb} (w={data.get('weight','?')})"
                for nb, data in neighbors.items()
            )
            st.markdown(f"**{node}** → {nbr_str if nbr_str else '—'}")
    else:
        st.info("Graf masih kosong.")
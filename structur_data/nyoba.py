# portfolio.py — One-project Portfolio Wawan Maulana Endang
# Jalankan: python -m streamlit run portfolio.py

import streamlit as st

# ╔══════════════════════════════════════════════════════╗
# ║                  BACKEND — DATA PYTHON               ║
# ╚══════════════════════════════════════════════════════╝

PROFILE = {
    "name"    : "wawan maulana endang",
    "sub"     : "Game Developer . 3D Art & Modeling . 2D Illustration",
    "desc"    : "Game Developer & Digital Artist. Bringing concepts to life through 3D art, illustration, and precision pixel art.",
    "avatar"  : "https://uimg.ngfiles.com/profile/28701/28701254.webp?f1776990534",
    "email"   : "oneproject079@gmail.com",
    "itch"    : "https://one-project.itch.io/",
    "ig"      : "https://www.instagram.com/zxone_079/",
    "twitter" : "https://x.com/oneproject07",
    "youtube" : "https://www.youtube.com/@one_project.079",
}

ABOUT = {
    "bio": [
        "Welcome. I am a game developer and digital artist focused on creating unique visual experiences. "
        "From the logic of programming to the beauty of the digital canvas, I blend technology and art to build immersive worlds.",
        "My expertise spans game development, 3D art, portrait painting, and precision pixel art. "
        "I am dedicated to creating works that leave a lasting impression through every detail I shape.",
    ],
    "skills": [
        ("GAME DEVELOPMENT",      90),
        ("3D MODELING & SCULPT",  50),
        ("PORTRAIT PAINTING",     25),
        ("PIXEL ART",             32),
    ],
}

WORKS = [
    {
        "cat"  : "game",
        "title": "EGG RICE WITH SOY SAUCE",
        "desc" : "someone who came home from working overtime and felt hungry finally cooked rice with egg and sweet soy sauce, but something happened.",
        "image": "https://img.itch.zone/aW1nLzI2ODM2NjM4LmpwZw==/315x250%23c/xq0xgK.jpg",
        "href" : "https://one-project.itch.io/egg-rice-with-soy-sauce",
    },
    {
        "cat"  : "game",
        "title": "NYUSRUK",
        "desc" : "A driver crashes deep in a forest. The car is wrecked. As you try to escape on foot, something mysterious begins to happen.",
        "image": "https://img.itch.zone/aW1nLzI1NDI1NTU0LnBuZw==/315x250%23c/S5rPc1.png",
        "href" : "https://one-project.itch.io/nyusruk",
    },
    {"cat": "3d",       "placeholder": True},
    {"cat": "portrait", "placeholder": True},
    {"cat": "pixel",    "placeholder": True},
]

CATEGORIES = ["game", "3d", "portrait", "pixel"]
CAT_LABELS  = {"game": "PSX Horror Game", "3d": "3D Art", "portrait": "Portrait", "pixel": "Pixel Art"}


def get_works(cat: str) -> list:
    return [w for w in WORKS if w["cat"] == cat]


# ╔══════════════════════════════════════════════════════╗
# ║              FRONTEND — STREAMLIT UI                 ║
# ╚══════════════════════════════════════════════════════╝

st.set_page_config(
    page_title="One-project all about Wawan",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS (identik dengan HTML asli) ─────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Creepster&family=Special+Elite&display=swap" rel="stylesheet"/>
<style>
:root {
  --blood:#8b0000; --blood-bright:#cc0000;
  --dim:#1a0a0a; --darker:#0d0505; --fog:#2a1515;
  --green-crt:#00ff41; --amber:#ffb000; --white-noise:#c8c8c8;
  --scan:rgba(0,0,0,0.08);
}

/* Reset Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.stApp { background: var(--darker) !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Scanlines */
.stApp::before {
  content:'';
  position:fixed; inset:0;
  background: repeating-linear-gradient(0deg,var(--scan) 0px,var(--scan) 1px,transparent 1px,transparent 3px);
  pointer-events:none; z-index:9999;
}
/* Vignette */
.stApp::after {
  content:'';
  position:fixed; inset:0;
  background: radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.85) 100%);
  pointer-events:none; z-index:9998;
}

body { cursor: crosshair; font-family:'Share Tech Mono',monospace; }

/* ── Keyframes ── */
@keyframes glitch1 {
  0%,100%{clip-path:inset(0 0 95% 0);transform:translate(-3px,0)}
  20%{clip-path:inset(30% 0 60% 0);transform:translate(3px,0)}
  40%{clip-path:inset(70% 0 10% 0);transform:translate(-2px,0)}
  60%{clip-path:inset(10% 0 80% 0);transform:translate(2px,0)}
  80%{clip-path:inset(50% 0 40% 0);transform:translate(-3px,0)}
}
@keyframes glitch2 {
  0%,100%{clip-path:inset(80% 0 5% 0);transform:translate(3px,0)}
  20%{clip-path:inset(10% 0 70% 0);transform:translate(-3px,0)}
  40%{clip-path:inset(50% 0 30% 0);transform:translate(2px,0)}
  60%{clip-path:inset(20% 0 65% 0);transform:translate(-2px,0)}
  80%{clip-path:inset(5% 0 85% 0);transform:translate(3px,0)}
}
@keyframes pulse-blood {
  0%,100%{box-shadow:0 0 8px var(--blood),0 0 20px var(--blood)}
  50%{box-shadow:0 0 20px var(--blood-bright),0 0 50px var(--blood-bright)}
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
@keyframes flicker{0%,100%{opacity:1}92%{opacity:1}93%{opacity:.4}94%{opacity:1}96%{opacity:.6}97%{opacity:1}}
@keyframes scanMove{0%{top:-100%}100%{top:100%}}
@keyframes float-up{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}

/* ── NAV ── */
.p-nav {
  position:fixed; top:0; width:100%; z-index:100;
  padding:1rem 2rem;
  display:flex; justify-content:space-between; align-items:center;
  background:linear-gradient(180deg,rgba(13,5,5,.95) 0%,transparent 100%);
  backdrop-filter:blur(4px);
  border-bottom:1px solid rgba(139,0,0,.3);
}
.p-nav-logo {
  font-family:'Creepster',cursive; font-size:1.4rem;
  color:var(--blood-bright); letter-spacing:.1em; text-decoration:none;
}
.p-nav-links { display:flex; gap:2rem; list-style:none; }
.p-nav-links a {
  font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
  color:var(--white-noise); text-decoration:none; transition:color .2s;
}
.p-nav-links a:hover { color:var(--blood-bright); }

/* ── HERO ── */
.p-hero {
  min-height:100vh;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  position:relative; text-align:center; padding:2rem;
  background:radial-gradient(ellipse 60% 40% at 50% 60%,rgba(139,0,0,.18) 0%,transparent 70%),var(--darker);
  animation:flicker 8s infinite;
  overflow:hidden;
}
.p-scan-line {
  position:absolute; width:100%; height:4px;
  background:linear-gradient(90deg,transparent,rgba(0,255,65,.06),transparent);
  animation:scanMove 6s linear infinite; pointer-events:none;
}
.p-avatar {
  width:150px; height:150px; border-radius:50%; overflow:hidden;
  border:3px solid var(--blood-bright);
  box-shadow:0 0 20px var(--blood-bright),inset 0 0 20px rgba(139,0,0,.3);
  animation:pulse-blood 3s infinite;
  margin:4rem auto 2rem; background:var(--fog);
}
.p-avatar img { width:100%; height:100%; object-fit:cover; display:block; }
.p-hero-tag {
  font-size:.7rem; letter-spacing:.3em; color:var(--blood-bright);
  text-transform:uppercase; margin-bottom:1.5rem;
}
.p-hero-tag span { animation:blink 1.2s step-end infinite; }
.p-hero-name {
  font-family:'Creepster',cursive;
  font-size:clamp(3rem,10vw,7rem); line-height:1;
  color:var(--white-noise); position:relative; letter-spacing:.05em;
}
.p-hero-name::before {
  content:attr(data-text); position:absolute; inset:0;
  font-family:inherit; font-size:inherit;
  color:var(--blood-bright); animation:glitch1 4s infinite;
}
.p-hero-name::after {
  content:attr(data-text); position:absolute; inset:0;
  font-family:inherit; font-size:inherit;
  color:var(--green-crt); animation:glitch2 4s infinite .2s;
}
.p-hero-sub {
  font-family:'Special Elite',serif;
  font-size:clamp(.9rem,2.5vw,1.3rem);
  color:var(--amber); margin-top:1.2rem; letter-spacing:.12em;
}
.p-hero-desc {
  max-width:520px; margin:1.5rem auto 0;
  font-size:.82rem; line-height:1.8; color:rgba(200,200,200,.65);
}
.p-cta-row {
  display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; margin-top:2.5rem;
}
.p-btn {
  padding:.7rem 1.8rem; font-family:'Share Tech Mono',monospace;
  font-size:.8rem; letter-spacing:.2em; text-transform:uppercase;
  text-decoration:none; border:1px solid; cursor:crosshair;
  transition:all .2s; display:inline-block;
}
.p-btn-primary {
  background:var(--blood); border-color:var(--blood-bright); color:#fff;
  animation:pulse-blood 3s infinite;
}
.p-btn-primary:hover { background:var(--blood-bright); }
.p-btn-outline {
  background:transparent; border-color:var(--green-crt); color:var(--green-crt);
}
.p-btn-outline:hover { background:rgba(0,255,65,.08); box-shadow:0 0 15px var(--green-crt); }

/* ── SECTION ── */
.p-section {
  padding:6rem 2rem; max-width:1100px; margin:0 auto;
  border-top:1px solid rgba(139,0,0,.2);
}
.p-section-label {
  font-size:.65rem; letter-spacing:.35em; color:var(--blood-bright);
  text-transform:uppercase; margin-bottom:.5rem;
}
.p-section-title {
  font-family:'Creepster',cursive;
  font-size:clamp(2rem,5vw,3.5rem); line-height:1.1; margin-bottom:3rem;
}
.p-section-title::after {
  content:''; display:block; width:60px; height:2px;
  background:var(--blood-bright); margin-top:.8rem;
  box-shadow:0 0 10px var(--blood-bright);
}

/* ── ABOUT GRID ── */
.p-about-grid {
  display:grid; grid-template-columns:1fr 1fr; gap:4rem; align-items:start;
}
@media(max-width:700px){.p-about-grid{grid-template-columns:1fr;gap:2rem}}
.p-about-text p {
  font-size:.88rem; line-height:1.9; color:rgba(200,200,200,.8); margin-bottom:1rem;
}
.p-skill-item { margin-bottom:1.2rem; }
.p-skill-label {
  display:flex; justify-content:space-between;
  font-size:.72rem; letter-spacing:.15em; margin-bottom:.4rem; color:var(--amber);
}
.p-skill-bar {
  height:4px; background:rgba(139,0,0,.2);
  border:1px solid rgba(139,0,0,.4); position:relative;
}
.p-skill-fill {
  height:100%;
  background:linear-gradient(90deg,var(--blood),var(--blood-bright));
  box-shadow:0 0 8px var(--blood-bright);
  transition:width 1.5s cubic-bezier(.16,1,.3,1);
}

/* ── WORKS ── */
.p-filter-row { display:flex; gap:.6rem; flex-wrap:wrap; margin-bottom:2.5rem; }
.p-filter-btn {
  padding:.35rem 1rem; font-family:'Share Tech Mono',monospace;
  font-size:.68rem; letter-spacing:.15em; text-transform:uppercase;
  border:1px solid rgba(139,0,0,.4); background:transparent;
  color:rgba(200,200,200,.6); cursor:crosshair; transition:all .2s;
  display:inline-block;
}
.p-filter-btn.active {
  border-color:var(--blood-bright); color:var(--blood-bright); background:rgba(139,0,0,.1);
}
.p-works-grid {
  display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:1.5rem;
}
.p-work-card {
  border:1px solid rgba(139,0,0,.3); background:var(--fog);
  overflow:hidden; transition:all .3s; animation:float-up .6s ease both;
  text-decoration:none; color:inherit; display:block;
}
.p-work-card:hover {
  border-color:var(--blood-bright); box-shadow:0 0 20px rgba(139,0,0,.3);
  transform:translateY(-3px);
}
.p-work-thumb {
  width:100%; aspect-ratio:16/10; overflow:hidden; position:relative;
  background:var(--dim);
}
.p-work-thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.p-coming-soon {
  display:flex; align-items:center; justify-content:center;
  height:160px; color:rgba(200,200,200,.8);
  font-size:.95rem; text-transform:uppercase; letter-spacing:.25em;
}
.p-work-info { padding:1.2rem; }
.p-work-tag {
  font-size:.6rem; letter-spacing:.25em; text-transform:uppercase;
  color:var(--blood-bright); margin-bottom:.4rem;
}
.p-work-title { font-family:'Special Elite',serif; font-size:1rem; margin-bottom:.5rem; }
.p-work-desc { font-size:.75rem; color:rgba(200,200,200,.55); line-height:1.7; }

/* ── CONTACT ── */
.p-contact { text-align:center; }
.p-contact p {
  font-size:.88rem; color:rgba(200,200,200,.6); line-height:1.9;
  max-width:480px; margin:0 auto 2.5rem;
}
.p-contact-links { display:flex; gap:1.5rem; justify-content:center; flex-wrap:wrap; margin-bottom:3rem; }
.p-contact-link {
  font-size:.72rem; letter-spacing:.2em; text-transform:uppercase;
  color:var(--green-crt); text-decoration:none;
  border-bottom:1px solid rgba(0,255,65,.3); padding-bottom:2px; transition:all .2s;
}
.p-contact-link:hover { color:#fff; border-color:#fff; text-shadow:0 0 10px var(--green-crt); }

/* ── FOOTER ── */
.p-footer {
  border-top:1px solid rgba(139,0,0,.15); padding:2rem; text-align:center;
  font-size:.65rem; letter-spacing:.15em; color:rgba(200,200,200,.25);
}
.p-footer span { color:var(--blood-bright); }
</style>
""", unsafe_allow_html=True)

# ── Session: active filter ────────────────────────────
if "active_cat" not in st.session_state:
    st.session_state.active_cat = "game"

# ══════════════════════════════════════════════════════
# NAV
# ══════════════════════════════════════════════════════
st.markdown("""
<nav class="p-nav">
  <a class="p-nav-logo" href="#">one-project</a>
  <ul class="p-nav-links">
    <li><a href="#about">Tentang</a></li>
    <li><a href="#works">Karya</a></li>
    <li><a href="#contact">Kontak</a></li>
  </ul>
</nav>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="p-hero">
  <div class="p-scan-line"></div>
  <div class="p-avatar">
    <img src="{PROFILE['avatar']}" alt="Profile"/>
  </div>
  <p class="p-hero-tag">&gt; LOADING PORTFOLIO.EXE<span>_</span></p>
  <h1 class="p-hero-name" data-text="{PROFILE['name']}">{PROFILE['name']}</h1>
  <p class="p-hero-sub">{PROFILE['sub']}</p>
  <p class="p-hero-desc">{PROFILE['desc']}</p>
  <div class="p-cta-row">
    <a href="#works" class="p-btn p-btn-primary">&#9654; Lihat Karya</a>
    <a href="#contact" class="p-btn p-btn-outline">&#128225; Hubungi</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════════
bio_html   = "".join(f"<p>{p}</p>" for p in ABOUT["bio"])
skills_html = ""
for name, pct in ABOUT["skills"]:
    skills_html += f"""
    <div class="p-skill-item">
      <div class="p-skill-label"><span>{name}</span><span>{pct}%</span></div>
      <div class="p-skill-bar"><div class="p-skill-fill" style="width:{pct}%"></div></div>
    </div>"""

st.markdown(f"""
<div id="about" class="p-section">
  <p class="p-section-label">// about.exe</p>
  <h2 class="p-section-title">Tentang Saya</h2>
  <div class="p-about-grid">
    <div class="p-about-text">{bio_html}</div>
    <div>{skills_html}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# WORKS — filter buttons via Streamlit columns
# ══════════════════════════════════════════════════════
st.markdown("""
<div id="works" class="p-section" style="padding-bottom:0">
  <p class="p-section-label">// works.dat</p>
  <h2 class="p-section-title">Karya Pilihan</h2>
</div>
""", unsafe_allow_html=True)

# Filter buttons
cols = st.columns(len(CATEGORIES))
for i, cat in enumerate(CATEGORIES):
    with cols[i]:
        active_cls = "active" if st.session_state.active_cat == cat else ""
        # Render styled button via HTML + a real st.button underneath
        st.markdown(f'<div style="margin-bottom:-1rem"><span class="p-filter-btn {active_cls}">{CAT_LABELS[cat]}</span></div>', unsafe_allow_html=True)
        if st.button(CAT_LABELS[cat], key=f"filter_{cat}", use_container_width=True):
            st.session_state.active_cat = cat
            st.rerun()

st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

# Work cards
filtered = get_works(st.session_state.active_cat)
cards_html = '<div class="p-works-grid">'
for i, w in enumerate(filtered):
    delay = f"{i * 0.08}s"
    if w.get("placeholder"):
        cards_html += f"""
        <div class="p-work-card" style="animation-delay:{delay}">
          <div class="p-coming-soon">coming soon</div>
        </div>"""
    else:
        cards_html += f"""
        <a class="p-work-card" href="{w['href']}" target="_blank" rel="noopener noreferrer" style="animation-delay:{delay}">
          <div class="p-work-thumb">
            <img src="{w['image']}" alt="{w['title']}"/>
          </div>
          <div class="p-work-info">
            <p class="p-work-tag">{w['cat'].upper()}</p>
            <h3 class="p-work-title">{w['title']}</h3>
            <p class="p-work-desc">{w['desc']}</p>
          </div>
        </a>"""
cards_html += '</div>'

st.markdown(f'<div style="max-width:1100px;margin:0 auto;padding:0 2rem 6rem">{cards_html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div id="contact" class="p-section p-contact">
  <p class="p-section-label">// contact.ini</p>
  <h2 class="p-section-title" style="text-align:center">Hubungi Saya</h2>
  <p>
    Tertarik berkolaborasi, komisioning karya, atau sekadar ngobrol?
    Jangan ragu untuk menghubungi saya melalui platform di bawah ini.
  </p>
  <div class="p-contact-links">
    <a href="mailto:{PROFILE['email']}" class="p-contact-link" target="_blank">&#9993; EMAIL</a>
    <a href="{PROFILE['itch']}"         class="p-contact-link" target="_blank">&#127918; ITCH.IO</a>
    <a href="{PROFILE['ig']}"           class="p-contact-link" target="_blank">&#128444; INSTAGRAM</a>
    <a href="{PROFILE['twitter']}"      class="p-contact-link" target="_blank">&#128038; TWITTER/X</a>
    <a href="{PROFILE['youtube']}"      class="p-contact-link" target="_blank">&#9654; YOUTUBE</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown("""
<footer class="p-footer">
  <p>© 2026 <span>one-project</span> — Dibuat dengan darah dan piksel &nbsp;|&nbsp; Hosted on <span>GitHub Pages</span></p>
</footer>

<script>
  // Custom cursor
  const dot = document.createElement('div');
  dot.style.cssText = 'width:6px;height:6px;background:#cc0000;border-radius:50%;position:fixed;pointer-events:none;z-index:10000;transform:translate(-50%,-50%);box-shadow:0 0 8px #cc0000;';
  document.body.appendChild(dot);
  document.addEventListener('mousemove', e => {
    dot.style.left = e.clientX+'px';
    dot.style.top  = e.clientY+'px';
  });
</script>
""", unsafe_allow_html=True)
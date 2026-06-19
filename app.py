import streamlit as st
from pathlib import Path
from data.grupos import get_flag_html

st.set_page_config(
    page_title="Simulador da Copa do Mundo 2026",
    page_icon="⚽",
    layout="wide",
)

css_path = Path(__file__).parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

# ── Top bar: logout (esquerda) + nome (direita) ─────────────────
col_logout, col_spacer, col_user = st.columns([1, 4, 1])
with col_logout:
    if st.button("Sair", key="btn_logout"):
        for key in ["participante_id", "nome", "admin", "terceiros_sorteados",
                     "r32_vencedores", "oitavas_vencedores",
                     "quartas_vencedores", "semis_vencedores"]:
            st.session_state.pop(key, None)
        st.switch_page("pages/0_login.py")
with col_user:
    st.markdown(f"<div style='text-align:right;font-weight:600'>👤 {st.session_state.get('nome', '')}</div>", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────
WC_LOGO = "https://cdn.prod.website-files.com/68f550992570ca0322737dc2/69f4a666ff876f5a52a1b7ab_fifa-world-cup-2026-official-logo-footylogos.png"

hero_flags = [
    get_flag_html("Brasil", 24), get_flag_html("Argentina", 24),
    get_flag_html("Alemanha", 24), get_flag_html("França", 24),
    get_flag_html("Espanha", 24), get_flag_html("Inglaterra", 24),
    get_flag_html("Japão", 24), get_flag_html("México", 24),
]
flags_row = " &nbsp; ".join(hero_flags)

st.markdown(f"""
<div class="copa-hero">
    <h1><img src="{WC_LOGO}" width="40" style="vertical-align:middle;margin-right:0.4rem">Copa do Mundo FIFA 2026</h1>
    <p>Simulador de Bolão — Monte o bracket e descubra o campeão!</p>
    <div style="margin-top:0.6rem;font-size:0.88em">{flags_row}</div>
</div>
""", unsafe_allow_html=True)

# ── Navigation ──────────────────────────────────────────────────
nav_items = [
    ("📝 Cadastro", "pages/1_cadastro.py", "nav_cadastro"),
    ("⚽ Seleção", "pages/2_selecao.py", "nav_selecao"),
    ("🏆 Resultado", "pages/3_resultado.py", "nav_resultado"),
    ("📊 Palpites", "pages/4_palpites.py", "nav_palpites"),
    ("🏅 Ranking", "pages/5_ranking.py", "nav_ranking"),
]
if st.session_state.get("admin", False):
    nav_items.append(("👑 Admin", "pages/6_admin.py", "nav_admin"))
cols = st.columns(len(nav_items))
for col, (label, page, key) in zip(cols, nav_items):
    with col:
        if st.button(label, key=key, use_container_width=True):
            st.switch_page(page)

st.markdown("---")

# ── Etapas ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center">
<h3>🏆 Bem-vindo ao Simulador de Bolão da Copa 2026!</h3>
<p style="color:#666">Escolha uma das opções acima para começar:</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
| Etapa | Descrição |
|:-----:|:---------:|
| **1. 📝 Cadastro** | Atualize seus dados cadastrais |
| **2. ⚽ Seleção** | Escolha o 1º e 2º lugar de cada grupo |
| **3. 🏆 Resultado** | Monte o bracket do mata-mata e salve seus palpites |
| **4. 📊 Palpites** | Veja os palpites de todos os participantes |
| **5. 🏅 Ranking** | Veja o ranking baseado nos resultados reais |
""")

# ── Footer ──────────────────────────────────────────────────────
footer_flags = [
    get_flag_html("Portugal", 20), get_flag_html("Croácia", 20),
    get_flag_html("Colômbia", 20), get_flag_html("Uruguai", 20),
    get_flag_html("Senegal", 20), get_flag_html("Marrocos", 20),
    get_flag_html("Austrália", 20), get_flag_html("Canadá", 20),
]
footer_row = " &nbsp; ".join(footer_flags)

st.markdown(f"""
<div style="text-align:center;margin:1rem 0 0.5rem">
    <div style="margin-bottom:0.5rem">{footer_row}</div>
    <p style="color:#888;font-size:0.82em;margin:0">
        <strong>48 seleções</strong> de 6 confederações — a primeira Copa com 48 equipes!
    </p>
</div>
""", unsafe_allow_html=True)

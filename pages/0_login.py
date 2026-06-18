import streamlit as st
from pathlib import Path
from database.connection import get_supabase
from utils.auth import hash_senha, verificar_senha
from data.grupos import get_flag_html

st.set_page_config(page_title="Login - Copa 2026", page_icon="🔑", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "participante_id" in st.session_state:
    st.switch_page("app.py")

# ── Hero ────────────────────────────────────────────────────────
hero_flags = [
    get_flag_html("Brasil", 24), get_flag_html("Argentina", 24),
    get_flag_html("Alemanha", 24), get_flag_html("França", 24),
    get_flag_html("Espanha", 24), get_flag_html("Inglaterra", 24),
    get_flag_html("Japão", 24), get_flag_html("México", 24),
]
flags_row = " &nbsp; ".join(hero_flags)

WC_LOGO = "https://cdn.prod.website-files.com/68f550992570ca0322737dc2/69f4a666ff876f5a52a1b7ab_fifa-world-cup-2026-official-logo-footylogos.png"

st.markdown(f"""
<div class="copa-hero">
    <h1><img src="{WC_LOGO}" width="40" style="vertical-align:middle;margin-right:0.4rem">Copa do Mundo FIFA 2026</h1>
    <p>Simulador de Bolão — Entre para palpitar!</p>
    <div style="margin-top:0.6rem;font-size:0.88em">{flags_row}</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────
tab_login, tab_cadastro = st.tabs(["🔑 Entrar", "📝 Cadastrar"])

supabase = get_supabase()

# ═══════════════════════════════════════════════════════════════════
# TAB LOGIN
# ═══════════════════════════════════════════════════════════════════
with tab_login:
    with st.form("login"):
        email = st.text_input("E-mail", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password", placeholder="Sua senha")
        enviado = st.form_submit_button("Entrar", use_container_width=True, type="primary")

    if enviado:
        if not email or not senha:
            st.error("Preencha e-mail e senha.")
        else:
            result = supabase.table("participantes").select("*").eq("email", email).execute()
            if not result.data:
                st.error("E-mail não encontrado.")
            else:
                user = result.data[0]
                if verificar_senha(senha, user["senha_hash"]):
                    st.session_state["participante_id"] = user["id"]
                    st.session_state["nome"] = user["nome_completo"]
                    st.success(f"Bem-vindo(a), {user['nome_completo']}!")
                    st.switch_page("app.py")
                else:
                    st.error("Senha incorreta.")

# ═══════════════════════════════════════════════════════════════════
# TAB CADASTRO
# ═══════════════════════════════════════════════════════════════════
with tab_cadastro:
    with st.form("cadastro"):
        nome = st.text_input("Nome Completo *", placeholder="Seu nome completo")
        email = st.text_input("E-mail *", placeholder="seu@email.com")
        senha = st.text_input("Senha *", type="password", placeholder="Mínimo 4 caracteres")
        senha_confirma = st.text_input("Confirmar Senha *", type="password")
        enviado = st.form_submit_button("Cadastrar", use_container_width=True, type="primary")

    if enviado:
        if not nome or not email or not senha:
            st.error("Preencha todos os campos obrigatórios.")
        elif "@" not in email:
            st.error("E-mail inválido.")
        elif len(senha) < 4:
            st.error("A senha deve ter pelo menos 4 caracteres.")
        elif senha != senha_confirma:
            st.error("As senhas não conferem.")
        else:
            try:
                result = supabase.table("participantes").insert({
                    "nome_completo": nome,
                    "email": email,
                    "senha_hash": hash_senha(senha),
                    "time_favorito": "",
                }).execute()

                st.session_state["participante_id"] = result.data[0]["id"]
                st.session_state["nome"] = nome
                st.success(f"Cadastro realizado! Bem-vindo(a), {nome}!")
                st.balloons()
                st.switch_page("app.py")
            except Exception as e:
                if "unique" in str(e).lower():
                    st.error("Este e-mail já está cadastrado.")
                else:
                    st.error(f"Erro ao cadastrar: {e}")

import streamlit as st
from pathlib import Path
from database.connection import get_supabase
from utils.auth import hash_senha, verificar_senha
from data.grupos import get_flag

st.set_page_config(page_title="Cadastro - Copa 2026", page_icon="📝", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("← Início", key="voltar_cadastro"):
    st.switch_page("app.py")

if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

st.title("📝 Meu Cadastro")

supabase = get_supabase()
participante_id = st.session_state["participante_id"]

user_data = supabase.table("participantes").select("*").eq("id", participante_id).execute()
if not user_data.data:
    st.error("Usuário não encontrado.")
    st.stop()

user = user_data.data[0]

# ── User info ───────────────────────────────────────────────────
st.markdown(f"👤 **{user['nome_completo']}** — {user['email']}")

# ── Edit form ───────────────────────────────────────────────────
with st.form("editar_perfil"):
    nome = st.text_input("Nome Completo", value=user["nome_completo"])
    st.markdown("**Alterar senha** (deixe em branco para manter)")
    nova_senha = st.text_input("Nova Senha", type="password")
    confirma_senha = st.text_input("Confirmar Nova Senha", type="password")
    senha_atual = st.text_input("Senha Atual (obrigatória para alterar)", type="password")

    enviado = st.form_submit_button("Salvar Alterações", use_container_width=True, type="primary")

if enviado:
    if not nome:
        st.error("Nome é obrigatório.")
    else:
        updates = {"nome_completo": nome}

        if nova_senha:
            if not verificar_senha(senha_atual, user["senha_hash"]):
                st.error("Senha atual incorreta.")
            elif len(nova_senha) < 4:
                st.error("A nova senha deve ter pelo menos 4 caracteres.")
            elif nova_senha != confirma_senha:
                st.error("As senhas não conferem.")
            else:
                updates["senha_hash"] = hash_senha(nova_senha)

        if "senha_hash" in updates or nome != user["nome_completo"]:
            try:
                supabase.table("participantes").update(updates).eq("id", participante_id).execute()
                st.session_state["nome"] = nome
                st.success("Dados atualizados!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")

# ── Status ──────────────────────────────────────────────────────
st.markdown("---")

selecoes = supabase.table("selecoes").select("*").eq("participante_id", participante_id).execute()
palpites_bracket = supabase.table("palpites_bracket").select("*").eq("participante_id", participante_id).execute()
palpites_grupos = supabase.table("palpites_grupos").select("*").eq("participante_id", participante_id).execute()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Grupos", len(selecoes.data))
with col2:
    st.metric("Palpites Grupos", len(palpites_grupos.data))
with col3:
    st.metric("Bracket", "Sim" if palpites_bracket.data else "Não")

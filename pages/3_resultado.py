import streamlit as st
from pathlib import Path
from database.connection import get_supabase
from data.grupos import GRUPOS, get_flag_html
from data.jogos import GRUPO_RODADAS, GRUPO_DATAS, GRUPO_JOGOS_DATAS
from utils.ui_components import grupo_label_with_flags

st.set_page_config(page_title="Resultado - Copa 2026", page_icon="🏆", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("← Início", key="voltar_resultado"):
    st.switch_page("app.py")

st.title("🏆 Resultado — Palpites por Data")

if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

supabase = get_supabase()
participante_id = st.session_state["participante_id"]

# ── Load data ───────────────────────────────────────────────────
selecoes = supabase.table("selecoes").select("*").eq("participante_id", participante_id).execute()
if not selecoes.data:
    st.warning("Faça suas seleções primeiro na aba 'Seleção'.")
    st.stop()

classificacao = {}
for sel in selecoes.data:
    classificacao[sel["grupo"]] = {"primeiro": sel["primeiro_lugar"], "segundo": sel["segundo_lugar"]}

terceiros_row = supabase.table("melhores_terceiros").select("terceiros_selecionados").eq("participante_id", participante_id).execute()
terceiros = terceiros_row.data[0]["terceiros_selecionados"] if terceiros_row.data else None

palpites_grupos_row = supabase.table("palpites_grupos").select("*").eq("participante_id", participante_id).execute()
palpites_grupos_data = {}
for p in palpites_grupos_row.data:
    key = (p["rodada"], p["grupo"], p["time_casa"], p["time_fora"])
    palpites_grupos_data[key] = p


# ═══════════════════════════════════════════════════════════════════
# PALPITES DA FASE DE GRUPOS — por grupo
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">📋 PALPITES — FASE DE GRUPOS</div>', unsafe_allow_html=True)

if palpites_grupos_data:
    for grupo_letra in GRUPOS.keys():
        st.markdown(f'<div class="bracket-round-header">⚽ {grupo_label_with_flags(grupo_letra)}</div>', unsafe_allow_html=True)

        for rodada_num in [1, 2, 3]:
            jogos_rodada = GRUPO_RODADAS[rodada_num]
            jogos_grupo = [(c, f) for g, c, f in jogos_rodada if g == grupo_letra]
            if not jogos_grupo:
                continue

            st.caption(f"Rodada {rodada_num} — {GRUPO_DATAS[rodada_num]}")
            for casa, fora in jogos_grupo:
                key = (rodada_num, grupo_letra, casa, fora)
                palpite = palpites_grupos_data.get(key)
                casa_flag = get_flag_html(casa, 18)
                fora_flag = get_flag_html(fora, 18)
                data_hora = GRUPO_JOGOS_DATAS.get(key, "")
                data_str = f" <small style='color:#999'>⏰ {data_hora} BRT</small>" if data_hora else ""
                if palpite:
                    st.markdown(
                        f"{casa_flag} **{casa}** {palpite['placar_casa']} x "
                        f"{palpite['placar_fora']} **{fora}** {fora_flag}{data_str}",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"{casa_flag} **{casa}** vs **{fora}** {fora_flag} — <em style='color:#999'>sem palpite</em>{data_str}",
                        unsafe_allow_html=True,
                    )
else:
    st.info("Nenhum palpite de fase de grupos registrado. Faça seus palpites na aba 'Seleção'.")

import streamlit as st
from pathlib import Path
from database.connection import get_supabase
from data.grupos import GRUPOS, get_flag, get_flag_html
from data.jogos import (
    GRUPO_RODADAS, GRUPO_DATAS, GRUPO_JOGOS_DATAS,
    MATA_MATA_RODADAS, ORDEM_RODADAS_MATA_MATA,
)
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

palpites_bracket_row = supabase.table("palpites_bracket").select("*").eq("participante_id", participante_id).execute()
palpites_bracket_data = palpites_bracket_row.data[0] if palpites_bracket_row.data else None

# ── Load real results ──────────────────────────────────────────
resultados_row = supabase.table("resultados").select("*").execute()
resultados_grupo = {}
resultados_bracket = {}
for r in resultados_row.data:
    if r["fase"] == "grupo":
        key = (r["rodada"], r["grupo"], r["time_casa"], r["time_fora"])
        resultados_grupo[key] = r
    else:
        key = (r["fase"], r["time_casa"], r["time_fora"])
        resultados_bracket[key] = r


# ═══════════════════════════════════════════════════════════════════
# PALPITES DA FASE DE GRUPOS — por data (tabs)
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">📋 PALPITES — FASE DE GRUPOS</div>', unsafe_allow_html=True)

if palpites_grupos_data:
    tab_labels = [f"Rodada {r} — {GRUPO_DATAS[r]}" for r in [1, 2, 3]]
    tabs = st.tabs(tab_labels)

    for tab, rodada_num in zip(tabs, [1, 2, 3]):
        with tab:
            jogos_rodada = GRUPO_RODADAS[rodada_num]
            jogos_por_grupo = {}
            for grupo, casa, fora in jogos_rodada:
                jogos_por_grupo.setdefault(grupo, []).append((casa, fora))

            for grupo_letra in GRUPOS.keys():
                jogos_grupo = jogos_por_grupo.get(grupo_letra, [])
                if not jogos_grupo:
                    continue

                st.markdown(f'<div class="bracket-round-header">⚽ {grupo_label_with_flags(grupo_letra)}</div>', unsafe_allow_html=True)

                for casa, fora in jogos_grupo:
                    key = (rodada_num, grupo_letra, casa, fora)
                    palpite = palpites_grupos_data.get(key)
                    resultado = resultados_grupo.get(key)
                    casa_flag = get_flag_html(casa, 18)
                    fora_flag = get_flag_html(fora, 18)
                    data_hora = GRUPO_JOGOS_DATAS.get(key, "")
                    data_str = f" <small style='color:#999'>⏰ {data_hora} BRT</small>" if data_hora else ""

                    if resultado:
                        r_casa, r_fora = resultado["gols_casa"], resultado["gols_fora"]
                        real_str = f"{r_casa}x{r_fora}"
                    else:
                        real_str = None

                    if palpite:
                        p_casa, p_fora = palpite["placar_casa"], palpite["placar_fora"]
                        palpite_str = f"{p_casa}x{p_fora}"

                        if real_str:
                            if p_casa == r_casa and p_fora == r_fora:
                                emoji = "✅"
                                pts_str = "4 pts"
                            elif (p_casa > p_fora and r_casa > r_fora) or (p_fora > p_casa and r_fora > r_casa) or (p_casa == p_fora and r_casa == r_fora):
                                emoji = "🟡"
                                pts_str = "1 pt"
                            else:
                                emoji = "❌"
                                pts_str = "0 pts"
                            st.markdown(
                                f"{casa_flag} **{casa}** {palpite_str} vs {real_str} **{fora}** {fora_flag} "
                                f"{emoji} {pts_str}{data_str}",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"{casa_flag} **{casa}** {palpite_str} vs ⏳ **{fora}** {fora_flag}{data_str}",
                                unsafe_allow_html=True,
                            )
                    else:
                        if real_str:
                            st.markdown(
                                f"{casa_flag} **{casa}** vs {real_str} **{fora}** {fora_flag} — "
                                f"<em style='color:#999'>sem palpite</em>{data_str}",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"{casa_flag} **{casa}** vs **{fora}** {fora_flag} — "
                                f"<em style='color:#999'>sem palpite</em>{data_str}",
                                unsafe_allow_html=True,
                            )
else:
    st.info("Nenhum palpite de fase de grupos registrado. Faça seus palpites na aba 'Seleção'.")


# ═══════════════════════════════════════════════════════════════════
# PALPITES DO MATA-MATA — por data (tabs)
# ═══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="bracket-round-header">🏆 PALPITES — MATA-MATA</div>', unsafe_allow_html=True)

if palpites_bracket_data:
    palpites = palpites_bracket_data["palpites"]

    tab_labels_mk = [
        f"{MATA_MATA_RODADAS[r]['label']} — {MATA_MATA_RODADAS[r]['data']}"
        for r in ORDEM_RODADAS_MATA_MATA
    ]
    tabs_mk = st.tabs(tab_labels_mk)

    for tab_mk, fase_key in zip(tabs_mk, ORDEM_RODADAS_MATA_MATA):
        with tab_mk:
            fase_label = MATA_MATA_RODADAS[fase_key]["label"]
            fase_palpites = palpites.get(fase_key, [])
            fase_placares = palpites.get(f"{fase_key}_placares", [])
            confrontos = MATA_MATA_RODADAS[fase_key]["confrontos"]

            if not fase_palpites:
                st.info(f"Sem palpites para {fase_label}.")
                continue

            for i, vencedor_palpite in enumerate(fase_palpites):
                if not vencedor_palpite:
                    continue

                placar_info = fase_placares[i] if i < len(fase_placares) else None
                if not placar_info:
                    continue

                casa_time = placar_info.get("casa_time", "")
                fora_time = placar_info.get("fora_time", "")
                p_casa = placar_info.get("placar_casa", 0)
                p_fora = placar_info.get("placar_fora", 0)

                # Buscar resultado real
                resultado = resultados_bracket.get((fase_key, casa_time, fora_time))
                reversed_bracket = False
                if not resultado:
                    resultado = resultados_bracket.get((fase_key, fora_time, casa_time))
                    reversed_bracket = True
                if resultado:
                    r_casa, r_fora = resultado["gols_casa"], resultado["gols_fora"]
                    if reversed_bracket:
                        r_casa, r_fora = r_fora, r_casa
                    if r_casa > r_fora:
                        vencedor_real = casa_time
                    elif r_fora > r_casa:
                        vencedor_real = fora_time
                    else:
                        vencedor_real = None  # Empate = precisa pênaltis

                    # Data do confronto
                    data_str = ""
                    for cd in confrontos:
                        if cd.get("casa") == casa_time or cd.get("fora") == fora_time:
                            data_str = cd.get("data", "")
                            break

                    casa_flag = get_flag_html(casa_time, 18)
                    fora_flag = get_flag_html(fora_time, 18)
                    real_str = f"{r_casa}x{r_fora}"

                    if vencedor_real:
                        if vencedor_palpite == vencedor_real:
                            if p_casa == r_casa and p_fora == r_fora:
                                emoji, pts_str = "✅", "4 pts"
                            else:
                                emoji, pts_str = "🟡", "1 pt"
                        else:
                            emoji, pts_str = "❌", "0 pts"

                        venc_palpite_flag = get_flag_html(vencedor_palpite, 16)
                        venc_real_flag = get_flag_html(vencedor_real, 16)
                        st.markdown(
                            f"{casa_flag} **{casa_time}** {real_str} **{fora_time}** {fora_flag} "
                            f"— Palpite: {venc_palpite_flag} **{vencedor_palpite}** ({p_casa}x{p_fora}) "
                            f"{emoji} {pts_str} "
                            f"<small style='color:#999'>⏰ {data_str}</small>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"{casa_flag} **{casa_time}** {real_str} **{fora_time}** {fora_flag} "
                            f"— ⚠️ Empate! Inserir pênaltis no Admin "
                            f"<small style='color:#999'>⏰ {data_str}</small>",
                            unsafe_allow_html=True,
                        )
                else:
                    # Sem resultado real ainda
                    casa_flag = get_flag_html(casa_time, 18)
                    fora_flag = get_flag_html(fora_time, 18)
                    venc_flag = get_flag_html(vencedor_palpite, 16)
                    st.markdown(
                        f"{casa_flag} **{casa_time}** vs **{fora_time}** {fora_flag} "
                        f"— Palpite: {venc_flag} **{vencedor_palpite}** ({p_casa}x{p_fora}) "
                        f"⏳ Aguardando",
                        unsafe_allow_html=True,
                    )
else:
    st.info("Nenhum palpite de mata-mata registrado. Faça seus palpites na aba 'Seleção'.")


# ═══════════════════════════════════════════════════════════════════
# RESUMO: CAMPEÃO ESCOLHIDO
# ═══════════════════════════════════════════════════════════════════
if palpites_bracket_data:
    st.markdown("---")
    st.markdown('<div class="bracket-round-header">🏆 MEU CAMPEÃO</div>', unsafe_allow_html=True)
    final_picks = palpites.get("Final", [])
    if final_picks and final_picks[0]:
        campeao = final_picks[0]
        campeao_flag = get_flag_html(campeao, 28)
        st.markdown(f"**{campeao_flag} {campeao}**", unsafe_allow_html=True)
    else:
        st.info("Nenhum palpite de campeão registrado.")

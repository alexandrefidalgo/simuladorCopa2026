import streamlit as st
import pandas as pd
from pathlib import Path
from database.connection import get_supabase
from data.grupos import get_flag, get_flag_html, time_com_bandeira, GRUPOS
from data.jogos import (
    GRUPO_RODADAS, GRUPO_DATAS, GRUPO_JOGOS_DATAS,
    MATA_MATA_RODADAS, ORDEM_RODADAS_MATA_MATA,
)
from utils.ui_components import grupo_label_with_flags

st.set_page_config(page_title="Palpites - Copa 2026", page_icon="📊", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("← Início", key="voltar_palpites"):
    st.switch_page("app.py")

st.title("📊 Palpites de Todos os Participantes")

supabase = get_supabase()

# ── Load data ───────────────────────────────────────────────────
palpites_data = supabase.table("palpites_bracket").select("*").execute()
palpites_grupos_data = supabase.table("palpites_grupos").select("*").execute()
participantes_data = supabase.table("participantes").select("id, nome_completo").execute()
participantes_map = {p["id"]: p["nome_completo"] for p in participantes_data.data}

if not palpites_data.data and not palpites_grupos_data.data:
    st.info("Nenhum participante salvou palpites ainda.")
    st.stop()

st.metric("Participantes", max(len(palpites_data.data), len(palpites_grupos_data.data)))

# ═══════════════════════════════════════════════════════════════════
# CLASSIFICAÇÃO DOS GRUPOS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">📋 CLASSIFICAÇÃO DOS GRUPOS</div>', unsafe_allow_html=True)

selecoes_data = supabase.table("selecoes").select("*").execute()
terceiros_data = supabase.table("melhores_terceiros").select("*").execute()

if selecoes_data.data:
    tab_labels_grupos = [f"Grupo {g}" for g in GRUPOS.keys()]
    tabs_grupos = st.tabs(tab_labels_grupos)

    for tab, grupo_letra in zip(tabs_grupos, GRUPOS.keys()):
        with tab:
            rows = []
            for p in selecoes_data.data:
                if p["grupo"] == grupo_letra:
                    nome = participantes_map.get(p["participante_id"], "?")
                    p_flag = get_flag(p["primeiro_lugar"])
                    s_flag = get_flag(p["segundo_lugar"])
                    rows.append({
                        "Participante": nome,
                        "1º Lugar": f"{p_flag} {p['primeiro_lugar']}",
                        "2º Lugar": f"{s_flag} {p['segundo_lugar']}",
                    })
            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info(f"Sem classificação para o Grupo {grupo_letra}.")

    if terceiros_data.data:
        st.markdown("#### 🎲 Melhores Terceiros")
        rows_t = []
        for p in terceiros_data.data:
            nome = participantes_map.get(p["participante_id"], "?")
            times = p["terceiros_selecionados"]
            flags_times = [f"{get_flag(t)} {t}" for t in times]
            rows_t.append({"Participante": nome, "Terceiros": ", ".join(flags_times)})
        if rows_t:
            df = pd.DataFrame(rows_t)
            st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma classificação registrada.")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# FASE DE GRUPOS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">📋 FASE DE GRUPOS</div>', unsafe_allow_html=True)

if palpites_grupos_data.data:
    tab_labels_grupos = [f"Rodada {r} — {GRUPO_DATAS[r]}" for r in [1, 2, 3]]
    tabs_grupos = st.tabs(tab_labels_grupos)

    for tab, rodada_num in zip(tabs_grupos, [1, 2, 3]):
        with tab:
            jogos_rodada = GRUPO_RODADAS[rodada_num]
            for grupo_letra in GRUPOS.keys():
                jogos_grupo = [(c, f) for g, c, f in jogos_rodada if g == grupo_letra]
                if not jogos_grupo:
                    continue

                st.markdown(f"**{grupo_label_with_flags(grupo_letra)}**")
                rows = []
                for casa, fora in jogos_grupo:
                    data_hora = GRUPO_JOGOS_DATAS.get((rodada_num, grupo_letra, casa, fora), "")
                    data_str = f" ({data_hora} BRT)" if data_hora else ""
                    casa_flag = get_flag(casa)
                    fora_flag = get_flag(fora)
                    row = {"Jogo": f"{casa_flag} {casa} vs {fora} {fora_flag}{data_str}"}
                    for p in palpites_grupos_data.data:
                        nome = participantes_map.get(p["participante_id"], "?")
                        if (p["rodada"] == rodada_num and p["grupo"] == grupo_letra
                                and p["time_casa"] == casa and p["time_fora"] == fora):
                            row[nome] = f"{p['placar_casa']} x {p['placar_fora']}"
                    rows.append(row)

                if rows:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum palpite de fase de grupos registrado.")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# MATA-MATA
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">🏆 MATA-MATA</div>', unsafe_allow_html=True)

if palpites_data.data:
    tab_labels = [
        f"{MATA_MATA_RODADAS[r]['label']} — {MATA_MATA_RODADAS[r]['data']}"
        for r in ORDEM_RODADAS_MATA_MATA
    ]
    tabs = st.tabs(tab_labels)

    for tab, fase_key in zip(tabs, ORDEM_RODADAS_MATA_MATA):
        with tab:
            fase_label = MATA_MATA_RODADAS[fase_key]["label"]
            placares_key = f"{fase_key}_placares"
            rows = []

            for palpites_row in palpites_data.data:
                participante_id = palpites_row["participante_id"]
                nome = participantes_map.get(participante_id, "?")
                palpites = palpites_row["palpites"]
                fase_palpites = palpites.get(fase_key, [])
                fase_placares = palpites.get(placares_key, [])

                if fase_palpites:
                    row = {"Participante": nome}
                    for i, vencedor in enumerate(fase_palpites):
                        if vencedor:
                            flag = get_flag(vencedor)
                            if i < len(fase_placares) and fase_placares[i]:
                                p = fase_placares[i]
                                row[f"Jogo {i+1}"] = f"{flag} {vencedor} ({p['placar_casa']}x{p['placar_fora']})"
                            else:
                                row[f"Jogo {i+1}"] = f"{flag} {vencedor}"
                        else:
                            row[f"Jogo {i+1}"] = "—"
                    rows.append(row)

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info(f"Sem palpites para {fase_label}.")
else:
    st.info("Nenhum palpite de mata-mata registrado.")

# ═══════════════════════════════════════════════════════════════════
# CAMPEÕES ESCOLHIDOS
# ═══════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("#### 🏆 Resumo: Campeões Escolhidos")

champion_counts = {}
for palpites_row in palpites_data.data:
    nome = participantes_map.get(palpites_row["participante_id"], "?")
    final_picks = palpites_row["palpites"].get("Final", [])
    if final_picks and final_picks[0]:
        campeao = final_picks[0]
        champion_counts.setdefault(campeao, []).append(nome)

if champion_counts:
    sorted_champs = sorted(champion_counts.items(), key=lambda x: len(x[1]), reverse=True)
    for campeao, nomes in sorted_champs:
        flag = get_flag_html(campeao, 22)
        st.markdown(f"**{flag} {campeao}** — {len(nomes)} palpite(s): {', '.join(nomes)}", unsafe_allow_html=True)
else:
    st.info("Nenhum palpite de campeão registrado.")

import streamlit as st
import pandas as pd
from pathlib import Path
from database.connection import get_supabase
from data.grupos import GRUPOS, get_flag, get_flag_html
from data.jogos import (
    GRUPO_RODADAS, GRUPO_DATAS, GRUPO_JOGOS_DATAS,
    MATA_MATA_RODADAS, ORDEM_RODADAS_MATA_MATA,
)
from utils.ui_components import render_grupo_simples, grupo_label_with_flags
from utils.api import build_resultados_from_api

st.set_page_config(page_title="Seleção - Copa Do Mundo 2026", page_icon="⚽", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("← Início", key="voltar_selecao"):
    st.switch_page("app.py")

st.title("⚽ Palpites — Copa 2026")

if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

supabase = get_supabase()
participante_id = st.session_state["participante_id"]

# ── Load saved data ─────────────────────────────────────────────
selecoes_row = supabase.table("selecoes").select("*").eq("participante_id", participante_id).execute()
salvos = {}
for sel in selecoes_row.data:
    salvos[sel["grupo"]] = {"primeiro": sel["primeiro_lugar"], "segundo": sel["segundo_lugar"]}

terceiros_row = supabase.table("melhores_terceiros").select("terceiros_selecionados").eq("participante_id", participante_id).execute()
if terceiros_row.data:
    st.session_state["terceiros_sorteados"] = terceiros_row.data[0]["terceiros_selecionados"]

palpites_grupos_row = supabase.table("palpites_grupos").select("*").eq("participante_id", participante_id).execute()
palpites_salvos = {}
for p in palpites_grupos_row.data:
    key = (p["rodada"], p["grupo"], p["time_casa"], p["time_fora"])
    palpites_salvos[key] = {"placar_casa": p["placar_casa"], "placar_fora": p["placar_fora"]}

# ── 1. Select 1st and 2nd per group ────────────────────────────
st.markdown("#### 📋 Selecione o 1º e 2º lugar de cada grupo")

resultados = {}
colunas = st.columns(3)
for i, grupo_letra in enumerate(GRUPOS.keys()):
    with colunas[i % 3]:
        sel = salvos.get(grupo_letra, {})
        with st.container(border=True):
            resultado = render_grupo_simples(
                grupo_letra, f"grupo_{grupo_letra}",
                default_primeiro=sel.get("primeiro"),
                default_segundo=sel.get("segundo"),
            )
            resultados[grupo_letra] = resultado

# ── 1.1 Live classification ────────────────────────────────────
st.markdown("---")
st.markdown("#### ⚽ Classificação dos Grupos — Ao Vivo")
st.caption("1º e 2º → Rodada de 32 | 3º → Melhores 8 | 4º → Eliminado")

resultados_row = supabase.table("resultados").select("*").execute()
resultados_grupo = {}
for r in resultados_row.data:
    if r["fase"] == "grupo":
        key = (r["rodada"], r["grupo"], r["time_casa"], r["time_fora"])
        resultados_grupo[key] = r

# Merge with live API results
# API uses rodada=0; override DB when DB has 0x0 (empty) results
api_resultados = build_resultados_from_api()
for key, api_r in api_resultados.items():
    grupo, casa, fora = key[1], key[2], key[3]
    has_real_result = False
    for rodada in [1, 2, 3]:
        db_key = (rodada, grupo, casa, fora)
        db_key_rev = (rodada, grupo, fora, casa)
        if db_key in resultados_grupo:
            r = resultados_grupo[db_key]
            if r.get("gols_casa", 0) > 0 or r.get("gols_fora", 0) > 0:
                has_real_result = True
                break
        if db_key_rev in resultados_grupo:
            r = resultados_grupo[db_key_rev]
            if r.get("gols_casa", 0) > 0 or r.get("gols_fora", 0) > 0:
                has_real_result = True
                break
    if not has_real_result:
        resultados_grupo[key] = api_r

# ── Navegação entre grupos ──────────────────────────────────────
if "grupo_idx" not in st.session_state:
    st.session_state["grupo_idx"] = 0

col_prev, col_select, col_next = st.columns([1, 3, 1])
with col_prev:
    if st.button("◀", key="prev_grupo", use_container_width=True):
        if st.session_state["grupo_idx"] > 0:
            st.session_state["grupo_idx"] -= 1
with col_select:
    grupo_letras = list(GRUPOS.keys())
    idx_atual = st.session_state["grupo_idx"]
    opcoes_grupos = [f"⚽ Grupo {g} — {' '.join(get_flag(t) for t in GRUPOS[g])}" for g in grupo_letras]
    escolha = st.selectbox("Grupo", opcoes_grupos, index=idx_atual, key="select_grupo_classif", label_visibility="collapsed")
    novo_idx = opcoes_grupos.index(escolha)
    if novo_idx != idx_atual:
        st.session_state["grupo_idx"] = novo_idx
        idx_atual = novo_idx
with col_next:
    if st.button("▶", key="next_grupo", use_container_width=True):
        if st.session_state["grupo_idx"] < len(grupo_letras) - 1:
            st.session_state["grupo_idx"] += 1

grupo_letra = grupo_letras[st.session_state["grupo_idx"]]

times_grupo = GRUPOS[grupo_letra]
stats = {}
for t in times_grupo:
    stats[t] = {"jogos": 0, "v": 0, "e": 0, "d": 0, "gf": 0, "gc": 0, "sg": 0, "pontos": 0}

for key, r in resultados_grupo.items():
    if key[1] != grupo_letra:
        continue
    gols_casa, gols_fora = r["gols_casa"], r["gols_fora"]
    if gols_casa == 0 and gols_fora == 0:
        casa, fora = key[2], key[3]
        has_real = any(
            resultados_grupo.get((rod, grupo_letra, casa, fora), {}).get("gols_casa", 0) > 0 or
            resultados_grupo.get((rod, grupo_letra, casa, fora), {}).get("gols_fora", 0) > 0
            for rod in [0, 1, 2, 3]
        ) or any(
            resultados_grupo.get((rod, grupo_letra, fora, casa), {}).get("gols_casa", 0) > 0 or
            resultados_grupo.get((rod, grupo_letra, fora, casa), {}).get("gols_fora", 0) > 0
            for rod in [0, 1, 2, 3]
        )
        if has_real:
            continue
    casa, fora = key[2], key[3]

    stats[casa]["jogos"] += 1
    stats[fora]["jogos"] += 1
    stats[casa]["gf"] += gols_casa
    stats[casa]["gc"] += gols_fora
    stats[fora]["gf"] += gols_fora
    stats[fora]["gc"] += gols_casa
    stats[casa]["sg"] = stats[casa]["gf"] - stats[casa]["gc"]
    stats[fora]["sg"] = stats[fora]["gf"] - stats[fora]["gc"]

    if gols_casa > gols_fora:
        stats[casa]["v"] += 1
        stats[casa]["pontos"] += 3
        stats[fora]["d"] += 1
    elif gols_fora > gols_casa:
        stats[fora]["v"] += 1
        stats[fora]["pontos"] += 3
        stats[casa]["d"] += 1
    else:
        stats[casa]["e"] += 1
        stats[fora]["e"] += 1
        stats[casa]["pontos"] += 1
        stats[fora]["pontos"] += 1

ranking_grupo = sorted(stats.items(), key=lambda x: (x[1]["pontos"], x[1]["sg"], x[1]["gf"]), reverse=True)

rows = []
for pos, (time, s) in enumerate(ranking_grupo):
    flag = get_flag(time)
    rows.append({
        "Pos": f"{pos+1}°",
        "Seleção": f"{flag} {time}",
        "J": s["jogos"],
        "V": s["v"],
        "E": s["e"],
        "D": s["d"],
        "GP": s["gf"],
        "GC": s["gc"],
        "SG": f"+{s['sg']}" if s['sg'] > 0 else str(s['sg']),
        "PTS": s["pontos"],
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

# ── 2. Best Thirds ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="bracket-round-header">🎲 MELHORES TERCEIROS</div>', unsafe_allow_html=True)
st.caption("Selecione os 8 melhores terceiros lugares (entre os 12 terceiros da fase de grupos):")

todos_terceiros = [resultados[g]["primeiro"] for g in GRUPOS.keys() if resultados[g].get("primeiro")]
# List all possible third-place teams (3rd in each group based on user picks)
terceiros_disponiveis = []
for g in GRUPOS.keys():
    times_grupo = GRUPOS[g]
    primeiro = resultados[g].get("primeiro")
    segundo = resultados[g].get("segundo")
    for t in times_grupo:
        if t != primeiro and t != segundo:
            terceiros_disponiveis.append(t)
            break  # Take the first non-selected team as "3rd place"

terceiros_salvos = st.session_state.get("terceiros_sorteados", [])
terceiros_opcoes = [f"{get_flag(t)} {t}" for t in terceiros_disponiveis]

terceiros_selecionados = st.multiselect(
    "8 Melhores Terceiros",
    terceiros_opcoes,
    default=[f"{get_flag(t)} {t}" for t in terceiros_salvos if t in terceiros_disponiveis],
    max_selections=8,
    key="terceiros_multiselect",
)
terceiros_clean = [t.split(" ", 1)[1] if " " in t else t for t in terceiros_selecionados]

# ── 3. Group match predictions ──────────────────────────────────
st.markdown("---")
st.markdown('<div class="bracket-round-header">⚽ PALPITES DA FASE DE GRUPOS</div>', unsafe_allow_html=True)
st.caption("Preveja o placar de cada jogo por rodada:")

tab_labels = [f"Rodada {r} — {GRUPO_DATAS[r]}" for r in [1, 2, 3]]
tabs = st.tabs(tab_labels)

palpites_grupos = {}

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

            # Banner do grupo
            st.markdown(f'<div class="bracket-round-header">⚽ {grupo_label_with_flags(grupo_letra)}</div>', unsafe_allow_html=True)

            for idx, (casa, fora) in enumerate(jogos_grupo):
                casa_flag = get_flag_html(casa, 20)
                fora_flag = get_flag_html(fora, 20)
                data_hora = GRUPO_JOGOS_DATAS.get((rodada_num, grupo_letra, casa, fora), "")
                data_str = f"<small style='color:#999'>⏰ {data_hora} BRT</small>" if data_hora else ""

                pkey = (rodada_num, grupo_letra, casa, fora)
                salvo = palpites_salvos.get(pkey, {})
                val_casa = salvo.get("placar_casa", 0)
                val_fora = salvo.get("placar_fora", 0)

                # Card do jogo
                st.markdown(f'<div class="match-card">{data_str}</div>', unsafe_allow_html=True)
                col_casa, col_pc, col_vs, col_pf, col_fora = st.columns([3, 1, 0.5, 1, 3])
                with col_casa:
                    st.markdown(f"**{casa_flag} {casa}**", unsafe_allow_html=True)
                with col_pc:
                    placar_casa = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_casa,
                        key=f"pc_r{rodada_num}_{grupo_letra}_{idx}",
                        label_visibility="collapsed",
                    )
                with col_vs:
                    st.markdown("<div style='text-align:center;padding-top:0.3rem;color:#999'>x</div>", unsafe_allow_html=True)
                with col_pf:
                    placar_fora = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_fora,
                        key=f"pf_r{rodada_num}_{grupo_letra}_{idx}",
                        label_visibility="collapsed",
                    )
                with col_fora:
                    st.markdown(f"**{fora_flag} {fora}**", unsafe_allow_html=True)

                palpites_grupos[(rodada_num, grupo_letra, casa, fora)] = {
                    "placar_casa": placar_casa,
                    "placar_fora": placar_fora,
                }

# ── 5. Bracket predictions (Mata-Mata) ─────────────────────────
st.markdown("---")
st.markdown('<div class="bracket-round-header">🏆 PALPITES — MATA-MATA (TODAS AS FASES)</div>', unsafe_allow_html=True)
st.caption("Selecione o vencedor de cada confronto. As fases seguintes dependem dos palpites anteriores.")

# Load saved bracket palpites
palpites_bracket_row = supabase.table("palpites_bracket").select("palpites").eq("participante_id", participante_id).execute()
bracket_salvo = palpites_bracket_row.data[0]["palpites"] if palpites_bracket_row.data else {}

# Helper: resolve position label to team name
def resolve_team(label, classificacao, terceiros_list, previous_winners):
    """Resolve a position label (1A, 2B, T3_1, W_R32_2, etc.) to a team name."""
    if not label:
        return None
    # Group positions
    if label.startswith("1") and len(label) == 2:
        grupo = label[1]
        return classificacao.get(grupo, {}).get("primeiro")
    if label.startswith("2") and len(label) == 2:
        grupo = label[1]
        return classificacao.get(grupo, {}).get("segundo")
    # Third places
    if label.startswith("T3_"):
        idx = int(label.split("_")[1]) - 1
        if terceiros_list and idx < len(terceiros_list):
            return terceiros_list[idx]
        return None
    # Winners from previous rounds
    if label.startswith("W_R32_"):
        idx = int(label.split("_")[2]) - 1
        winners = previous_winners.get("R32", [])
        return winners[idx] if idx < len(winners) else None
    if label.startswith("W_Oit_"):
        idx = int(label.split("_")[2]) - 1
        winners = previous_winners.get("Oitavas", [])
        return winners[idx] if idx < len(winners) else None
    if label.startswith("W_Qua_"):
        idx = int(label.split("_")[2]) - 1
        winners = previous_winners.get("Quartas", [])
        return winners[idx] if idx < len(winners) else None
    if label.startswith("W_Semi_"):
        idx = int(label.split("_")[2]) - 1
        winners = previous_winners.get("Semis", [])
        return winners[idx] if idx < len(winners) else None
    if label.startswith("L_Semi_"):
        idx = int(label.split("_")[2]) - 1
        losers = previous_winners.get("Semis_perdedores", [])
        return losers[idx] if idx < len(losers) else None
    return None

# R32 matchups from data
r32_confrontos = MATA_MATA_RODADAS["R32"]["confrontos"]

# Build bracket predictions round by round
bracket_palpites = {}
bracket_placares = {}
all_previous_winners = dict(bracket_salvo)  # Start with saved data

tab_labels_bracket = [
    f"{MATA_MATA_RODADAS[r]['label']} — {MATA_MATA_RODADAS[r]['data']}"
    for r in ORDEM_RODADAS_MATA_MATA
]
tabs_bracket = st.tabs(tab_labels_bracket)

for tab_bracket, fase_key in zip(tabs_bracket, ORDEM_RODADAS_MATA_MATA):
    with tab_bracket:
        fase_info = MATA_MATA_RODADAS[fase_key]
        confrontos = fase_info["confrontos"]

        # Get saved data for this phase
        fase_palpite_salvo = bracket_salvo.get(fase_key, [])
        fase_placar_salvo = bracket_salvo.get(f"{fase_key}_placares", [])

        winners = []
        placares = []

        for idx, confronto in enumerate(confrontos):
            casa_label = confronto["casa"]
            fora_label = confronto["fora"]
            data_confronto = confronto.get("data", "")

            casa_time = resolve_team(casa_label, resultados, terceiros_clean, all_previous_winners)
            fora_time = resolve_team(fora_label, resultados, terceiros_clean, all_previous_winners)

            # Default saved values
            salvo_vencedor = fase_palpite_salvo[idx] if idx < len(fase_palpite_salvo) else None
            salvo_placar = fase_placar_salvo[idx] if idx < len(fase_placar_salvo) else None
            val_casa = salvo_placar.get("placar_casa", 0) if salvo_placar else 0
            val_fora = salvo_placar.get("placar_fora", 0) if salvo_placar else 0

            if casa_time and fora_time:
                casa_flag = get_flag_html(casa_time, 20)
                fora_flag = get_flag_html(fora_time, 20)
                data_str = f"<small style='color:#999'>⏰ {data_confronto}</small>" if data_confronto else ""

                st.markdown(f'<div class="match-card">{data_str}</div>', unsafe_allow_html=True)

                # Radio for winner
                opcoes_vencedor = [f"{casa_flag} {casa_time}", f"{fora_flag} {fora_time}"]
                default_idx = 0
                if salvo_vencedor:
                    if salvo_vencedor == casa_time:
                        default_idx = 0
                    elif salvo_vencedor == fora_time:
                        default_idx = 1

                col_casa, col_radio, col_fora = st.columns([3, 2, 3])
                with col_casa:
                    st.markdown(f"**{casa_flag} {casa_time}**", unsafe_allow_html=True)
                with col_radio:
                    vencedor_escolha = st.radio(
                        "Vencedor",
                        opcoes_vencedor,
                        index=default_idx,
                        key=f"bracket_{fase_key}_{idx}",
                        horizontal=True,
                        label_visibility="collapsed",
                    )
                with col_fora:
                    st.markdown(f"**{fora_flag} {fora_time}**", unsafe_allow_html=True)

                vencedor = casa_time if vencedor_escolha.startswith(casa_flag) or casa_time in vencedor_escolha else fora_time

                # Score inputs
                col_pc, col_vs, col_pf = st.columns([2, 0.5, 2])
                with col_pc:
                    placar_casa = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_casa,
                        key=f"bpc_{fase_key}_{idx}",
                        label_visibility="collapsed",
                    )
                with col_vs:
                    st.markdown("<div style='text-align:center;padding-top:0.3rem;color:#999'>x</div>", unsafe_allow_html=True)
                with col_pf:
                    placar_fora = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_fora,
                        key=f"bpf_{fase_key}_{idx}",
                        label_visibility="collapsed",
                    )

                winners.append(vencedor)
                placares.append({
                    "casa_time": casa_time,
                    "fora_time": fora_time,
                    "placar_casa": placar_casa,
                    "placar_fora": placar_fora,
                })
            elif casa_time or fora_time:
                # One team missing
                st.warning(f"Confronto {idx+1}: aguardando definição de um dos times ({casa_label} / {fora_label})")
                winners.append(None)
                placares.append(None)
            else:
                st.info(f"Confronto {idx+1}: aguardando definição dos times ({casa_label} vs {fora_label})")
                winners.append(None)
                placares.append(None)

        bracket_palpites[fase_key] = winners
        bracket_placares[f"{fase_key}_placares"] = placares

        # Update previous winners for next round resolution
        all_previous_winners[fase_key] = winners
        if fase_key == "Semis":
            # For Terceiro place match, track losers
            losers = []
            for i, w in enumerate(winners):
                if w and placares[i]:
                    p = placares[i]
                    losers.append(p["fora_time"] if w == p["casa_time"] else p["casa_time"])
                else:
                    losers.append(None)
            all_previous_winners["Semis_perdedores"] = losers

# ── 6. Save ─────────────────────────────────────────────────────
st.markdown("---")
if st.button("💾 Salvar Seleções", type="primary", use_container_width=True):
    erros = []
    for grupo_letra, res in resultados.items():
        if res["primeiro"] and res["segundo"] and res["primeiro"] == res["segundo"]:
            erros.append(f"Grupo {grupo_letra} (mesmo time)")

    if erros:
        st.error(f"Corrija os grupos: {', '.join(erros)}")
    else:
        try:
            # Save selecoes
            supabase.table("selecoes").delete().eq("participante_id", participante_id).execute()
            for grupo_letra, res in resultados.items():
                if res["primeiro"] and res["segundo"]:
                    supabase.table("selecoes").insert({
                        "participante_id": participante_id,
                        "grupo": grupo_letra,
                        "primeiro_lugar": res["primeiro"],
                        "segundo_lugar": res["segundo"],
                    }).execute()

            # Save palpites_grupos
            supabase.table("palpites_grupos").delete().eq("participante_id", participante_id).execute()
            for (rodada, grupo_letra, casa, fora), placar in palpites_grupos.items():
                supabase.table("palpites_grupos").insert({
                    "participante_id": participante_id,
                    "rodada": rodada,
                    "grupo": grupo_letra,
                    "time_casa": casa,
                    "time_fora": fora,
                    "placar_casa": placar["placar_casa"],
                    "placar_fora": placar["placar_fora"],
                }).execute()

            # Save melhores_terceiros
            if terceiros_clean:
                supabase.table("melhores_terceiros").delete().eq("participante_id", participante_id).execute()
                supabase.table("melhores_terceiros").insert({
                    "participante_id": participante_id,
                    "terceiros_selecionados": terceiros_clean,
                }).execute()

            # Save palpites_bracket
            bracket_data = {}
            bracket_data.update(bracket_palpites)
            bracket_data.update(bracket_placares)
            supabase.table("palpites_bracket").delete().eq("participante_id", participante_id).execute()
            supabase.table("palpites_bracket").insert({
                "participante_id": participante_id,
                "palpites": bracket_data,
            }).execute()

            st.success("Seleções e palpites salvos!")
            st.switch_page("pages/3_resultado.py")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

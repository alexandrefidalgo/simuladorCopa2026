import streamlit as st
import pandas as pd
from pathlib import Path
from database.connection import get_supabase
from data.grupos import GRUPOS, get_flag, get_flag_html
from data.jogos import (
    GRUPO_JOGOS_DATAS,
    MATA_MATA_RODADAS, ORDEM_RODADAS_MATA_MATA,
)
from utils.api import build_resultados_from_api
from utils.ui_components import grupo_label_with_flags

st.set_page_config(page_title="Ranking - Copa 2026", page_icon="🏆", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if st.button("← Início", key="voltar_ranking"):
    st.switch_page("app.py")

st.title("🏆 Ranking dos Participantes")

if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

supabase = get_supabase()

# ═══════════════════════════════════════════════════════════════════
# CARREGAR RESULTADOS (DB + API)
# ═══════════════════════════════════════════════════════════════════
if st.button("🔄 Atualizar Resultados", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

resultados_row = supabase.table("resultados").select("*").execute()
resultados_existentes = {}
resultados_grupo = {}
resultados_bracket = {}
for r in resultados_row.data:
    if r["fase"] == "grupo":
        key = (r["rodada"], r["grupo"], r["time_casa"], r["time_fora"])
        resultados_grupo[key] = r
    else:
        key = (r["fase"], r["time_casa"], r["time_fora"])
        resultados_bracket[key] = r
    resultados_existentes[key] = r

# Merge with live API results
api_resultados = build_resultados_from_api()
for key, api_r in api_resultados.items():
    grupo, casa, fora = key[1], key[2], key[3]
    has_real_result = False
    for rodada in [1, 2, 3]:
        db_key = (rodada, grupo, casa, fora)
        if db_key in resultados_grupo:
            r = resultados_grupo[db_key]
            if r.get("gols_casa", 0) > 0 or r.get("gols_fora", 0) > 0:
                has_real_result = True
                break
    if not has_real_result:
        resultados_grupo[key] = api_r

# ═══════════════════════════════════════════════════════════════════
# CLASSIFICAÇÃO EM TEMPO REAL DOS GRUPOS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">⚽ CLASSIFICAÇÃO DOS GRUPOS — AO VIVO</div>', unsafe_allow_html=True)
st.caption("1º e 2º → Rodada de 32 | 3º → Melhores 8 | 4º → Eliminado")

tab_labels_grupos = [grupo_label_with_flags(g) for g in GRUPOS.keys()]
tabs_grupos = st.tabs(tab_labels_grupos)

for tab_grupo, grupo_letra in zip(tabs_grupos, GRUPOS.keys()):
    with tab_grupo:
        times_grupo = GRUPOS[grupo_letra]
        stats = {}
        for t in times_grupo:
            stats[t] = {"jogos": 0, "v": 0, "e": 0, "d": 0, "gf": 0, "gc": 0, "sg": 0, "pontos": 0}

        for key, r in resultados_grupo.items():
            if key[1] != grupo_letra:
                continue
            gc, gf = r["gols_casa"], r["gols_fora"]
            if gc == 0 and gf == 0:
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
            stats[casa]["gf"] += gc
            stats[casa]["gc"] += gf
            stats[fora]["gf"] += gf
            stats[fora]["gc"] += gc
            stats[casa]["sg"] = stats[casa]["gf"] - stats[casa]["gc"]
            stats[fora]["sg"] = stats[fora]["gf"] - stats[fora]["gc"]

            if gc > gf:
                stats[casa]["v"] += 1
                stats[casa]["pontos"] += 3
                stats[fora]["d"] += 1
            elif gf > gc:
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
            pos_str = f"{pos+1}°"
            flag = get_flag(time)
            rows.append({
                "Pos": pos_str,
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

# ═══════════════════════════════════════════════════════════════════
# MELHORES TERCEIROS
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">🎲 MELHORES TERCEIROS</div>', unsafe_allow_html=True)

# Calcular terceiros de cada grupo baseado nos resultados reais
terceiros_por_grupo = {}
for grupo_letra in GRUPOS.keys():
    times_grupo = GRUPOS[grupo_letra]
    stats = {}
    for t in times_grupo:
        stats[t] = {"pontos": 0, "sg": 0, "gf": 0}

    for key, r in resultados_grupo.items():
        if key[1] != grupo_letra:
            continue
        gc, gf = r["gols_casa"], r["gols_fora"]
        # Skip empty 0x0 results if a real result exists
        if gc == 0 and gf == 0:
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

        if gc > gf:
            stats[casa]["pontos"] += 3
        elif gf > gc:
            stats[fora]["pontos"] += 3
        else:
            stats[casa]["pontos"] += 1
            stats[fora]["pontos"] += 1

        stats[casa]["sg"] += gc - gf
        stats[fora]["sg"] += gf - gc
        stats[casa]["gf"] += gc
        stats[fora]["gf"] += gf

    # Ordenar por pontos, SG, GF
    ranking_grupo = sorted(stats.items(), key=lambda x: (x[1]["pontos"], x[1]["sg"], x[1]["gf"]), reverse=True)
    if len(ranking_grupo) >= 3:
        terceiros_por_grupo[grupo_letra] = {
            "time": ranking_grupo[2][0],
            "pontos": ranking_grupo[2][1]["pontos"],
            "sg": ranking_grupo[2][1]["sg"],
            "gf": ranking_grupo[2][1]["gf"],
        }

if terceiros_por_grupo:
    st.markdown("**Classificação dos terceiros lugares:**")

    rows_t = []
    for grupo_letra, info in sorted(terceiros_por_grupo.items(), key=lambda x: (x[1]["pontos"], x[1]["sg"], x[1]["gf"]), reverse=True):
        flag = get_flag(info["time"])
        rows_t.append({
            "Grupo": grupo_letra,
            "Terceiro": f"{flag} {info['time']}",
            "Pontos": info["pontos"],
            "SG": info["sg"],
            "GF": info["gf"],
        })

    df_ter = pd.DataFrame(rows_t)
    st.dataframe(df_ter, use_container_width=True, hide_index=True)

    # Top 8
    top8 = sorted(terceiros_por_grupo.items(), key=lambda x: (x[1]["pontos"], x[1]["sg"], x[1]["gf"]), reverse=True)[:8]

    st.markdown("**🏆 Top 8 Melhores Terceiros:**")
    top8_nomes = [info["time"] for _, info in top8]
    top8_display = [f"{get_flag_html(t, 20)} {t}" for t in top8_nomes]
    st.markdown(" &nbsp; | &nbsp; ".join(top8_display), unsafe_allow_html=True)

    # Salvar terceiros confirmados (global)
    if st.button("✅ Confirmar Top 8 Terceiros", type="primary", use_container_width=True):
        try:
            # Limpar terceiros anteriores e salvar os confirmados
            supabase.table("melhores_terceiros").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            supabase.table("melhores_terceiros").insert({
                "participante_id": participante_id,
                "terceiros_selecionados": sorted(top8_nomes),
            }).execute()
            st.success("Top 8 terceiros confirmados!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
else:
    st.info("Registre os resultados da fase de grupos para calcular os melhores terceiros.")

# ═══════════════════════════════════════════════════════════════════
# COMPARAÇÃO POR JOGO + RANKING
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="bracket-round-header">📊 COMPARAÇÃO POR JOGO</div>', unsafe_allow_html=True)

palpites_grupos_all = supabase.table("palpites_grupos").select("*").execute()
palpites_bracket_all = supabase.table("palpites_bracket").select("*").execute()
participantes_data = supabase.table("participantes").select("id, nome_completo").execute()
participantes_map = {p["id"]: p["nome_completo"] for p in participantes_data.data}



# ── Função para calcular pontos ──────────────────────────────────
def calcular_pontos(part_id):
    pontos = 0
    detalhes = []

    palpites_p = [p for p in palpites_grupos_all.data if p["participante_id"] == part_id]
    for palpite in palpites_p:
        key = (palpite["rodada"], palpite["grupo"], palpite["time_casa"], palpite["time_fora"])
        resultado = resultados_grupo.get(key)
        # Fallback: API results have rodada=0, match by (grupo, casa, fora)
        if not resultado:
            resultado = resultados_grupo.get((0, palpite["grupo"], palpite["time_casa"], palpite["time_fora"]))
        # Fallback: try reversed matchup order
        reversed_key = (palpite["rodada"], palpite["grupo"], palpite["time_fora"], palpite["time_casa"])
        if not resultado:
            resultado = resultados_grupo.get(reversed_key)
        if not resultado:
            resultado = resultados_grupo.get((0, palpite["grupo"], palpite["time_fora"], palpite["time_casa"]))
        # If found result is 0x0, check if API has a better result
        if resultado and resultado.get("gols_casa", 0) == 0 and resultado.get("gols_fora", 0) == 0:
            for try_key in [
                (0, palpite["grupo"], palpite["time_casa"], palpite["time_fora"]),
                (0, palpite["grupo"], palpite["time_fora"], palpite["time_casa"]),
            ]:
                api_r = resultados_grupo.get(try_key)
                if api_r and (api_r.get("gols_casa", 0) > 0 or api_r.get("gols_fora", 0) > 0):
                    resultado = api_r
                    break
        data_hora = GRUPO_JOGOS_DATAS.get(key, "")
        p_casa, p_fora = palpite["placar_casa"], palpite["placar_fora"]

        if resultado:
            r_casa, r_fora = resultado["gols_casa"], resultado["gols_fora"]

            if r_casa > r_fora: vencedor_real = "casa"
            elif r_fora > r_casa: vencedor_real = "fora"
            else: vencedor_real = "empate"

            if p_casa > p_fora: vencedor_palpite = "casa"
            elif p_fora > p_casa: vencedor_palpite = "fora"
            else: vencedor_palpite = "empate"

            if p_casa == r_casa and p_fora == r_fora:
                pts, tipo = 4, "placar_exato"
            elif vencedor_palpite == vencedor_real:
                pts, tipo = 1, "resultado"
            else:
                pts, tipo = 0, "errou"

            pontos += pts
            detalhes.append({
                "data": data_hora,
                "fase": f"Grupo {palpite['grupo']}",
                "jogo": f"{get_flag(palpite['time_casa'])} {palpite['time_casa']} x {palpite['time_fora']} {get_flag(palpite['time_fora'])}",
                "palpite": f"{p_casa}x{p_fora}",
                "real": f"{r_casa}x{r_fora}",
                "pontos": pts,
                "tipo": tipo,
            })
        else:
            detalhes.append({
                "data": data_hora,
                "fase": f"Grupo {palpite['grupo']}",
                "jogo": f"{get_flag(palpite['time_casa'])} {palpite['time_casa']} x {palpite['time_fora']} {get_flag(palpite['time_fora'])}",
                "palpite": f"{p_casa}x{p_fora}",
                "real": "Aguardando",
                "pontos": 0,
                "tipo": "aguardando",
            })

    palpites_b = [p for p in palpites_bracket_all.data if p["participante_id"] == part_id]
    for palpite_row in palpites_b:
        palpites = palpite_row["palpites"]
        for fase_key in ORDEM_RODADAS_MATA_MATA:
            fase_palpites = palpites.get(fase_key, [])
            fase_placares = palpites.get(f"{fase_key}_placares", [])

            for i, vencedor_palpite in enumerate(fase_palpites):
                if not vencedor_palpite:
                    continue
                placar_info = fase_placares[i] if i < len(fase_placares) else None
                if not placar_info:
                    continue

                casa_time = placar_info.get("casa_time", "")
                fora_time = placar_info.get("fora_time", "")
                resultado = resultados_bracket.get((fase_key, casa_time, fora_time))

                if resultado:
                    r_casa, r_fora = resultado["gols_casa"], resultado["gols_fora"]
                    if r_casa > r_fora: vencedor_real = casa_time
                    elif r_fora > r_casa: vencedor_real = fora_time
                    else: vencedor_real = casa_time

                    # Data do confronto
                    confronto_data = MATA_MATA_RODADAS[fase_key]["confrontos"]
                    data_str = ""
                    for cd in confronto_data:
                        if cd.get("casa") == casa_time or cd.get("fora") == fora_time:
                            data_str = cd.get("data", "")
                            break

                    p_casa = placar_info.get("placar_casa", 0)
                    p_fora = placar_info.get("placar_fora", 0)

                    if vencedor_palpite == vencedor_real:
                        if p_casa == r_casa and p_fora == r_fora:
                            pts, tipo = 4, "placar_exato"
                        else:
                            pts, tipo = 1, "resultado"
                    else:
                        pts, tipo = 0, "errou"

                    pontos += pts
                    detalhes.append({
                        "data": data_str,
                        "fase": MATA_MATA_RODADAS[fase_key]["label"],
                        "jogo": f"{get_flag(casa_time)} {casa_time} x {fora_time} {get_flag(fora_time)}",
                        "palpite": vencedor_palpite,
                        "real": f"{vencedor_real} ({r_casa}x{r_fora})",
                        "pontos": pts,
                        "tipo": tipo,
                    })

    return pontos, detalhes

# ── Calcular ranking ─────────────────────────────────────────────
ranking = []
for part_id, nome in participantes_map.items():
    pts, detalhes = calcular_pontos(part_id)
    ranking.append({"participante_id": part_id, "nome": nome, "pontos": pts, "detalhes": detalhes})

ranking.sort(key=lambda x: x["pontos"], reverse=True)

# ── Exibir ranking ───────────────────────────────────────────────
if ranking:
    rows = []
    for i, entry in enumerate(ranking):
        pos = i + 1
        if pos == 1: pos_str = "🥇 1º"
        elif pos == 2: pos_str = "🥈 2º"
        elif pos == 3: pos_str = "🥉 3º"
        else: pos_str = f"{pos}º"
        rows.append({"Posição": pos_str, "Participante": entry["nome"], "Pontos": entry["pontos"]})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Regras de Pontuação ───────────────────────────────────────
    with st.expander("📖 Regras de Pontuação", expanded=False):
        st.markdown("""
        | Acerto | Pontos |
        |---|:---:|
        | ⚽ **Placar exato** (vitória ou empate) | **4** |
        | 🎯 **Acertar o resultado** (errando placar) | **1** |
        | ❌ **Errou** o resultado | **0** |
        """)
        st.markdown("**Exemplos:**")
        br_flag = get_flag_html("Brasil", 18)
        ar_flag = get_flag_html("Argentina", 18)
        fr_flag = get_flag_html("França", 18)
        de_flag = get_flag_html("Alemanha", 18)
        st.markdown(f"""
        - **Jogo:** {br_flag} **Brasil** 2 x 1 **Argentina** {ar_flag}
          - Aposta 2x1 → **4 pts** (placar exato)
          - Aposta 2x0 (Brasil vence) → **1 pt** (acertou vencedor)
          - Aposta 1x2 → **0 pts** (errou)

        - **Jogo:** {fr_flag} **França** 1 x 1 **Alemanha** {de_flag} (empate)
          - Aposta 1x1 → **4 pts** (placar exato de empate)
          - Aposta 2x2 (empate) → **1 pt** (acertou que seria empate)
          - Aposta 2x1 → **0 pts** (errou)
        """, unsafe_allow_html=True)

    # ── Detalhes por jogo ────────────────────────────────────────
    st.markdown('<div class="bracket-round-header">📋 COMPARAÇÃO POR JOGO — TODOS OS PARTICIPANTES</div>', unsafe_allow_html=True)

    # Agrupar todos os detalhes por jogo
    todos_detalhes = []
    for entry in ranking:
        for d in entry["detalhes"]:
            todos_detalhes.append({
                "participante": entry["nome"],
                **d,
            })

    if todos_detalhes:
        df_todos = pd.DataFrame(todos_detalhes)

        # Tabs por fase (sem R32)
        fases_disponiveis = sorted(df_todos["fase"].unique(), key=lambda x: (
            0 if "Grupo" in x else
            1 if "Oitavas" in x else
            2 if "Quartas" in x else
            3 if "Semi" in x else
            4 if "Terceiro" in x else
            5
        ))
        fases_disponiveis = [f for f in fases_disponiveis if "Rodada de 32" not in f]

        tabs_fases = st.tabs(fases_disponiveis)
        for tab_fase, fase in zip(tabs_fases, fases_disponiveis):
            with tab_fase:
                df_fase = df_todos[df_todos["fase"] == fase]
                jogos = df_fase["jogo"].unique()

                for jogo in jogos:
                    df_jogo = df_fase[df_fase["jogo"] == jogo]
                    data_info = df_jogo.iloc[0]["data"]
                    real_info = df_jogo.iloc[0]["real"]

                    # Header do jogo
                    st.markdown(f'<div class="match-detail-header"><strong>⚽ {jogo}</strong> — {real_info} ⏰ {data_info}</div>', unsafe_allow_html=True)

                    rows_jogo = []
                    for _, row in df_jogo.iterrows():
                        if row["tipo"] == "aguardando":
                            emoji = "⏳"
                        elif row["tipo"] == "placar_exato":
                            emoji = "✅"
                        elif row["tipo"] == "resultado":
                            emoji = "🟡"
                        else:
                            emoji = "❌"
                        rows_jogo.append({
                            "Participante": row["participante"],
                            "Palpite": row["palpite"],
                            "Pontos": f"{emoji} {row['pontos']}",
                        })

                    st.dataframe(pd.DataFrame(rows_jogo), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum resultado registrado para comparar.")
else:
    st.info("Nenhum participante com palpites registrados.")

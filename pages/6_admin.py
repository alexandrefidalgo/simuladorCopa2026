import streamlit as st
from pathlib import Path
from database.connection import get_supabase
from data.grupos import GRUPOS, get_flag, get_flag_html, time_com_bandeira
from data.jogos import GRUPO_RODADAS, GRUPO_DATAS, GRUPO_JOGOS_DATAS
from utils.ui_components import render_grupo_simples, grupo_label_with_flags

st.set_page_config(page_title="Admin - Copa 2026", page_icon="👑", layout="wide")

css_path = Path(__file__).parent.parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# ── Auth check ──────────────────────────────────────────────────
if "participante_id" not in st.session_state:
    st.switch_page("pages/0_login.py")

if not st.session_state.get("admin", False):
    st.error("Acesso restrito a administradores.")
    st.stop()

if st.button("← Início", key="voltar_admin"):
    st.switch_page("app.py")

st.title("👑 Painel Admin — Palpites dos Participantes")

supabase = get_supabase()

# ── Select participant ──────────────────────────────────────────
participantes_data = supabase.table("participantes").select("id, nome_completo").execute()
participantes_map = {p["id"]: p["nome_completo"] for p in participantes_data.data}
participantes_list = list(participantes_map.values())
participantes_ids = list(participantes_map.keys())

selected_name = st.selectbox("Selecionar Participante", participantes_list, key="admin_select_part")
selected_id = [k for k, v in participantes_map.items() if v == selected_name][0]

st.markdown(f"**Editando palpites de:** {selected_name}")

# ── Load existing data ──────────────────────────────────────────
selecoes_row = supabase.table("selecoes").select("*").eq("participante_id", selected_id).execute()
salvos = {s["grupo"]: s for s in selecoes_row.data}

palpites_grupos_row = supabase.table("palpites_grupos").select("*").eq("participante_id", selected_id).execute()
palpites_salvos = {}
for p in palpites_grupos_row.data:
    key = (p["rodada"], p["grupo"], p["time_casa"], p["time_fora"])
    palpites_salvos[key] = p

# ── TAB 1: Classificação por grupo ─────────────────────────────
st.markdown("---")
st.markdown('<div class="bracket-round-header">⚽ CLASSIFICAÇÃO DOS GRUPOS</div>', unsafe_allow_html=True)

resultados = {}
colunas = st.columns(3)
for i, grupo_letra in enumerate(GRUPOS.keys()):
    with colunas[i % 3]:
        sel = salvos.get(grupo_letra, {})
        with st.container(border=True):
            resultado = render_grupo_simples(
                grupo_letra, f"admin_grupo_{grupo_letra}",
                default_primeiro=sel.get("primeiro_lugar"),
                default_segundo=sel.get("segundo_lugar"),
            )
            resultados[grupo_letra] = resultado

# ── TAB 2: Palpites de placar por rodada ───────────────────────
st.markdown("---")
st.markdown('<div class="bracket-round-header">⚽ PALPITES DE PLACAR</div>', unsafe_allow_html=True)
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

                st.markdown(f'<div class="match-card">{data_str}</div>', unsafe_allow_html=True)
                col_casa, col_pc, col_vs, col_pf, col_fora = st.columns([3, 1, 0.5, 1, 3])
                with col_casa:
                    st.markdown(f"**{casa_flag} {casa}**", unsafe_allow_html=True)
                with col_pc:
                    placar_casa = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_casa,
                        key=f"admin_pc_r{rodada_num}_{grupo_letra}_{idx}",
                        label_visibility="collapsed",
                    )
                with col_vs:
                    st.markdown("<div style='text-align:center;padding-top:0.3rem;color:#999'>x</div>", unsafe_allow_html=True)
                with col_pf:
                    placar_fora = st.number_input(
                        "Gols", min_value=0, max_value=20, value=val_fora,
                        key=f"admin_pf_r{rodada_num}_{grupo_letra}_{idx}",
                        label_visibility="collapsed",
                    )
                with col_fora:
                    st.markdown(f"**{fora_flag} {fora}**", unsafe_allow_html=True)

                palpites_grupos[(rodada_num, grupo_letra, casa, fora)] = {
                    "placar_casa": placar_casa,
                    "placar_fora": placar_fora,
                }

# ── Save ────────────────────────────────────────────────────────
st.markdown("---")
if st.button("💾 Salvar Palpites como Admin", type="primary", use_container_width=True):
    erros = []
    for grupo_letra, res in resultados.items():
        if res["primeiro"] and res["segundo"] and res["primeiro"] == res["segundo"]:
            erros.append(f"Grupo {grupo_letra} (mesmo time)")

    if erros:
        st.error(f"Corrija os grupos: {', '.join(erros)}")
    else:
        try:
            # Save selecoes
            supabase.table("selecoes").delete().eq("participante_id", selected_id).execute()
            for grupo_letra, res in resultados.items():
                if res["primeiro"] and res["segundo"]:
                    supabase.table("selecoes").insert({
                        "participante_id": selected_id,
                        "grupo": grupo_letra,
                        "primeiro_lugar": res["primeiro"],
                        "segundo_lugar": res["segundo"],
                    }).execute()

            # Save palpites_grupos
            supabase.table("palpites_grupos").delete().eq("participante_id", selected_id).execute()
            for (rodada, grupo_letra, casa, fora), placar in palpites_grupos.items():
                supabase.table("palpites_grupos").insert({
                    "participante_id": selected_id,
                    "rodada": rodada,
                    "grupo": grupo_letra,
                    "time_casa": casa,
                    "time_fora": fora,
                    "placar_casa": placar["placar_casa"],
                    "placar_fora": placar["placar_fora"],
                }).execute()

            st.success(f"Palpites de {selected_name} salvos com sucesso!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

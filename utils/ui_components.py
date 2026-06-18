import streamlit as st
from data.grupos import GRUPOS, get_flag, get_flag_html, time_com_bandeira


def _extract_clean_name(display_name: str) -> str:
    """Extract clean team name from '🇧🇷 Brasil' format."""
    if display_name and " " in display_name:
        return display_name.split(" ", 1)[1]
    return display_name


def render_grupo_simples(grupo_letra: str, key_prefix: str,
                         default_primeiro: str | None = None,
                         default_segundo: str | None = None) -> dict:
    """Render a compact group card with green header, team list and selectboxes."""
    times = GRUPOS[grupo_letra]

    # Green header via native markdown
    st.markdown(f"**⚽ Grupo {grupo_letra}**")
    for t in times:
        flag_img = get_flag_html(t, size=20)
        st.markdown(f"{flag_img} {t}", unsafe_allow_html=True)

    # Selection
    opcoes = [""] + [time_com_bandeira(t) for t in times]

    idx_primeiro = 0
    if default_primeiro:
        try:
            idx_primeiro = opcoes.index(time_com_bandeira(default_primeiro))
        except ValueError:
            pass

    idx_segundo = 0
    if default_segundo:
        try:
            idx_segundo = opcoes.index(time_com_bandeira(default_segundo))
        except ValueError:
            pass

    col1, col2 = st.columns(2)
    with col1:
        primeiro = st.selectbox(
            "1o",
            opcoes,
            index=idx_primeiro,
            key=f"{key_prefix}_1o",
            label_visibility="collapsed",
            placeholder="1o Lugar",
        )
    with col2:
        segundo = st.selectbox(
            "2o",
            opcoes,
            index=idx_segundo,
            key=f"{key_prefix}_2o",
            label_visibility="collapsed",
            placeholder="2o Lugar",
        )

    primeiro_clean = _extract_clean_name(primeiro) if primeiro else None
    segundo_clean = _extract_clean_name(segundo) if segundo else None

    return {"primeiro": primeiro_clean, "segundo": segundo_clean}


def grupo_label_with_flags(grupo_letra: str) -> str:
    """Return '⚽ Grupo A — 🇲🇽 🇿🇦 🇰🇷 🇨🇿' format string with team flags."""
    times = GRUPOS.get(grupo_letra, [])
    flags = " ".join(get_flag(t) for t in times)
    return f"⚽ Grupo {grupo_letra} — {flags}"

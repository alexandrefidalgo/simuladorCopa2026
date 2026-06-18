import json
import requests
from data.grupos import GRUPOS

WORLDCUP26_URL = "https://worldcup26.ir/get/games"
WHENISKICKOFF_URL = "https://wheniskickoff.com/data/v1/matches.json"

TEAM_MAP = {
    # FIFA codes
    "MEX": "México", "RSA": "África do Sul", "KOR": "Coreia do Sul", "CZE": "Tchéquia",
    "CAN": "Canadá", "BIH": "Bósnia e Herzegovina", "QAT": "Catar", "SUI": "Suíça",
    "BRA": "Brasil", "MAR": "Marrocos", "HAI": "Haiti", "SCO": "Escócia",
    "USA": "Estados Unidos", "AUS": "Austrália", "PAR": "Paraguai", "TUR": "Turquia",
    "GER": "Alemanha", "CUW": "Curaçao", "CIV": "Costa do Marfim", "ECU": "Equador",
    "NED": "Holanda", "JPN": "Japão", "SWE": "Suécia", "TUN": "Tunísia",
    "BEL": "Bélgica", "EGY": "Egito", "IRN": "Irã", "NZL": "Nova Zelândia",
    "ESP": "Espanha", "CPV": "Cabo Verde", "KSA": "Arábia Saudita", "URU": "Uruguai",
    "FRA": "França", "SEN": "Senegal", "IRQ": "Iraque", "NOR": "Noruega",
    "ARG": "Argentina", "ALG": "Argélia", "AUT": "Áustria", "JOR": "Jordânia",
    "POR": "Portugal", "COD": "RD Congo", "UZB": "Uzbequistão", "COL": "Colômbia",
    "ENG": "Inglaterra", "CRO": "Croácia", "GHA": "Gana", "PAN": "Panamá",
    # English names — wheniskickoff
    "Mexico": "México", "South Africa": "África do Sul", "South Korea": "Coreia do Sul",
    "Czechia": "Tchéquia", "Canada": "Canadá", "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Qatar": "Catar", "Switzerland": "Suíça", "Brazil": "Brasil", "Morocco": "Marrocos",
    "Haiti": "Haiti", "Scotland": "Escócia", "United States": "Estados Unidos",
    "Australia": "Austrália", "Paraguay": "Paraguai", "Turkey": "Turquia",
    "Germany": "Alemanha", "Curaçao": "Curaçao", "Ivory Coast": "Costa do Marfim",
    "Ecuador": "Equador", "Netherlands": "Holanda", "Japan": "Japão", "Sweden": "Suécia",
    "Tunisia": "Tunísia", "Belgium": "Bélgica", "Egypt": "Egito", "Iran": "Irã",
    "New Zealand": "Nova Zelândia", "Spain": "Espanha", "Cape Verde": "Cabo Verde",
    "Saudi Arabia": "Arábia Saudita", "Uruguay": "Uruguai", "France": "França",
    "Senegal": "Senegal", "Iraq": "Iraque", "Norway": "Noruega", "Argentina": "Argentina",
    "Algeria": "Argélia", "Austria": "Áustria", "Jordan": "Jordânia", "Portugal": "Portugal",
    "DR Congo": "RD Congo", "Uzbekistan": "Uzbequistão", "Colombia": "Colômbia",
    "England": "Inglaterra", "Croatia": "Croácia", "Ghana": "Gana", "Panama": "Panamá",
    "Congo DR": "RD Congo",
    # English names — worldcup26.ir
    "Czech Republic": "Tchéquia", "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Democratic Republic of the Congo": "RD Congo",
    # Portuguese names (pass through)
    "México": "México", "África do Sul": "África do Sul", "Coreia do Sul": "Coreia do Sul",
    "Tchéquia": "Tchéquia", "Canadá": "Canadá", "Bósnia e Herzegovina": "Bósnia e Herzegovina",
    "Catar": "Catar", "Suíça": "Suíça", "Brasil": "Brasil", "Marrocos": "Marrocos",
    "Haiti": "Haiti", "Escócia": "Escócia", "Estados Unidos": "Estados Unidos",
    "Austrália": "Austrália", "Paraguai": "Paraguai", "Turquia": "Turquia",
    "Alemanha": "Alemanha", "Curaçao": "Curaçao", "Costa do Marfim": "Costa do Marfim",
    "Equador": "Equador", "Holanda": "Holanda", "Japão": "Japão", "Suécia": "Suécia",
    "Tunísia": "Tunísia", "Bélgica": "Bélgica", "Egito": "Egito", "Irã": "Irã",
    "Nova Zelândia": "Nova Zelândia", "Espanha": "Espanha", "Cabo Verde": "Cabo Verde",
    "Arábia Saudita": "Arábia Saudita", "Uruguai": "Uruguai", "França": "França",
    "Senegal": "Senegal", "Iraque": "Iraque", "Noruega": "Noruega", "Argentina": "Argentina",
    "Argélia": "Argélia", "Áustria": "Áustria", "Jordânia": "Jordânia", "Portugal": "Portugal",
    "RD Congo": "RD Congo", "Uzbequistão": "Uzbequistão", "Colômbia": "Colômbia",
    "Inglaterra": "Inglaterra", "Croácia": "Croácia", "Gana": "Gana", "Panamá": "Panamá",
}

ALL_TEAMS = set()
for times in GRUPOS.values():
    ALL_TEAMS.update(times)


def normalize_team(name: str) -> str | None:
    return TEAM_MAP.get(name)


def _fetch_worldcup26() -> list[dict]:
    """Fetch from worldcup26.ir."""
    try:
        resp = requests.get(WORLDCUP26_URL, timeout=20, verify=False)
        resp.raise_for_status()
        data = resp.json()
        games = data.get("games", data.get("data", data)) if isinstance(data, dict) else data
        if not isinstance(games, list):
            return []

        matches = []
        for g in games:
            home_en = g.get("home_team_name_en", "")
            away_en = g.get("away_team_name_en", "")
            home_pt = normalize_team(home_en)
            away_pt = normalize_team(away_en)
            if not home_pt or not away_pt:
                continue

            finished = str(g.get("finished", "")).upper() == "TRUE"
            group = g.get("group", "")
            if group not in GRUPOS:
                continue

            sh = g.get("home_score")
            sa = g.get("away_score")
            try:
                sh = int(sh) if sh not in (None, "", "null") else None
                sa = int(sa) if sa not in (None, "", "null") else None
            except (ValueError, TypeError):
                sh = sa = None

            matches.append({
                "home": home_pt,
                "away": away_pt,
                "status": "FINISHED" if finished else "SCHEDULED",
                "score_home": sh,
                "score_away": sa,
                "group": group,
            })
        return matches
    except Exception:
        return []


def _fetch_wheniskickoff() -> list[dict]:
    """Fetch from wheniskickoff.com (static, slower updates)."""
    try:
        resp = requests.get(WHENISKICKOFF_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    matches = []
    for m in data.get("data", []):
        home_pt = normalize_team(m.get("home_name", "") or m.get("home", ""))
        away_pt = normalize_team(m.get("away_name", "") or m.get("away", ""))
        if not home_pt or not away_pt:
            continue

        status = m.get("status", "")
        score_home = m.get("score_home")
        score_away = m.get("score_away")
        group = m.get("group", "")
        if group not in GRUPOS:
            continue

        matches.append({
            "home": home_pt,
            "away": away_pt,
            "status": status,
            "score_home": int(score_home) if score_home is not None else None,
            "score_away": int(score_away) if score_away is not None else None,
            "group": group,
        })
    return matches


def fetch_matches() -> list[dict]:
    """Fetch matches: worldcup26.ir (real-time) first, fallback to wheniskickoff.com."""
    matches = _fetch_worldcup26()
    if matches:
        return matches
    return _fetch_wheniskickoff()


def get_finished_group_matches() -> list[dict]:
    """Return group-stage matches that have been played (non-zero scores or FINISHED status)."""
    all_matches = fetch_matches()
    return [
        m for m in all_matches
        if m["group"] in GRUPOS
        and m["score_home"] is not None
        and m["score_away"] is not None
        and (m["status"] == "FINISHED" or m["score_home"] + m["score_away"] > 0)
    ]


def build_resultados_from_api() -> dict:
    """
    Build a resultados dict compatible with existing code.
    Returns: {(0, grupo, time_casa, time_fora): {"gols_casa": int, "gols_fora": int}}
    """
    finished = get_finished_group_matches()
    resultados = {}
    for m in finished:
        key = (0, m["group"], m["home"], m["away"])
        resultados[key] = {
            "gols_casa": m["score_home"],
            "gols_fora": m["score_away"],
        }
    return resultados

# Grupos oficiais da Copa do Mundo FIFA 2026
# 12 grupos (A-L), 4 seleções cada — 48 seleções classificadas

from itertools import combinations

GRUPOS = {
    "A": ["México", "África do Sul", "Coreia do Sul", "Tchéquia"],
    "B": ["Canadá", "Bósnia e Herzegovina", "Catar", "Suíça"],
    "C": ["Brasil", "Marrocos", "Haiti", "Escócia"],
    "D": ["Estados Unidos", "Paraguai", "Austrália", "Turquia"],
    "E": ["Alemanha", "Curaçao", "Costa do Marfim", "Equador"],
    "F": ["Holanda", "Japão", "Suécia", "Tunísia"],
    "G": ["Bélgica", "Egito", "Irã", "Nova Zelândia"],
    "H": ["Espanha", "Cabo Verde", "Arábia Saudita", "Uruguai"],
    "I": ["França", "Senegal", "Iraque", "Noruega"],
    "J": ["Argentina", "Argélia", "Áustria", "Jordânia"],
    "K": ["Portugal", "RD Congo", "Uzbequistão", "Colômbia"],
    "L": ["Inglaterra", "Croácia", "Gana", "Panamá"],
}

# Bandeiras (emojis) por nome de seleção
FLAGS = {
    "México": "🇲🇽",
    "Coreia do Sul": "🇰🇷",
    "África do Sul": "🇿🇦",
    "Tchéquia": "🇨🇿",
    "Canadá": "🇨🇦",
    "Bósnia e Herzegovina": "🇧🇦",
    "Catar": "🇶🇦",
    "Suíça": "🇨🇭",
    "Brasil": "🇧🇷",
    "Marrocos": "🇲🇦",
    "Haiti": "🇭🇹",
    "Escócia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Estados Unidos": "🇺🇸",
    "Austrália": "🇦🇺",
    "Paraguai": "🇵🇾",
    "Turquia": "🇹🇷",
    "Alemanha": "🇩🇪",
    "Curaçao": "🇨🇼",
    "Costa do Marfim": "🇨🇮",
    "Equador": "🇪🇨",
    "Holanda": "🇳🇱",
    "Japão": "🇯🇵",
    "Tunísia": "🇹🇳",
    "Suécia": "🇸🇪",
    "Bélgica": "🇧🇪",
    "Egito": "🇪🇬",
    "Irã": "🇮🇷",
    "Nova Zelândia": "🇳🇿",
    "Espanha": "🇪🇸",
    "Cabo Verde": "🇨🇻",
    "Arábia Saudita": "🇸🇦",
    "Uruguai": "🇺🇾",
    "França": "🇫🇷",
    "Senegal": "🇸🇳",
    "Noruega": "🇳🇴",
    "Iraque": "🇮🇶",
    "Argentina": "🇦🇷",
    "Áustria": "🇦🇹",
    "Argélia": "🇩🇿",
    "Jordânia": "🇯🇴",
    "Portugal": "🇵🇹",
    "RD Congo": "🇨🇩",
    "Uzbequistão": "🇺🇿",
    "Colômbia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croácia": "🇭🇷",
    "Gana": "🇬🇭",
    "Panamá": "🇵🇦",
}

# Códigos ISO 3166-1 para bandeiras via flagcdn.com
FLAG_CODES = {
    "México": "mx",
    "Coreia do Sul": "kr",
    "África do Sul": "za",
    "Tchéquia": "cz",
    "Canadá": "ca",
    "Bósnia e Herzegovina": "ba",
    "Catar": "qa",
    "Suíça": "ch",
    "Brasil": "br",
    "Marrocos": "ma",
    "Haiti": "ht",
    "Escócia": "gb-sct",
    "Estados Unidos": "us",
    "Austrália": "au",
    "Paraguai": "py",
    "Turquia": "tr",
    "Alemanha": "de",
    "Curaçao": "cw",
    "Costa do Marfim": "ci",
    "Equador": "ec",
    "Holanda": "nl",
    "Japão": "jp",
    "Tunísia": "tn",
    "Suécia": "se",
    "Bélgica": "be",
    "Egito": "eg",
    "Irã": "ir",
    "Nova Zelândia": "nz",
    "Espanha": "es",
    "Cabo Verde": "cv",
    "Arábia Saudita": "sa",
    "Uruguai": "uy",
    "França": "fr",
    "Senegal": "sn",
    "Noruega": "no",
    "Iraque": "iq",
    "Argentina": "ar",
    "Áustria": "at",
    "Argélia": "dz",
    "Jordânia": "jo",
    "Portugal": "pt",
    "RD Congo": "cd",
    "Uzbequistão": "uz",
    "Colômbia": "co",
    "Inglaterra": "gb-eng",
    "Croácia": "hr",
    "Gana": "gh",
    "Panamá": "pa",
}


def get_flag(nome_time: str) -> str:
    """Retorna a bandeira emoji de uma seleção (case-insensitive)."""
    if not nome_time:
        return "⚽"
    # Busca exata
    if nome_time in FLAGS:
        return FLAGS[nome_time]
    # Busca case-insensitive
    nome_lower = nome_time.lower()
    for nome, flag in FLAGS.items():
        if nome.lower() == nome_lower:
            return flag
    return "⚽"


def get_flag_html(nome_time: str, size: int = 20) -> str:
    """Retorna tag <img> com bandeira do CDN flagcdn.com (case-insensitive)."""
    if not nome_time:
        return "⚽"
    # Busca exata
    code = FLAG_CODES.get(nome_time, "")
    # Busca case-insensitive
    if not code:
        nome_lower = nome_time.lower()
        for nome, c in FLAG_CODES.items():
            if nome.lower() == nome_lower:
                code = c
                break
    if code:
        return f'<img src="https://flagcdn.com/{code}.svg" width="{size}" alt="{nome_time}" style="vertical-align:middle">'
    return "⚽"


def time_com_bandeira(nome_time: str) -> str:
    """Retorna nome da seleção com bandeira."""
    flag = get_flag(nome_time)
    return f"{flag} {nome_time}"


# Times por grupo (para select boxes)
TODOS_OS_TIMES = []
for grupo, times in GRUPOS.items():
    for time in times:
        TODOS_OS_TIMES.append(time)

# Lista de seleções para o torneio
SELECOES_POR_GRUPO = {grupo: times for grupo, times in GRUPOS.items()}


def gerar_jogos_grupo() -> list[dict]:
    """Gera todos os jogos da fase de grupos (6 jogos por grupo × 12 grupos = 72 jogos)."""
    jogos = []
    for grupo, times in GRUPOS.items():
        for i, j in combinations(range(len(times)), 2):
            jogos.append({
                "grupo": grupo,
                "casa": times[i],
                "fora": times[j],
            })
    return jogos

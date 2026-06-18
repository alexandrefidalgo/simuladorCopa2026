# Cronograma oficial de jogos da Copa do Mundo FIFA 2026
# Organizado por data — fase de grupos (3 rodadas) + mata-mata
# Fonte: wheniskickoff.com — horários em BRT (Horário de Brasília, UTC-3)

from data.grupos import GRUPOS

# ── Fase de Grupos: rodadas × jogos ──────────────────────────────
# Cada rodada tem 24 jogos (2 por grupo). Times do mesmo grupo
# são pareados em rodadas diferentes para garantir 3 jogos por time.
# Estrutura: rodada -> [(grupo, casa, fora), ...]

GRUPO_RODADAS = {
    1: [
        ("A", GRUPOS["A"][0], GRUPOS["A"][1]),
        ("A", GRUPOS["A"][2], GRUPOS["A"][3]),
        ("B", GRUPOS["B"][0], GRUPOS["B"][1]),
        ("B", GRUPOS["B"][2], GRUPOS["B"][3]),
        ("C", GRUPOS["C"][0], GRUPOS["C"][1]),
        ("C", GRUPOS["C"][2], GRUPOS["C"][3]),
        ("D", GRUPOS["D"][0], GRUPOS["D"][1]),
        ("D", GRUPOS["D"][2], GRUPOS["D"][3]),
        ("E", GRUPOS["E"][0], GRUPOS["E"][1]),
        ("E", GRUPOS["E"][2], GRUPOS["E"][3]),
        ("F", GRUPOS["F"][0], GRUPOS["F"][1]),
        ("F", GRUPOS["F"][2], GRUPOS["F"][3]),
        ("G", GRUPOS["G"][0], GRUPOS["G"][1]),
        ("G", GRUPOS["G"][2], GRUPOS["G"][3]),
        ("H", GRUPOS["H"][0], GRUPOS["H"][1]),
        ("H", GRUPOS["H"][2], GRUPOS["H"][3]),
        ("I", GRUPOS["I"][0], GRUPOS["I"][1]),
        ("I", GRUPOS["I"][2], GRUPOS["I"][3]),
        ("J", GRUPOS["J"][0], GRUPOS["J"][1]),
        ("J", GRUPOS["J"][2], GRUPOS["J"][3]),
        ("K", GRUPOS["K"][0], GRUPOS["K"][1]),
        ("K", GRUPOS["K"][2], GRUPOS["K"][3]),
        ("L", GRUPOS["L"][0], GRUPOS["L"][1]),
        ("L", GRUPOS["L"][2], GRUPOS["L"][3]),
    ],
    2: [
        ("A", GRUPOS["A"][0], GRUPOS["A"][2]),
        ("A", GRUPOS["A"][1], GRUPOS["A"][3]),
        ("B", GRUPOS["B"][0], GRUPOS["B"][2]),
        ("B", GRUPOS["B"][1], GRUPOS["B"][3]),
        ("C", GRUPOS["C"][0], GRUPOS["C"][2]),
        ("C", GRUPOS["C"][1], GRUPOS["C"][3]),
        ("D", GRUPOS["D"][0], GRUPOS["D"][2]),
        ("D", GRUPOS["D"][1], GRUPOS["D"][3]),
        ("E", GRUPOS["E"][0], GRUPOS["E"][2]),
        ("E", GRUPOS["E"][1], GRUPOS["E"][3]),
        ("F", GRUPOS["F"][0], GRUPOS["F"][2]),
        ("F", GRUPOS["F"][1], GRUPOS["F"][3]),
        ("G", GRUPOS["G"][0], GRUPOS["G"][2]),
        ("G", GRUPOS["G"][1], GRUPOS["G"][3]),
        ("H", GRUPOS["H"][0], GRUPOS["H"][2]),
        ("H", GRUPOS["H"][1], GRUPOS["H"][3]),
        ("I", GRUPOS["I"][0], GRUPOS["I"][2]),
        ("I", GRUPOS["I"][1], GRUPOS["I"][3]),
        ("J", GRUPOS["J"][0], GRUPOS["J"][2]),
        ("J", GRUPOS["J"][1], GRUPOS["J"][3]),
        ("K", GRUPOS["K"][0], GRUPOS["K"][2]),
        ("K", GRUPOS["K"][1], GRUPOS["K"][3]),
        ("L", GRUPOS["L"][0], GRUPOS["L"][2]),
        ("L", GRUPOS["L"][1], GRUPOS["L"][3]),
    ],
    3: [
        ("A", GRUPOS["A"][0], GRUPOS["A"][3]),
        ("A", GRUPOS["A"][1], GRUPOS["A"][2]),
        ("B", GRUPOS["B"][0], GRUPOS["B"][3]),
        ("B", GRUPOS["B"][1], GRUPOS["B"][2]),
        ("C", GRUPOS["C"][0], GRUPOS["C"][3]),
        ("C", GRUPOS["C"][1], GRUPOS["C"][2]),
        ("D", GRUPOS["D"][0], GRUPOS["D"][3]),
        ("D", GRUPOS["D"][1], GRUPOS["D"][2]),
        ("E", GRUPOS["E"][0], GRUPOS["E"][3]),
        ("E", GRUPOS["E"][1], GRUPOS["E"][2]),
        ("F", GRUPOS["F"][0], GRUPOS["F"][3]),
        ("F", GRUPOS["F"][1], GRUPOS["F"][2]),
        ("G", GRUPOS["G"][0], GRUPOS["G"][3]),
        ("G", GRUPOS["G"][1], GRUPOS["G"][2]),
        ("H", GRUPOS["H"][0], GRUPOS["H"][3]),
        ("H", GRUPOS["H"][1], GRUPOS["H"][2]),
        ("I", GRUPOS["I"][0], GRUPOS["I"][3]),
        ("I", GRUPOS["I"][1], GRUPOS["I"][2]),
        ("J", GRUPOS["J"][0], GRUPOS["J"][3]),
        ("J", GRUPOS["J"][1], GRUPOS["J"][2]),
        ("K", GRUPOS["K"][0], GRUPOS["K"][3]),
        ("K", GRUPOS["K"][1], GRUPOS["K"][2]),
        ("L", GRUPOS["L"][0], GRUPOS["L"][3]),
        ("L", GRUPOS["L"][1], GRUPOS["L"][2]),
    ],
}

# ── Datas das rodadas da fase de grupos ───────────────────────────
GRUPO_DATAS = {
    1: "11-17 Jun",
    2: "18-23 Jun",
    3: "24-27 Jun",
}

# ── Data e hora de cada jogo da fase de grupos (BRT - Horário de Brasília) ──
# Chave: (rodada, grupo, casa, fora) -> "DD Jun HH:MM"
GRUPO_JOGOS_DATAS = {
    # ── Rodada 1 ──────────────────────────────────────────────────
    (1, "A", GRUPOS["A"][0], GRUPOS["A"][1]): "11 Jun 16:00",
    (1, "A", GRUPOS["A"][2], GRUPOS["A"][3]): "11 Jun 23:00",
    (1, "B", GRUPOS["B"][0], GRUPOS["B"][1]): "12 Jun 16:00",
    (1, "B", GRUPOS["B"][2], GRUPOS["B"][3]): "13 Jun 16:00",
    (1, "C", GRUPOS["C"][0], GRUPOS["C"][1]): "13 Jun 19:00",
    (1, "C", GRUPOS["C"][2], GRUPOS["C"][3]): "13 Jun 22:00",
    (1, "D", GRUPOS["D"][0], GRUPOS["D"][1]): "12 Jun 22:00",
    (1, "D", GRUPOS["D"][2], GRUPOS["D"][3]): "14 Jun 01:00",
    (1, "E", GRUPOS["E"][0], GRUPOS["E"][1]): "14 Jun 14:00",
    (1, "E", GRUPOS["E"][2], GRUPOS["E"][3]): "14 Jun 20:00",
    (1, "F", GRUPOS["F"][0], GRUPOS["F"][1]): "14 Jun 17:00",
    (1, "F", GRUPOS["F"][2], GRUPOS["F"][3]): "14 Jun 23:00",
    (1, "G", GRUPOS["G"][0], GRUPOS["G"][1]): "15 Jun 16:00",
    (1, "G", GRUPOS["G"][2], GRUPOS["G"][3]): "15 Jun 22:00",
    (1, "H", GRUPOS["H"][0], GRUPOS["H"][1]): "15 Jun 13:00",
    (1, "H", GRUPOS["H"][2], GRUPOS["H"][3]): "15 Jun 19:00",
    (1, "I", GRUPOS["I"][0], GRUPOS["I"][1]): "16 Jun 16:00",
    (1, "I", GRUPOS["I"][2], GRUPOS["I"][3]): "16 Jun 19:00",
    (1, "J", GRUPOS["J"][0], GRUPOS["J"][1]): "16 Jun 22:00",
    (1, "J", GRUPOS["J"][2], GRUPOS["J"][3]): "17 Jun 01:00",
    (1, "K", GRUPOS["K"][0], GRUPOS["K"][1]): "17 Jun 14:00",
    (1, "K", GRUPOS["K"][2], GRUPOS["K"][3]): "17 Jun 23:00",
    (1, "L", GRUPOS["L"][0], GRUPOS["L"][1]): "17 Jun 17:00",
    (1, "L", GRUPOS["L"][2], GRUPOS["L"][3]): "17 Jun 20:00",
    # ── Rodada 2 ──────────────────────────────────────────────────
    (2, "A", GRUPOS["A"][0], GRUPOS["A"][2]): "18 Jun 22:00",
    (2, "A", GRUPOS["A"][1], GRUPOS["A"][3]): "18 Jun 13:00",
    (2, "B", GRUPOS["B"][0], GRUPOS["B"][2]): "18 Jun 19:00",
    (2, "B", GRUPOS["B"][1], GRUPOS["B"][3]): "18 Jun 16:00",
    (2, "C", GRUPOS["C"][0], GRUPOS["C"][2]): "19 Jun 21:30",
    (2, "C", GRUPOS["C"][1], GRUPOS["C"][3]): "19 Jun 19:00",
    (2, "D", GRUPOS["D"][0], GRUPOS["D"][2]): "19 Jun 16:00",
    (2, "D", GRUPOS["D"][1], GRUPOS["D"][3]): "20 Jun 00:00",
    (2, "E", GRUPOS["E"][0], GRUPOS["E"][2]): "20 Jun 17:00",
    (2, "E", GRUPOS["E"][1], GRUPOS["E"][3]): "20 Jun 21:00",
    (2, "F", GRUPOS["F"][0], GRUPOS["F"][2]): "20 Jun 14:00",
    (2, "F", GRUPOS["F"][1], GRUPOS["F"][3]): "21 Jun 01:00",
    (2, "G", GRUPOS["G"][0], GRUPOS["G"][2]): "21 Jun 16:00",
    (2, "G", GRUPOS["G"][1], GRUPOS["G"][3]): "21 Jun 22:00",
    (2, "H", GRUPOS["H"][0], GRUPOS["H"][2]): "21 Jun 13:00",
    (2, "H", GRUPOS["H"][1], GRUPOS["H"][3]): "21 Jun 19:00",
    (2, "I", GRUPOS["I"][0], GRUPOS["I"][2]): "22 Jun 18:00",
    (2, "I", GRUPOS["I"][1], GRUPOS["I"][3]): "22 Jun 21:00",
    (2, "J", GRUPOS["J"][0], GRUPOS["J"][2]): "22 Jun 14:00",
    (2, "J", GRUPOS["J"][1], GRUPOS["J"][3]): "23 Jun 00:00",
    (2, "K", GRUPOS["K"][0], GRUPOS["K"][2]): "23 Jun 14:00",
    (2, "K", GRUPOS["K"][1], GRUPOS["K"][3]): "23 Jun 23:00",
    (2, "L", GRUPOS["L"][0], GRUPOS["L"][2]): "23 Jun 17:00",
    (2, "L", GRUPOS["L"][1], GRUPOS["L"][3]): "23 Jun 20:00",
    # ── Rodada 3 (simultâneos) ────────────────────────────────────
    (3, "A", GRUPOS["A"][0], GRUPOS["A"][3]): "24 Jun 22:00",
    (3, "A", GRUPOS["A"][1], GRUPOS["A"][2]): "24 Jun 22:00",
    (3, "B", GRUPOS["B"][0], GRUPOS["B"][3]): "24 Jun 16:00",
    (3, "B", GRUPOS["B"][1], GRUPOS["B"][2]): "24 Jun 16:00",
    (3, "C", GRUPOS["C"][0], GRUPOS["C"][3]): "24 Jun 19:00",
    (3, "C", GRUPOS["C"][1], GRUPOS["C"][2]): "24 Jun 19:00",
    (3, "D", GRUPOS["D"][0], GRUPOS["D"][3]): "25 Jun 23:00",
    (3, "D", GRUPOS["D"][1], GRUPOS["D"][2]): "25 Jun 23:00",
    (3, "E", GRUPOS["E"][0], GRUPOS["E"][3]): "25 Jun 17:00",
    (3, "E", GRUPOS["E"][1], GRUPOS["E"][2]): "25 Jun 17:00",
    (3, "F", GRUPOS["F"][0], GRUPOS["F"][3]): "25 Jun 20:00",
    (3, "F", GRUPOS["F"][1], GRUPOS["F"][2]): "25 Jun 20:00",
    (3, "G", GRUPOS["G"][0], GRUPOS["G"][3]): "27 Jun 00:00",
    (3, "G", GRUPOS["G"][1], GRUPOS["G"][2]): "27 Jun 00:00",
    (3, "H", GRUPOS["H"][0], GRUPOS["H"][3]): "26 Jun 21:00",
    (3, "H", GRUPOS["H"][1], GRUPOS["H"][2]): "26 Jun 21:00",
    (3, "I", GRUPOS["I"][0], GRUPOS["I"][3]): "26 Jun 16:00",
    (3, "I", GRUPOS["I"][1], GRUPOS["I"][2]): "26 Jun 16:00",
    (3, "J", GRUPOS["J"][0], GRUPOS["J"][3]): "27 Jun 23:00",
    (3, "J", GRUPOS["J"][1], GRUPOS["J"][2]): "27 Jun 23:00",
    (3, "K", GRUPOS["K"][0], GRUPOS["K"][3]): "27 Jun 20:30",
    (3, "K", GRUPOS["K"][1], GRUPOS["K"][2]): "27 Jun 20:30",
    (3, "L", GRUPOS["L"][0], GRUPOS["L"][3]): "27 Jun 18:00",
    (3, "L", GRUPOS["L"][1], GRUPOS["L"][2]): "27 Jun 18:00",
}


# ── Mata-mata: confrontos por rodada ──────────────────────────────
# Posições usam notação: "1A" = 1º do grupo A, "2B" = 2º do grupo B,
# "T3_X" = melhor terceiro sorteado.
# Cada confronto inclui "data" com data e hora específicas (BRT - Horário de Brasília).

MATA_MATA_RODADAS = {
    "R32": {
        "label": "Rodada de 32",
        "data": "28 Jun - 3 Jul",
        "confrontos": [
            {"casa": "2A", "fora": "2B", "data": "28 Jun 16:00"},
            {"casa": "1E", "fora": "T3_1", "data": "29 Jun 14:00"},
            {"casa": "1F", "fora": "2C", "data": "29 Jun 17:30"},
            {"casa": "1C", "fora": "2F", "data": "29 Jun 22:00"},
            {"casa": "1I", "fora": "T3_2", "data": "30 Jun 14:00"},
            {"casa": "2E", "fora": "2I", "data": "30 Jun 18:00"},
            {"casa": "1A", "fora": "T3_3", "data": "30 Jun 22:00"},
            {"casa": "1L", "fora": "T3_4", "data": "01 Jul 13:00"},
            {"casa": "1D", "fora": "T3_5", "data": "01 Jul 17:00"},
            {"casa": "1G", "fora": "T3_6", "data": "01 Jul 21:00"},
            {"casa": "2K", "fora": "2L", "data": "02 Jul 16:00"},
            {"casa": "1H", "fora": "2J", "data": "02 Jul 20:00"},
            {"casa": "1B", "fora": "T3_7", "data": "03 Jul 00:00"},
            {"casa": "1J", "fora": "2H", "data": "03 Jul 15:00"},
            {"casa": "1K", "fora": "T3_8", "data": "03 Jul 19:00"},
            {"casa": "2D", "fora": "2G", "data": "03 Jul 22:30"},
        ],
    },
    "Oitavas": {
        "label": "Oitavas de Final",
        "data": "4-7 Jul",
        "confrontos": [
            {"casa": "W_R32_2", "fora": "W_R32_3", "data": "04 Jul 14:00"},
            {"casa": "W_R32_1", "fora": "W_R32_4", "data": "04 Jul 18:00"},
            {"casa": "W_R32_5", "fora": "W_R32_6", "data": "05 Jul 17:00"},
            {"casa": "W_R32_7", "fora": "W_R32_8", "data": "05 Jul 21:00"},
            {"casa": "W_R32_9", "fora": "W_R32_10", "data": "06 Jul 16:00"},
            {"casa": "W_R32_11", "fora": "W_R32_12", "data": "06 Jul 21:00"},
            {"casa": "W_R32_13", "fora": "W_R32_14", "data": "07 Jul 13:00"},
            {"casa": "W_R32_15", "fora": "W_R32_16", "data": "07 Jul 17:00"},
        ],
    },
    "Quartas": {
        "label": "Quartas de Final",
        "data": "9-11 Jul",
        "confrontos": [
            {"casa": "W_Oit_1", "fora": "W_Oit_2", "data": "09 Jul 17:00"},
            {"casa": "W_Oit_3", "fora": "W_Oit_4", "data": "10 Jul 16:00"},
            {"casa": "W_Oit_5", "fora": "W_Oit_6", "data": "11 Jul 18:00"},
            {"casa": "W_Oit_7", "fora": "W_Oit_8", "data": "11 Jul 22:00"},
        ],
    },
    "Semis": {
        "label": "Semi-Finais",
        "data": "14-15 Jul",
        "confrontos": [
            {"casa": "W_Qua_1", "fora": "W_Qua_2", "data": "14 Jul 16:00"},
            {"casa": "W_Qua_3", "fora": "W_Qua_4", "data": "15 Jul 16:00"},
        ],
    },
    "Terceiro": {
        "label": "Terceiro Lugar",
        "data": "18 Jul",
        "confrontos": [
            {"casa": "L_Semi_1", "fora": "L_Semi_2", "data": "18 Jul 18:00"},
        ],
    },
    "Final": {
        "label": "Final",
        "data": "19 Jul",
        "confrontos": [
            {"casa": "W_Semi_1", "fora": "W_Semi_2", "data": "19 Jul 16:00"},
        ],
    },
}

# Ordem das rodadas para exibição
ORDEM_RODADAS_MATA_MATA = ["R32", "Oitavas", "Quartas", "Semis", "Terceiro", "Final"]

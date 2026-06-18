import random


def sortear_terceiros(terceiros_grupos: list[str]) -> list[str]:
    """Recebe lista de 12 terceiros (um por grupo), retorna os 8 sorteados."""
    if len(terceiros_grupos) != 12:
        raise ValueError("Devem ser fornecidos exatamente 12 terceiros lugares")
    sorteados = random.sample(terceiros_grupos, 8)
    return sorted(sorteados)


def classificar_grupo(times: list[str]) -> dict:
    """Retorna classificação simulada do grupo (1º e 2º lugar)."""
    return {
        "primeiro": times[0] if len(times) > 0 else None,
        "segundo": times[1] if len(times) > 1 else None,
    }


def montar_bracket(classificacao: dict, terceiros: list[str] | None = None) -> list[dict]:
    """
    Monta bracket de mata-mata (Round of 32) a partir da classificação dos grupos.
    Copa 2026: 12 grupos × 2 = 24 + 8 melhores terceiros = 32 equipes.
    classificacao: {"A": {"primeiro": "Brasil", "segundo": "Argentina"}, ...}
    terceiros: lista dos 8 melhores terceiros lugares (opcional).
    Retorna lista de confrontos do Round of 32 (16 confrontos com terceiros, 12 sem).
    """
    grupos = list(classificacao.keys())

    # Pares de grupos para o Round of 32 (formato oficial FIFA 2026)
    pares = [
        (grupos[0], grupos[1]),   # A vs B
        (grupos[2], grupos[3]),   # C vs D
        (grupos[4], grupos[5]),   # E vs F
        (grupos[6], grupos[7]),   # G vs H
        (grupos[8], grupos[9]),   # I vs J
        (grupos[10], grupos[11]), # K vs L
    ]

    rodada = []

    if terceiros and len(terceiros) == 8:
        # Com terceiros: 16 confrontos
        # Pares 0-3: vencedor vs terceiro, vencedor vs terceiro
        for i, (g1, g2) in enumerate(pares[:4]):
            rodada.append({
                "casa": classificacao[g1]["primeiro"],
                "fora": terceiros[i * 2],
            })
            rodada.append({
                "casa": classificacao[g2]["primeiro"],
                "fora": terceiros[i * 2 + 1],
            })

        # Pares 4-5: formato padrão (vencedor vs segundo)
        for g1, g2 in pares[4:]:
            rodada.append({
                "casa": classificacao[g1]["primeiro"],
                "fora": classificacao[g2]["segundo"],
            })
            rodada.append({
                "casa": classificacao[g2]["primeiro"],
                "fora": classificacao[g1]["segundo"],
            })

        # Segundos lugares deslocados dos pares 0-3 enfrentam entre si
        rodada.append({
            "casa": classificacao[pares[0][0]]["segundo"],
            "fora": classificacao[pares[1][0]]["segundo"],
        })
        rodada.append({
            "casa": classificacao[pares[0][1]]["segundo"],
            "fora": classificacao[pares[1][1]]["segundo"],
        })
        rodada.append({
            "casa": classificacao[pares[2][0]]["segundo"],
            "fora": classificacao[pares[3][0]]["segundo"],
        })
        rodada.append({
            "casa": classificacao[pares[2][1]]["segundo"],
            "fora": classificacao[pares[3][1]]["segundo"],
        })
    else:
        # Sem terceiros: 12 confrontos (formato original)
        for g1, g2 in pares:
            rodada.append({
                "casa": classificacao[g1]["primeiro"],
                "fora": classificacao[g2]["segundo"],
            })
            rodada.append({
                "casa": classificacao[g2]["primeiro"],
                "fora": classificacao[g1]["segundo"],
            })

    return rodada

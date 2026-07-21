"""Regras de negocio do calculo de premiacao.

Os formatos de premiacao (quantidade de colocacoes e percentuais) ficam
isolados em `PrizeTier` / listas de tiers. Isso deixa o caminho pronto para
uma futura tela de "porcentagens personalizadas": bastaria montar uma lista
de `PrizeTier` diferente e passar para `calculate_prizes(tiers=...)` em vez
de depender de `get_default_tiers` ou `build_podium_tiers`.
"""

from app.core.models import PrizePlace, PrizeTier, TournamentResult

# Emoji usado em cada posicao do podio (posicoes sem entrada usam o "🎖️" padrao).
EMOJI_BY_POSITION = {1: "🏆", 2: "🥈", 3: "🥉"}
DEFAULT_EMOJI = "🎖️"

# Percentuais padrao por tamanho de podio (todas somam 100%).
PODIUM_PERCENTAGES: dict[int, list[float]] = {
    1: [100],
    2: [60, 40],
    3: [50, 30, 20],
    4: [40, 30, 20, 10],
    5: [35, 25, 20, 12, 8],
    6: [30, 22, 18, 13, 10, 7],
    7: [28, 20, 16, 12, 10, 8, 6],
    8: [25, 18, 15, 12, 10, 8, 7, 5],
}

MIN_PODIUM_SIZE = min(PODIUM_PERCENTAGES)
MAX_PODIUM_SIZE = max(PODIUM_PERCENTAGES)

# Tamanho do podio usado pelo modo "Automático" conforme a quantidade de jogadores.
PLAYERS_THRESHOLD_FOR_TOP_4 = 10


class ValidationError(ValueError):
    """Erro de validacao de entrada (jogadores / inscrição / tamanho do pódio)."""


def build_podium_tiers(size: int) -> list[PrizeTier]:
    """Monta a lista de PrizeTier para um tamanho de pódio padrao (1 a 8 colocações)."""

    if size not in PODIUM_PERCENTAGES:
        raise ValidationError(
            f"Tamanho de pódio inválido: escolha entre {MIN_PODIUM_SIZE} e {MAX_PODIUM_SIZE}."
        )

    return [
        PrizeTier(
            position=position,
            label=f"{position}º Lugar",
            emoji=EMOJI_BY_POSITION.get(position, DEFAULT_EMOJI),
            percentage=percentage,
        )
        for position, percentage in enumerate(PODIUM_PERCENTAGES[size], start=1)
    ]


def get_default_tiers(num_players: int) -> list[PrizeTier]:
    """Escolhe o formato padrao (Top 3 ou Top 4) conforme a quantidade de jogadores."""

    size = 4 if num_players >= PLAYERS_THRESHOLD_FOR_TOP_4 else 3
    return build_podium_tiers(size)


def validate_inputs(num_players: int, entry_fee: float, podium_size: int | None = None) -> None:
    if num_players <= 0:
        raise ValidationError("A quantidade de jogadores deve ser maior que zero.")
    if entry_fee <= 0:
        raise ValidationError("O valor da inscrição deve ser maior que zero.")
    if podium_size is not None and podium_size > num_players:
        raise ValidationError("O pódio não pode premiar mais colocações do que jogadores.")


def calculate_prizes(
    num_players: int,
    entry_fee: float,
    tiers: list[PrizeTier] | None = None,
    podium_size: int | None = None,
) -> TournamentResult:
    """Calcula a arrecadacao total e a premiacao de cada colocacao.

    - `tiers`: lista explícita de PrizeTier (ponto de extensão para percentuais
      totalmente personalizados no futuro). Tem prioridade sobre `podium_size`.
    - `podium_size`: quantidade de colocações premiadas (1 a 8) usando os
      percentuais padrao de `PODIUM_PERCENTAGES`. Se omitido junto com `tiers`,
      usa o formato automático (Top 3 abaixo de 10 jogadores, Top 4 a partir
      de 10 - `get_default_tiers`).
    """

    validate_inputs(num_players, entry_fee, podium_size if tiers is None else None)

    if tiers is not None:
        active_tiers = tiers
    elif podium_size is not None:
        active_tiers = build_podium_tiers(podium_size)
    else:
        active_tiers = get_default_tiers(num_players)

    total_collected = num_players * entry_fee

    places = [
        PrizePlace(tier=tier, amount=total_collected * tier.percentage / 100)
        for tier in active_tiers
    ]

    return TournamentResult(
        num_players=num_players,
        entry_fee=entry_fee,
        total_collected=total_collected,
        places=places,
    )

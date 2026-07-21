"""Modelos de dados usados pelo calculo de premiacao.

Sao dataclasses simples (facilmente serializaveis) para que features futuras
como historico de torneios, exportacao em PDF/Excel etc. possam reaproveitar
essas mesmas estruturas sem precisar remodelar nada.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PrizeTier:
    """Uma faixa de premiacao: posicao, rotulo exibido, emoji e % da arrecadacao."""

    position: int
    label: str
    emoji: str
    percentage: float  # 0-100


@dataclass(frozen=True)
class PrizePlace:
    """Resultado calculado para uma posicao especifica (faixa + valor em R$)."""

    tier: PrizeTier
    amount: float


@dataclass(frozen=True)
class TournamentResult:
    """Resultado completo do calculo de premiacao de um torneio."""

    num_players: int
    entry_fee: float
    total_collected: float
    places: list[PrizePlace] = field(default_factory=list)

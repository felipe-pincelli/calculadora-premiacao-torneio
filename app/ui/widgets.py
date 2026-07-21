"""Widgets reutilizaveis da interface."""

import customtkinter as ctk

from app.core.formatting import format_brl
from app.core.models import PrizePlace
from app.ui.theme import CORNER_RADIUS, FONT_FAMILY, MEDAL_COLORS


class PrizeCard(ctk.CTkFrame):
    """Cartao que exibe uma colocacao (emoji + rotulo + valor em R$).

    Tem uma faixa colorida à esquerda (ouro/prata/bronze/destaque) para dar
    uma leitura visual imediata de hierarquia do pódio.
    """

    def __init__(
        self,
        master,
        place: PrizePlace,
        card_bg: str,
        text_color: str,
        accent_color: str,
        border_color: str,
        **kwargs,
    ):
        super().__init__(
            master,
            corner_radius=CORNER_RADIUS,
            fg_color=card_bg,
            border_width=1,
            border_color=border_color,
            **kwargs,
        )

        tier = place.tier
        stripe_color = MEDAL_COLORS.get(tier.position, accent_color)

        self.grid_columnconfigure(1, weight=1)

        stripe = ctk.CTkFrame(self, width=6, corner_radius=3, fg_color=stripe_color)
        stripe.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(12, 0), pady=14)
        stripe.grid_propagate(False)

        label_text = ctk.CTkLabel(
            self,
            text=f"{tier.emoji}  {tier.label}",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=text_color,
            anchor="w",
        )
        label_text.grid(row=0, column=1, sticky="w", padx=14, pady=(14, 2))

        value_label = ctk.CTkLabel(
            self,
            text=format_brl(place.amount),
            font=(FONT_FAMILY, 23, "bold"),
            text_color=stripe_color,
            anchor="w",
        )
        value_label.grid(row=1, column=1, sticky="w", padx=14, pady=(0, 14))


class SummaryRow(ctk.CTkFrame):
    """Linha simples de resumo (rotulo a esquerda, valor a direita)."""

    def __init__(self, master, label: str, value: str, text_color: str, muted_color: str, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(
            self, text=label, font=(FONT_FAMILY, 13), text_color=muted_color, anchor="w"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self, text=value, font=(FONT_FAMILY, 13, "bold"), text_color=text_color, anchor="e"
        ).grid(row=0, column=1, sticky="e")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

"""Janela principal da Calculadora de Premiação."""

import customtkinter as ctk

from app.core.formatting import format_brl
from app.core.prize_calculator import (
    MAX_PODIUM_SIZE,
    MIN_PODIUM_SIZE,
    ValidationError,
    calculate_prizes,
)
from app.ui.theme import COLORS, CORNER_RADIUS, FONT_FAMILY, PADDING
from app.ui.widgets import PrizeCard, SummaryRow

WINDOW_TITLE = "Calculadora de Premiação"
WINDOW_SIZE = "480x780"
WINDOW_MIN_SIZE = (420, 600)

PODIUM_AUTO_LABEL = "Automático (por nº de jogadores)"
PODIUM_OPTIONS = [PODIUM_AUTO_LABEL] + [
    f"Top {n}" for n in range(MIN_PODIUM_SIZE, MAX_PODIUM_SIZE + 1)
]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._appearance = ctk.get_appearance_mode().lower()
        if self._appearance not in COLORS:
            self._appearance = "light"

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*WINDOW_MIN_SIZE)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._last_result = None

        self._build_header()
        self._build_scroll_area()
        self._build_form()
        self._build_results_placeholder()

        self._apply_theme()
        self.after(50, self._update_scrollbar_visibility)

    # ------------------------------------------------------------------
    # Construção da UI
    # ------------------------------------------------------------------
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=PADDING, pady=(PADDING, 0))
        header.grid_columnconfigure(0, weight=1)

        self.title_badge = ctk.CTkFrame(header, corner_radius=CORNER_RADIUS)
        self.title_badge.grid(row=0, column=0, sticky="w")

        self.title_label = ctk.CTkLabel(
            self.title_badge,
            text="🏆  Premiação de Torneio",
            font=(FONT_FAMILY, 21, "bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=16, pady=10)

        self.theme_switch = ctk.CTkSwitch(
            header,
            text="Modo escuro",
            command=self._toggle_theme,
            font=(FONT_FAMILY, 12),
        )
        self.theme_switch.grid(row=0, column=1, sticky="e")
        if self._appearance == "dark":
            self.theme_switch.select()

    def _build_scroll_area(self):
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.grid(row=1, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
        self.scroll_area.grid_columnconfigure(0, weight=1)

        # CTkScrollableFrame sempre reserva espaço pra scrollbar, mesmo sem
        # conteúdo suficiente pra rolar. Guardamos o grid original dela pra
        # poder escondê-la/mostrá-la sob demanda (ver _update_scrollbar_visibility).
        self._scrollbar_grid_info = self.scroll_area._scrollbar.grid_info()
        self.scroll_area._scrollbar.grid_remove()
        self.scroll_area.bind("<Configure>", self._update_scrollbar_visibility, add="+")
        self.scroll_area._parent_canvas.bind("<Configure>", self._update_scrollbar_visibility, add="+")

    def _build_form(self):
        self.form_card = ctk.CTkFrame(self.scroll_area, corner_radius=CORNER_RADIUS, border_width=1)
        self.form_card.grid(row=0, column=0, sticky="ew", pady=(0, PADDING))
        self.form_card.grid_columnconfigure(0, weight=1)

        self.players_label = ctk.CTkLabel(
            self.form_card, text="Quantidade de jogadores", font=(FONT_FAMILY, 13), anchor="w"
        )
        self.players_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        self.players_entry = ctk.CTkEntry(
            self.form_card, placeholder_text="Ex: 12", corner_radius=CORNER_RADIUS - 6, height=38
        )
        self.players_entry.grid(row=1, column=0, sticky="ew", padx=20)
        self.players_entry.bind("<Return>", self._on_calculate)

        self.fee_label = ctk.CTkLabel(
            self.form_card, text="Valor da inscrição (R$)", font=(FONT_FAMILY, 13), anchor="w"
        )
        self.fee_label.grid(row=2, column=0, sticky="w", padx=20, pady=(16, 4))

        self.fee_entry = ctk.CTkEntry(
            self.form_card, placeholder_text="Ex: 20,00", corner_radius=CORNER_RADIUS - 6, height=38
        )
        self.fee_entry.grid(row=3, column=0, sticky="ew", padx=20)
        self.fee_entry.bind("<Return>", self._on_calculate)

        self.podium_label = ctk.CTkLabel(
            self.form_card, text="Tamanho do pódio", font=(FONT_FAMILY, 13), anchor="w"
        )
        self.podium_label.grid(row=4, column=0, sticky="w", padx=20, pady=(16, 4))

        self.podium_menu = ctk.CTkOptionMenu(
            self.form_card,
            values=PODIUM_OPTIONS,
            corner_radius=CORNER_RADIUS - 6,
            height=38,
            font=(FONT_FAMILY, 13),
            dropdown_font=(FONT_FAMILY, 13),
        )
        self.podium_menu.set(PODIUM_AUTO_LABEL)
        self.podium_menu.grid(row=5, column=0, sticky="ew", padx=20)

        self.error_label = ctk.CTkLabel(
            self.form_card, text="", font=(FONT_FAMILY, 12), anchor="w"
        )
        self.error_label.grid(row=6, column=0, sticky="ew", padx=20, pady=(12, 0))

        self.calculate_button = ctk.CTkButton(
            self.form_card,
            text="Calcular Premiação",
            font=(FONT_FAMILY, 14, "bold"),
            corner_radius=CORNER_RADIUS - 6,
            height=44,
            command=self._on_calculate,
        )
        self.calculate_button.grid(row=7, column=0, sticky="ew", padx=20, pady=20)

    def _build_results_placeholder(self):
        self.results_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.results_container.grid(row=1, column=0, sticky="ew")
        self.results_container.grid_columnconfigure(0, weight=1)

        self.placeholder_label = ctk.CTkLabel(
            self.results_container,
            text="Preencha os campos acima e clique em \"Calcular Premiação\".",
            font=(FONT_FAMILY, 13),
            wraplength=380,
            justify="left",
        )
        self.placeholder_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------
    def _selected_podium_size(self) -> int | None:
        selection = self.podium_menu.get()
        if selection == PODIUM_AUTO_LABEL:
            return None
        return int(selection.split(" ")[1])

    def _on_calculate(self, _event=None):
        self.error_label.configure(text="")

        raw_players = self.players_entry.get().strip()
        raw_fee = self.fee_entry.get().strip().replace("R$", "").replace(".", "").replace(",", ".")

        if not raw_players or not raw_fee:
            self.error_label.configure(text="Preencha todos os campos.")
            return

        try:
            num_players = int(raw_players)
            entry_fee = float(raw_fee)
        except ValueError:
            self.error_label.configure(text="Use apenas números válidos.")
            return

        try:
            result = calculate_prizes(num_players, entry_fee, podium_size=self._selected_podium_size())
        except ValidationError as exc:
            self.error_label.configure(text=str(exc))
            return

        self._last_result = result
        self._render_results(result)
        self.after(50, self._update_scrollbar_visibility)

    def _render_results(self, result):
        for widget in self.results_container.winfo_children():
            widget.destroy()

        colors = COLORS[self._appearance]
        row = 0

        summary_card = ctk.CTkFrame(
            self.results_container,
            corner_radius=CORNER_RADIUS,
            fg_color=colors["card_bg"],
            border_width=1,
            border_color=colors["card_border"],
        )
        summary_card.grid(row=row, column=0, sticky="ew", pady=(0, PADDING))
        summary_card.grid_columnconfigure(0, weight=1)
        row += 1

        rows = [
            ("Quantidade de jogadores", str(result.num_players)),
            ("Valor da inscrição", format_brl(result.entry_fee)),
            ("Arrecadação total", format_brl(result.total_collected)),
        ]
        for i, (label, value) in enumerate(rows):
            summary_row = SummaryRow(
                summary_card,
                label=label,
                value=value,
                text_color=colors["text"],
                muted_color=colors["text_muted"],
            )
            summary_row.grid(row=i, column=0, sticky="ew", padx=20, pady=(16 if i == 0 else 4, 16 if i == len(rows) - 1 else 4))

        for place in result.places:
            card = PrizeCard(
                self.results_container,
                place=place,
                card_bg=colors["card_bg"],
                text_color=colors["text"],
                accent_color=colors["accent"],
                border_color=colors["card_border"],
            )
            card.grid(row=row, column=0, sticky="ew", pady=(0, 10))
            row += 1

    def _toggle_theme(self):
        self._appearance = "dark" if self.theme_switch.get() else "light"
        ctk.set_appearance_mode(self._appearance)
        self._apply_theme()
        if self._last_result is not None:
            self._render_results(self._last_result)

    def _apply_theme(self):
        colors = COLORS[self._appearance]
        self.configure(fg_color=colors["bg"])
        self.title_badge.configure(fg_color=colors["header_fg_color"])
        self.title_label.configure(text_color=colors["accent"])
        self.form_card.configure(fg_color=colors["card_bg"], border_color=colors["card_border"])
        self.players_label.configure(text_color=colors["text"])
        self.fee_label.configure(text_color=colors["text"])
        self.podium_label.configure(text_color=colors["text"])
        self.error_label.configure(text_color=colors["error"])
        if self.placeholder_label.winfo_exists():
            self.placeholder_label.configure(text_color=colors["text_muted"])
        for entry in (self.players_entry, self.fee_entry):
            entry.configure(fg_color=colors["entry_bg"], border_color=colors["border"], text_color=colors["text"])
        self.podium_menu.configure(
            fg_color=colors["entry_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["accent_hover"],
            text_color=colors["text"],
            dropdown_fg_color=colors["card_bg"],
            dropdown_text_color=colors["text"],
            dropdown_hover_color=colors["accent"],
        )
        self.calculate_button.configure(fg_color=colors["accent"], hover_color=colors["accent_hover"])

    # ------------------------------------------------------------------
    # Scrollbar sob demanda
    # ------------------------------------------------------------------
    def _update_scrollbar_visibility(self, _event=None):
        canvas = self.scroll_area._parent_canvas
        bbox = canvas.bbox("all")
        if not bbox:
            return

        content_height = bbox[3] - bbox[1]
        visible_height = canvas.winfo_height()
        scrollbar = self.scroll_area._scrollbar

        if content_height > visible_height:
            scrollbar.grid(**self._scrollbar_grid_info)
        else:
            scrollbar.grid_remove()

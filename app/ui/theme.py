"""Paleta de cores, fontes e constantes visuais da interface.

Mantido separado da logica de layout para facilitar ajustes de estilo
(e uma eventual troca de tema) sem mexer em `main_window.py`.
"""

FONT_FAMILY = "Segoe UI"

CORNER_RADIUS = 16
PADDING = 22

COLORS = {
    "light": {
        "bg": "#F6F2EA",
        "card_bg": "#FFFFFF",
        "card_border": "#EAE3D6",
        "accent": "#B8860B",
        "accent_hover": "#96700A",
        "text": "#2B2620",
        "text_muted": "#77705F",
        "border": "#E4DFD6",
        "entry_bg": "#FFFFFF",
        "error": "#C0392B",
        "header_fg_color": "#FBE9C8",
    },
    "dark": {
        "bg": "#1B1917",
        "card_bg": "#28241F",
        "card_border": "#3A342C",
        "accent": "#D4AF37",
        "accent_hover": "#B99527",
        "text": "#F2EFE9",
        "text_muted": "#B3AC9F",
        "border": "#3A3632",
        "entry_bg": "#332F2C",
        "error": "#E57373",
        "header_fg_color": "#3A2F14",
    },
}

# Cores de medalha por colocação (independentes do tema — ouro/prata/bronze
# são reconhecíveis em qualquer fundo). Colocações sem entrada aqui caem no
# fallback (cor de destaque do tema).
MEDAL_COLORS = {
    1: "#D4AF37",  # ouro
    2: "#A8AAAD",  # prata
    3: "#C97C3D",  # bronze
}

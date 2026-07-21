"""Formatacao de valores no padrao brasileiro (R$ 0,00)."""


def format_brl(value: float) -> str:
    """Formata um numero como moeda brasileira, ex: 1234.5 -> 'R$ 1.234,50'."""

    formatted = f"{value:,.2f}"
    # f-string usa separador dos EUA (1,234.50); trocamos para o padrao BR (1.234,50).
    formatted = formatted.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return f"R$ {formatted}"

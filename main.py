"""Ponto de entrada da Calculadora de Premiação.

Executar em desenvolvimento: `python main.py`
Gerar o .exe: ver `build.ps1` / README.md.
"""

import sys
from pathlib import Path

import customtkinter as ctk

from app.ui.main_window import App


def resource_path(relative_path: str) -> Path:
    """Resolve um caminho de recurso tanto rodando via `python main.py`
    quanto empacotado pelo PyInstaller (onefile extrai tudo em `sys._MEIPASS`)."""

    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base_path / relative_path


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()

    icon_path = resource_path("assets/icon.ico")
    if icon_path.exists():
        try:
            app.iconbitmap(str(icon_path))
        except Exception:
            pass  # ícone é cosmético — nunca deve impedir o app de abrir

    app.mainloop()


if __name__ == "__main__":
    main()

"""Gera assets/icon.ico e assets/icon.png a partir de assets/trophy_source.png.

`trophy_source.png` é a arte final do troféu (fundo já transparente, recortada
e centralizada num canvas quadrado). Este script só redimensiona/exporta essa
arte nos formatos que o app e o instalador do .exe precisam — roda uma vez
durante o desenvolvimento, não é empacotado no executável final.

Se um dia trocar a arte do troféu, basta substituir `trophy_source.png` por
uma nova imagem (fundo transparente, quadrada) e rodar este script de novo.
"""

from pathlib import Path

from PIL import Image

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
PNG_SIZE = 256


def main():
    assets_dir = Path(__file__).parent
    source = Image.open(assets_dir / "trophy_source.png").convert("RGBA")

    preview = source.resize((PNG_SIZE, PNG_SIZE), Image.LANCZOS)
    preview.save(assets_dir / "icon.png")

    source.save(assets_dir / "icon.ico", sizes=ICO_SIZES)
    print("Ícone gerado em assets/icon.ico e assets/icon.png")


if __name__ == "__main__":
    main()

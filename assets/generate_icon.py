"""Gera assets/icon.ico (troféu dourado simples) usado no .exe e na janela.

Script utilitário — roda uma vez durante o desenvolvimento, não é
empacotado no executável final.
"""

from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256
GOLD = (212, 175, 55, 255)
GOLD_DARK = (168, 130, 30, 255)
BG = (0, 0, 0, 0)


def draw_trophy() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    cx = SIZE // 2

    # Taça (corpo do troféu)
    cup_top = 40
    cup_bottom = 130
    draw.pieslice([cx - 70, cup_top, cx + 70, cup_top + 140], 0, 180, fill=GOLD)
    draw.rectangle([cx - 70, cup_top + 70, cx + 70, cup_bottom], fill=GOLD)

    # Alças laterais
    draw.arc([cx - 110, cup_top + 10, cx - 40, cup_top + 90], 90, 270, fill=GOLD_DARK, width=10)
    draw.arc([cx + 40, cup_top + 10, cx + 110, cup_top + 90], -90, 90, fill=GOLD_DARK, width=10)

    # Haste
    draw.rectangle([cx - 14, cup_bottom, cx + 14, cup_bottom + 40], fill=GOLD_DARK)

    # Base
    draw.rectangle([cx - 50, cup_bottom + 40, cx + 50, cup_bottom + 60], fill=GOLD)
    draw.rectangle([cx - 65, cup_bottom + 60, cx + 65, cup_bottom + 78], fill=GOLD_DARK)

    return img


def main():
    assets_dir = Path(__file__).parent
    img = draw_trophy()

    img.save(assets_dir / "icon.png")
    img.save(
        assets_dir / "icon.ico",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print("Ícone gerado em assets/icon.ico e assets/icon.png")


if __name__ == "__main__":
    main()

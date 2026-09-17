from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ICO = ASSETS / "matrix-windows-commander.ico"
PNG = ASSETS / "matrix-windows-commander.png"


def draw(size: int = 512) -> Image.Image:
    img = Image.new("RGBA", (size, size), (4, 9, 20, 255))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((34, 34, size - 34, size - 34), radius=94, outline=(70, 207, 255, 200), width=22)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))

    d = ImageDraw.Draw(img)
    d.rounded_rectangle((34, 34, size - 34, size - 34), radius=94, fill=(7, 19, 34, 255), outline=(54, 126, 184, 255), width=14)
    d.rounded_rectangle((83, 108, 429, 378), radius=28, fill=(5, 15, 27, 255), outline=(43, 110, 163, 255), width=10)
    d.line((119, 158, 173, 202, 119, 246), fill=(106, 224, 255, 255), width=18, joint="curve")
    d.line((196, 246, 288, 246), fill=(106, 224, 255, 255), width=18)
    for y in (151, 195, 239, 283):
        d.line((316, y, 388, y), fill=(82, 167, 216, 255), width=12)
    d.line((118, 414, 394, 414), fill=(64, 224, 176, 255), width=12)
    return img


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    image = draw()
    image.save(PNG, format="PNG")
    image.save(ICO, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(ICO)
    print(PNG)

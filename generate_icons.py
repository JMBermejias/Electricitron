#!/usr/bin/env python3
"""Generate app icons for Electricitron."""
from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size=512):
    """Create Electricitron app icon."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r = size // 2 - 10

    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill='#2980b9')
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], fill='#1a5276')
    draw.ellipse([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16], fill='#2980b9')

    bolt_color = '#f1c40f'
    bw = size // 8
    points = [
        (cx + bw, cy - r + 20),
        (cx - bw * 2, cy + 5),
        (cx - bw // 2, cy + 5),
        (cx - bw, cy + r - 20),
        (cx + bw * 2, cy - 5),
        (cx + bw // 2, cy - 5),
    ]
    draw.polygon(points, fill=bolt_color)

    for angle_offset in range(0, 360, 45):
        import math
        angle = math.radians(angle_offset)
        x1 = cx + int((r + 5) * math.cos(angle))
        y1 = cy + int((r + 5) * math.sin(angle))
        x2 = cx + int((r + 20) * math.cos(angle))
        y2 = cy + int((r + 20) * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill='#85c1e9', width=max(2, size // 100))

    return img


def main():
    os.makedirs('assets', exist_ok=True)

    icon_512 = create_icon(512)
    icon_512.save('assets/icon.png')
    print("Generated: assets/icon.png (512x512)")

    icon_256 = icon_512.resize((256, 256), Image.Resampling.LANCZOS)
    icon_256.save('assets/icon_256.png')
    print("Generated: assets/icon_256.png (256x256)")

    icon_128 = icon_512.resize((128, 128), Image.Resampling.LANCZOS)
    icon_128.save('assets/icon_128.png')
    print("Generated: assets/icon_128.png (128x128)")

    icon_64 = icon_512.resize((64, 64), Image.Resampling.LANCZOS)
    icon_64.save('assets/icon_64.png')
    print("Generated: assets/icon_64.png (64x64)")

    icon_48 = icon_512.resize((48, 48), Image.Resampling.LANCZOS)
    icon_48.save('assets/icon_48.png')
    print("Generated: assets/icon_48.png (48x48)")

    icon_32 = icon_512.resize((32, 32), Image.Resampling.LANCZOS)
    icon_32.save('assets/icon_32.png')
    print("Generated: assets/icon_32.png (32x32)")

    icon_16 = icon_512.resize((16, 16), Image.Resampling.LANCZOS)
    icon_16.save('assets/icon_16.png')
    print("Generated: assets/icon_16.png (16x16)")

    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = [icon_512.resize(s, Image.Resampling.LANCZOS) for s in ico_sizes]
    ico_images[0].save('assets/icon.ico', format='ICO', sizes=ico_sizes, append_images=ico_images[1:])
    print("Generated: assets/icon.ico")

    print("\nAll icons generated successfully!")


if __name__ == "__main__":
    main()

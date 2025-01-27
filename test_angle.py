# coding: utf-8
from tr import *
from PIL import Image, ImageDraw, ImageFont, ImageOps
import cv2

if __name__ == "__main__":
    img_path = "imgs/id_card.jpeg"

    img_pil = Image.open(img_path)
    MAX_SIZE = 2000
    if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
        scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

        new_width = int(img_pil.width / scale + 0.5)
        new_height = int(img_pil.height / scale + 0.5)
        img_pil = img_pil.resize((new_width, new_height), Image.BICUBIC)

    print(img_pil.width, img_pil.height)

    color_pil = img_pil.convert("RGB")
    gray_pil = img_pil.convert("L")

    rect_arr = detect(gray_pil, FLAG_ROTATED_RECT)

    img_draw = ImageDraw.Draw(color_pil)
    colors = ['red', 'green', 'blue', "purple"]

    for i, rect in enumerate(rect_arr):
        cx, cy, w, h, a = rect
        box = cv2.boxPoints(((cx, cy), (w, h), a))
        box = numpy.int0(box)

        for p1, p2 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            img_draw.line(xy=(box[p1][0], box[p1][1], box[p2][0], box[p2][1]), fill=colors[i % len(colors)], width=2)

    color_pil.save("~color_pil.png")
    color_pil.show()

    blank_pil = Image.new("RGBA", img_pil.size, (255, 255, 255, 255))
    blank_draw = ImageDraw.Draw(blank_pil)

    results = run_angle(gray_pil)
    for line in results:
        cx, cy, w, h, a = line[0]
        if a < -45:
            w, h = h, w
            a += 90

        txt_pil = Image.new('RGBA', (w, h), (255, 255, 255, 0))
        txt_draw = ImageDraw.Draw(txt_pil)

        txt = line[1]
        font = ImageFont.truetype("msyh.ttf", max(int(h * 0.5), 14))

        txt_draw.text(xy=(0, 0), text=txt, font=font, fill=(0, 0, 0, 255))
        txt_pil = txt_pil.rotate(-a, expand=1, resample=Image.BICUBIC)
        blank_pil.paste(txt_pil, (int(cx - w / 2), int(cy - h / 2)), txt_pil)

    blank_pil.show()
    blank_pil.save("~blank_pil.png")
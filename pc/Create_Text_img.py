import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
import matplotlib.pyplot as plt
import numpy as np


def creatData(s, debug=False, size=26, dy=-5):
    length = 0
    size_w = math.floor(160 / size * 2)

    group = []
    i = 0
    last_i = 0
    delta = 0
    for c in s:
        if c == '\n':
            group.append(s[last_i:i])
            delta = 0
            last_i = i
        elif ord(c) < 128:
            length += 1
            delta += 1
        else:
            length += 2
            delta += 2
        if delta >= size_w:
            group.append(s[last_i:i])
            delta = 0
            last_i = i
        i += 1

    if delta != 0:
        group.append(s[last_i:])
    print(group)
    size_h = len(group)
    print(size_w, len(group))
    img = np.zeros((min(size * size_h, 128), min(160, length * 25), 3), dtype='uint8')
    # img.fill(0)
    img_pil = Image.fromarray(img, mode='RGB')
    fontText = ImageFont.truetype("./msyh.ttc", size - 1, encoding="utf-8")

    draw = ImageDraw.Draw(img_pil)
    i = 0
    for s in group:
        print(s)
        draw.text((0, dy + 25 * i), s, font=fontText,
                  fill=0xffffff)
        i += 1
    if debug:
        # img_pil = img_pil.resize((8, 8), Image.NEAREST)
        plt.imshow(img_pil)
        plt.pause(1000)

    return img_pil, (min(160, length * 25), min(size * size_h, 128))


if __name__ == '__main__':
    creatData(r'有两种类型的套接字：基于文件的和面向网络的。', True)

# -*- coding: utf-8 -*-
import string
from PIL import Image


ascii_char = string.printable[:94]


def _get_char(r, g, b, alpha=256):
    """
    灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，黑色为0，故黑白图片也称灰度图像
    gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
    """
    if alpha == 0:
        return ' '

    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    length = len(ascii_char)
    unit = (alpha + 1) / length
    return ascii_char[int(gray/unit)]


def pic_to_ascii(path, width=80, height=80):
    with open(path, "rb") as IMG:
        img = Image.open(IMG)
        img = img.resize((width, height), Image.NEAREST)
        img = img.convert('RGBA')

        txt = ""
        for h in range(height):
            for w in range(width):
                txt += _get_char(*img.getpixel((w, h)))
            txt += "\n"

        return txt


if __name__ == "__main__":
    result = pic_to_ascii('/Users/andy/Documents/wm.png')
    print(result)

# -*- coding: utf-8 -*-
from PIL import *


def makeImgEven(img):
    pixels = list(img.getdata())  # 得到一个这样的列表： [(r,g,b,t),(r,g,b,t)...]
    evenPixels = [(r>>1<<1,g>>1<<1,b>>1<<1,t>>1<<1) for [r,g,b,t] in pixels]  # 更改所有值为偶数（魔法般的移位）
    evenImg = Image.new(image.mode, image.size)  # 创建一个相同大小的图片副本
    evenImg.putdata(evenPixels)  # 把上面的像素放入到图片副本
    return evenImg


def constLenBin(int):
    # 去掉 bin() 返回的二进制字符串中的 '0b'，并在左边补足 '0' 直到字符串长度为 8
    binary = "0" * (8 - (len(bin(int)) - 2)) + bin(int).replace('0b', '')
    return binary


def encodeImg(img, data):
    evenImg = makeImgEven(img)  # 获得最低有效位为 0 的图片副本
    binary = ''.join(map(constLenBin, bytearray(data, 'utf-8')))  # 将需要被隐藏的字符串转换成二进制字符串
    if len(binary) > len(image.getdata()) * 4:  # 如果不可能编码全部数据， 抛出异常
        raise Exception("Error: Can't encode more than " + len(evenImg.getdata()) * 4 + " bits in this image. ")

    encodedPixels = [(r+int(binary[index*4+0]), g+int(binary[index*4+1]), b+int(binary[index*4+2]), t+int(binary[index*4+3])) if index*4 < len(binary) else (r,g,b,t) for index, (r,g,b,t) in enumerate(list(evenImg.getdata()))]  # 将 binary 中的二进制字符串信息编码进像素里
    encodedImg = Image.new(evenImg.mode, evenImg.size)  # 创建新图片以存放编码后的像素
    encodedImg.putdata(encodedPixels)  # 添加编码后的数据
    return encodedImage

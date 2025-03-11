"""
PIL mode说明:
1 (1-bit pixels, black and white, stored with one pixel per byte)
L (8-bit pixels, black and white)，8位灰度图
P (8-bit pixels, mapped to any other mode using a colour palette)，8位彩色图，含调色板
RGB (3x8-bit pixels, true colour)，24位彩色图
RGBA (4x8-bit pixels, true colour with transparency mask)，32位彩色图，含alpha通道
CMYK (4x8-bit pixels, colour separation)，32位彩色，即印刷四色模式，印刷颜色模型
YCbCr (3x8-bit pixels, colour video format)，24位彩色，视频颜色格式
I (32-bit signed integer pixels)，32位有符号整型
F (32-bit floating point pixels)，32位浮点数
"""

from PIL import Image


def get_image_palette(image_path):
    image = Image.open(image_path)

    # 缩小图片，否则计算机压力太大
    image = image.resize((50, 50))
    result = image.convert("P", palette=Image.ADAPTIVE, colors=10)

    # 找到主要的颜色
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)
    colors = []

    for color_count in color_counts:
        index = color_count[1]
        color = palette[index * 3: index * 3 + 3]
        colors.append(tuple(color))

    return colors


def color_hex_string(color: tuple) -> str:
    return '#' + (''.join(map(lambda x: hex(x).replace('0x', '').zfill(2), color)))


def test_image_palette():
    path = '/Users/zhouzhenliang/Desktop/py-tools/ic_launcher.png'
    colors = get_image_palette(path)
    hex_colors = tuple(map(color_hex_string, colors))
    print(hex_colors)

    import matplotlib.pyplot as plt
    x_list = tuple(range(len(hex_colors)))
    y_list = tuple(map(lambda x: 100, x_list))
    plt.bar(x_list, y_list, color=hex_colors)
    plt.show()


if __name__ == '__main__':
    test_image_palette()

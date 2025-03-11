"""
官网: https://pngquant.org/

pngquant是一款功能强大的PNG图片压缩工具，它能够在保持图片质量的同时，显著减少文件大小。
pngquant 是有损压缩
"""
import os.path
import shutil
import time

import pngquant

from pyutils import byte2string


def compress_image(src_path, dst_path):
    pngquant.quant_image(image=src_path, dst=dst_path)


def test_compress():
    path = shutil.which('pngquant')
    pngquant.config(quant_file=path, min_quality=95, max_quality=100, speed=1)
    path1 = '/Users/zhouzhenliang/Desktop/py-tools/bg.png'
    name1, name2 = os.path.splitext(path1)
    path2 = f'{name1}_pngquant{name2}'
    stat_time = time.time()
    compress_image(path1, path2)
    size1 = byte2string(os.path.getsize(path1))
    size2 = byte2string(os.path.getsize(path2))
    duration = round((time.time() - stat_time) * 1000)
    print(f'{size1} -> {size2}, {duration}ms')


if __name__ == '__main__':
    test_compress()

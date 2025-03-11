"""
Pngquant & Zopflipng压缩，效果和tinify效果基本一致
1. Pngquant有损压缩
2. Zopflipng无损压缩
"""
import os.path
import shutil
import time

import subprocess

from pyutils import byte2string


def compress_by_pngquant(src_path, dst_path):
    subprocess.check_call(
        ['pngquant',
         '--speed', '1',  # speed/quality trade-off. 1=slow, 4=default, 11=fast & rough
         '--quality', '95-100',  # don't save below min, use fewer colors below max (0-100)
         '--force',  # overwrite existing output files (synonym: -f)
         '--strip',  # remove optional metadata (default on Mac)
         src_path,
         '--output', dst_path])


def compress_by_zopflipng(src_path, dst_path):
    subprocess.check_call(
        ['zopflipng',
         '-y',  # do not ask about overwriting files.
         # remove colors behind alpha channel 0. No visual difference, removes hidden information.
         '--lossy_transparent',
         '--lossy_8bit',  # convert 16-bit per channel image to 8-bit per channel.
         src_path,
         dst_path])


def test_compress():
    pngquant_path = shutil.which('pngquant')
    print(f'pngquant: {pngquant_path}')
    zopflipng_path = shutil.which('zopflipng')
    print(f'zopflipng: {zopflipng_path}')

    path1 = '/Users/zhouzhenliang/Desktop/py-tools/bg1.png'
    name1, name2 = os.path.splitext(path1)
    path2 = f'{name1}_pngquant{name2}'
    path3 = f'{name1}_pngquant_zopflipng{name2}'
    stat_time = time.time()
    compress_by_pngquant(path1, path2)
    duration1 = round((time.time() - stat_time) * 1000)
    compress_by_zopflipng(path2, path3)
    duration2 = round((time.time() - stat_time) * 1000) - duration1

    size1 = os.path.getsize(path1)
    size2 = os.path.getsize(path2)
    size3 = os.path.getsize(path3)
    size1_txt = byte2string(size1)
    size2_txt = byte2string(size2)
    size3_txt = byte2string(size3)
    print(f'path: {path1}')
    print(f'Pngquant: {size1_txt} -> {size2_txt}, {round(size2 / size1 * 100, 1)}%, {duration1}ms')
    print(f'Zopflipng: {size2_txt} -> {size3_txt}, {round(size3 / size2 * 100, 1)}%, {duration2}ms')
    print(f'Total: {size1_txt} -> {size3_txt}, {round(size3 / size1 * 100, 1)}%, {duration1 + duration2}ms')


if __name__ == '__main__':
    test_compress()

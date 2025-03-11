"""
"""
import os.path
import shutil
import time

import subprocess

from pyutils import byte2string


def compress_image(src_path, dst_path):
    result = subprocess.run(
        ['zopflipng', '--iterations=15', '--splitting=3', '--filters=01234mepb', src_path, dst_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode == 0:
        print(f"{src_path} 优化成功并保存为 {dst_path}")
    else:
        print(f"{src_path} 优化失败")


def test_compress():
    path = shutil.which('zopflipng')
    print(f'zopflipng = {path}')
    path1 = '/Users/zhouzhenliang/Desktop/py-tools/bg.png'
    name1, name2 = os.path.splitext(path1)
    path2 = f'{name1}_zopflipng{name2}'
    stat_time = time.time()
    compress_image(path1, path2)
    size1 = byte2string(os.path.getsize(path1))
    size2 = byte2string(os.path.getsize(path2))
    duration = round((time.time() - stat_time) * 1000)
    print(f'{size1} -> {size2}, {duration}ms')


if __name__ == '__main__':
    test_compress()

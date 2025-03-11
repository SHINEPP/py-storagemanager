import os
import time

import tinify

from pyutils import byte2string


def compress_image(src_path, des_path):
    tinify.key = "R06Khz9NqK8Y3GMbv7HN4qZPjGwTy3qQ"
    source = tinify.from_file(src_path)
    source.to_file(des_path)


def test_compress():
    path1 = '/Users/zhouzhenliang/Desktop/py-tools/bg.png'
    name1, name2 = os.path.splitext(path1)
    path2 = f'{name1}_tinify{name2}'
    stat_time = time.time()
    compress_image(path1, path2)
    size1 = byte2string(os.path.getsize(path1))
    size2 = byte2string(os.path.getsize(path2))
    duration = round((time.time() - stat_time) * 1000)
    print(f'{size1} -> {size2}, {duration}ms')


if __name__ == '__main__':
    test_compress()

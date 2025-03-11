import os
import time

from pyutils import byte2string
from pydub import AudioSegment


def compress_audio(src_path: str, dst_path: str):
    audio = AudioSegment.from_file(src_path)
    audio.export(dst_path, format='mp3', bitrate='128k')


def test_compress():
    path1 = '/Users/zhouzhenliang/Desktop/py-tools/bg.wav'
    name1, name2 = os.path.splitext(path1)
    path2 = f'{name1}_pydub{name2}'
    stat_time = time.time()
    compress_audio(path1, path2)
    size1 = os.path.getsize(path1)
    size2 = os.path.getsize(path2)
    size1_txt = byte2string(size1)
    size2_txt = byte2string(size2)
    duration = round((time.time() - stat_time) * 1000)
    print(f'{size1_txt} -> {size2_txt}, {round(size2 / size1 * 100, 1)}%, {duration}ms')


def use_compress_1():
    dir_path = os.path.expanduser('~/source/google-game/temp/app-wordcross/app/src/main/res/raw')
    names = os.listdir(dir_path)
    for name in names:
        if not name.endswith('.wav'):
            continue
        path1 = os.path.join(dir_path, name)
        name1, name2 = os.path.splitext(path1)
        path2 = f'{name1}.mp3'
        compress_audio(path1, path2)


if __name__ == '__main__':
    # test_compress()
    use_compress_1()

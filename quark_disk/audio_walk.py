import os


def walk_audio(audio_root: str):
    count = 0
    for root_dir, dirs, files in os.walk(audio_root):
        for file in files:
            count += 1
            print(f'{count} {file}')


if __name__ == '__main__':
    walk_audio('/Volumes/WDDATA4T/quark_disk/经典音乐小合集【766GB】')

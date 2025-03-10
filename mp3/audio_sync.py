import os
import shutil

if __name__ == '__main__':
    src_path = '/Volumes/WDDATA4T/audio'
    for root, dirs, names in os.walk(src_path):
        for name in names:
            path = os.path.join(root, name)
            if not path.endswith('.mp3'):
                continue
            dst_path = path.replace('/Volumes/WDDATA4T/audio', '/Volumes/US100/audio')
            if os.path.exists(dst_path):
                continue
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copyfile(path, dst_path)
            print(dst_path)

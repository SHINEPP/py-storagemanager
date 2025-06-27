import os


def get_file_magic_number(file_path, num_bytes=4):
    with open(file_path, 'rb') as f:
        magic = f.read(num_bytes)
    return magic.hex().upper()


if __name__ == '__main__':
    root_dir = '/Users/zhouzhenliang/Desktop/apk/deepsafebrowser/deepsafebrowser-vc4-v1.2.0-release'
    for root, dirs, paths in os.walk(root_dir):
        for path in paths:
            if path.endswith('.so'):
                file_path = os.path.join(root, path)
                magic_number = get_file_magic_number(file_path)
                print(f'{file_path} -> {magic_number}')

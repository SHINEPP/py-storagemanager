import os

if __name__ == '__main__':
    src_path = '/Volumes/US100/audio'
    count = 0
    for root, dirs, names in os.walk(src_path):
        for name in names:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                count += 1
                print(f'{count}: {path}')

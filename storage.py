import hashlib
import os


class Storage:

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def travel(self):
        self.travel_dir(self.root_dir, 0)

    def travel_dir(self, cur_dir: str, deep: int):
        if deep >= 5:
            return
        files = os.listdir(cur_dir)
        for file in files:
            path = os.path.join(cur_dir, file)
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    sha1 = hashlib.sha1(f.read()).hexdigest()
                    print(f'{path} -> {sha1}')
            elif os.path.isdir(path):
                self.travel_dir(path, deep + 1)


if __name__ == '__main__':
    storage = Storage('/Volumes/WDDATA/shine/.zhou_20240909')
    storage.travel()

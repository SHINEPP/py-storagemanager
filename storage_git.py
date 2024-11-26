import os.path


class StorageGit:

    @staticmethod
    def is_storage_git(root_dir: str) -> bool:
        git_dir = os.path.join(root_dir, '.git')
        return os.path.exists(git_dir) and os.path.isdir(git_dir)

    def __init__(self, root_dir):
        self.root_dir = root_dir


if __name__ == '__main__':
    test_dir = '/Volumes/WDDATA/shine/.zhou_20240909/source/git/lib-buildingblock'
    is_git = StorageGit.is_storage_git(test_dir)
    StorageGit(test_dir)

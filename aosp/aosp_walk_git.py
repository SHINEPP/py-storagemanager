import os

import git


def walk_git(root_dir, index=0):
    if index >= 5:
        return
    if not os.path.isdir(root_dir):
        return
    git_dir = os.path.join(root_dir, '.git')
    if os.path.exists(git_dir):
        yield root_dir
        return

    paths = os.listdir(root_dir)
    for name in paths:
        yield from walk_git(os.path.join(root_dir, name), index + 1)


def walk_gits():
    aosp_root_dir = '/Volumes/WDDATA/android/aosp/android-repo'
    index = 0
    for proj_path in walk_git(aosp_root_dir):
        path = proj_path[len(aosp_root_dir):].strip(os.path.sep)
        repo = git.Repo(proj_path)
        commit = repo.head.commit
        tags = [tag.name for tag in repo.tags if tag.commit == commit]
        name = ', '.join(tags)
        print(f'index: {index}, path: {path}, name: {name}')
        index += 1


if __name__ == '__main__':
    walk_gits()

import os


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
    aosp_root_dir = '/Volumes/WDDATA/android/aosp/android-13.0.0_r60'
    index = 0
    for proj_path in walk_git(aosp_root_dir):
        path = proj_path[len(aosp_root_dir):].strip(os.path.sep)
        print(f'index: {index}, path: {path}')
        index += 1


if __name__ == '__main__':
    walk_gits()

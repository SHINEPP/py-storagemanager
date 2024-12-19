import os
import shutil


def walk_gradle_build(root_dir, deep):
    if deep > 5 or not os.path.isdir(root_dir):
        return

    gradle = os.path.join(root_dir, 'build.gradle')
    gradle_kt = os.path.join(root_dir, 'build.gradle.kts')
    is_build = False
    if os.path.exists(gradle) or os.path.exists(gradle_kt):
        build_dir = os.path.join(root_dir, 'build')
        if os.path.exists(build_dir):
            is_build = True
            yield build_dir

    paths = os.listdir(root_dir)
    for name in paths:
        if is_build and name == 'build':
            continue
        yield from walk_gradle_build(os.path.join(root_dir, name), deep + 1)


def walk_gradle_gradle(root_dir, deep):
    if deep > 5 or not os.path.isdir(root_dir):
        return

    gradle = os.path.join(root_dir, 'build.gradle')
    gradle_kt = os.path.join(root_dir, 'build.gradle.kts')
    if os.path.exists(gradle) or os.path.exists(gradle_kt):
        gradle_dir = os.path.join(root_dir, '.gradle')
        if os.path.exists(gradle_dir):
            yield gradle_dir
            return

    paths = os.listdir(root_dir)
    for name in paths:
        yield from walk_gradle_gradle(os.path.join(root_dir, name), deep + 1)


if __name__ == '__main__':
    source_dirs = [
        '/Volumes/WDDATA/shine/.zhou_20221221/source',
        '/Volumes/WDDATA/shine/.zhou_20230314/source',
        '/Volumes/WDDATA/shine/.zhou_20230630/source',
        '/Volumes/WDDATA/shine/.zhou_20230925/source',
        '/Volumes/WDDATA/shine/.zhou_20240429/source',
        '/Volumes/WDDATA/shine/.zhou_20240909/source',
        '/Volumes/WDDATA/shine/.zhou_20241216/source']
    for source_dir in source_dirs:
        for build in walk_gradle_build(source_dir, 0):
            print(build)
            shutil.rmtree(build)
        for build in walk_gradle_gradle(source_dir, 0):
            print(build)
            shutil.rmtree(build)

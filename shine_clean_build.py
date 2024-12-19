import os


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


if __name__ == '__main__':
    source_dir = '/Users/zhouzhenliang/source'
    for build in walk_gradle_build(source_dir, 0):
        print(build)

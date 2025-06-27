import os
import subprocess


def walk_gradlew(root_dir, deep):
    if deep > 5 or not os.path.isdir(root_dir):
        return

    gradlew = os.path.join(root_dir, 'gradlew')
    if os.path.exists(gradlew):
        yield root_dir
        return

    paths = os.listdir(root_dir)
    for name in paths:
        yield from walk_gradlew(os.path.join(root_dir, name), deep + 1)


def run_command(command, cwd):
    result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


if __name__ == '__main__':
    source_dirs = [
        '/Users/zhouzhenliang/source/google1',
    ]
    for source_dir in source_dirs:
        for gradlew_dir in walk_gradlew(source_dir, 0):
            print(gradlew_dir)
            print(run_command("./gradlew clean", gradlew_dir))
            print()
            print()
            print()

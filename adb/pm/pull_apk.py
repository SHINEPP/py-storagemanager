import os
import subprocess
import sys


# 执行 adb 命令并获取输出
def run_adb_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def pm_list_packages():
    packages = []
    content = run_adb_command('adb shell pm list packages')
    lines = content.splitlines()
    for line in lines:
        if line.startswith('package:'):
            packages.append(line[len('package:'):].strip())
    return packages


def pm_dump_package(package_name: str):
    content = run_adb_command(f'adb shell pm dump {package_name}')
    if 'android.accounts.AccountAuthenticator' in content:
        print(f'\r{package_name} -> android.accounts.AccountAuthenticator', file=sys.stderr)


def pm_path_package(package_name: str):
    paths = []
    content = run_adb_command(f'adb shell pm path {package_name}')
    lines = content.splitlines()
    for line in lines:
        if line.startswith('package:'):
            paths.append(line[len('package:'):].strip())
    return paths


def pull_file(src_path, dst_path):
    run_adb_command(f'adb pull {src_path} {dst_path}')


def main_find_account():
    names = pm_list_packages()
    total_count = len(names)
    for i in range(total_count):
        name = names[i]
        print(f'\r{i + 1}/{total_count} dump {name}', end='')
        pm_dump_package(name)
    print('\rfinished')


def pull_package_apks(package_name: str):
    os.makedirs(dst_path, exist_ok=True)
    paths = pm_path_package(package_name)
    for path in paths:
        print(path)
        pull_file(path, dst_path)


if __name__ == '__main__':
    dst_path = '/Users/zhouzhenliang/Desktop/Desktop/apk/ShieldClean'
    pull_package_apks('com.shield.roc.cleaner')

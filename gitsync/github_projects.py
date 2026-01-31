import json
import os.path
import sys
import time

import git
import requests

from gitsync.base import source_dir


def fetch_repositories():
    with open('github_access.json', 'r') as file:
        data = json.loads(file.read())
        github_host = data['host']
        access_token = data['token']
        username = data['username']
    api_url = f'https://api.{github_host}/users/{username}/repos'
    print(api_url)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}, Message: {response.text}', file=sys.stderr)
        return []


class Progress(git.RemoteProgress):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def update(self, op_code, cur_count, max_count=None, message=''):
        percent = 0 if max_count is None else round((cur_count / max_count) * 100)
        print(f'{self.message} {percent}%', end='')


def run():
    github_root = source_dir + 'github-zzl'
    repositories = fetch_repositories()
    count = len(repositories)
    print(f'Total count: {count}')

    skip_count = 0
    c_success_count = 0
    c_fail_count = 0
    f_success_count = 0
    f_fail_count = 0
    index = -1

    def progress():
        return f'{round(100 * (index + 1) / count)}% ({index + 1}/{count})'

    def duration(start_time):
        return f'done in {round(time.time() - start_time, 1)}s'

    for repository in repositories:
        index += 1
        path = repository['name']
        if path == 'SHINEPP':
            print(f'\rCheck out: {progress()} skip {path}')
            continue
        clone_url = repository['clone_url']
        local_git = os.path.join(github_root, path)

        if os.path.exists(local_git):
            repo = None
            stime = time.time()
            try:
                msg = f'\rCheck out: {progress()} fetch {path}'
                print(msg, end='')
                repo = git.Repo(local_git)
                repo.remote().fetch(progress=Progress(msg))
                print(f'\rCheck out: {progress()} fetch {path} success, {duration(stime)}')
                f_success_count += 1
            except Exception as e:
                print(f'\rCheck out: {progress()} fetch {path} fail, {duration(stime)}', file=sys.stderr)
                print(f'e = {e}')
                f_fail_count += 1
            finally:
                repo.close()
        else:
            stime = time.time()
            try:
                msg = f'\rCheck out: {progress()} clone {path}'
                print(msg, end='')

                def callback(op_code, cur_count, max_count=None, message=''):
                    percent = 0 if max_count is None else round((cur_count / max_count) * 100)
                    print(f'{msg} {percent}%', end='')

                git.Repo.clone_from(clone_url, local_git, progress=callback)
                print(f'\rCheck out: {progress()} clone {path} success, {duration(stime)}')
                c_success_count += 1
            except Exception as e:
                print(f'\rCheck out: {progress()} clone {path} fail, {duration(stime)}', file=sys.stderr)
                print(f'e = {e}')
                c_fail_count += 1

    print(f'Check out: total skip {skip_count}')
    print(f'Check out: total clone ({c_success_count}/{c_fail_count + c_success_count})')
    print(f'Check out: total fetch ({f_success_count}/{f_fail_count + f_success_count})')


if __name__ == '__main__':
    run()

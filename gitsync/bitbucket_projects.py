import json
import os
import sys
import time

import git
import requests


def fetch_repositories():
    with open('bitbucket_access.json', 'r') as file:
        data = json.loads(file.read())
        username = data['username']
        password = data['password']

    repositories = []
    workspaces = ['zhouzhenliang', 'permanent-workspace']
    for workspace in workspaces:
        api_url = f'https://api.bitbucket.org/2.0/repositories/{workspace}'
        print(api_url)

        while True:
            response = requests.get(api_url, auth=(username, password))
            if response.status_code == 200:
                result = response.json()
                repositories.extend(result['values'])
                if 'next' in result.keys() and result['next']:
                    api_url = result['next']
                else:
                    break
            else:
                print(f'Error: {response.status_code}, Message: {response.text}')
                break
    return repositories


def run():
    github_root = '/Volumes/WDDATA4T/git/bitbucket'
    repositories = fetch_repositories()
    count = len(repositories)
    print(f'Total count: {count}')

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
        path = repository['full_name']
        clone_url = ''
        for clone_info in repository['links']['clone']:
            if clone_info['name'] == 'ssh':
                clone_url = clone_info['href']
        if len(clone_url) == 0:
            continue

        local_git = os.path.join(github_root, path)

        if os.path.exists(local_git):
            repo = None
            stime = time.time()
            try:
                print(f'\rCheck out: {progress()} fetch {path}', end='')
                repo = git.Repo(local_git)
                repo.remote().pull()
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

    print(f'Check out: total clone ({c_success_count}/{c_fail_count + c_success_count})')
    print(f'Check out: total fetch ({f_success_count}/{f_fail_count + f_success_count})')


if __name__ == '__main__':
    run()

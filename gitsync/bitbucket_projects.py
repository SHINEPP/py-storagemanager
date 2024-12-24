import json
import logging
import os
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
    github_root = '/Volumes/WDDATA/git/bitbucket'
    repositories = fetch_repositories()
    print(f'count: {len(repositories)}')

    index = 0
    for repository in repositories:
        path = repository['full_name']
        clone_url = ''
        for clone_info in repository['links']['clone']:
            if clone_info['name'] == 'ssh':
                clone_url = clone_info['href']
        if len(clone_url) == 0:
            continue

        local_git = os.path.join(github_root, path)

        print('---------------------------------------')
        print(f'{index} {path}')
        if os.path.exists(local_git):
            print(f'exist')
            repo = None
            start_time = time.time()
            try:
                print('origin pull')
                repo = git.Repo(local_git)
                repo.remote().pull()
                print(f'origin pull success, duration: {round(time.time() - start_time, 1)}s')
            except Exception as e:
                logging.error(f'origin pull fail, duration: {round(time.time() - start_time, 1)}s, e = {e}')
            finally:
                repo.close()
        else:
            print(f'clone')
            start_time = time.time()
            try:
                git.Repo.clone_from(clone_url, local_git)
                print(f'clone success, duration: {round(time.time() - start_time, 1)}s')
            except Exception as e:
                logging.error(f'clone fail, duration: {round(time.time() - start_time, 1)}s, e = {e}')
        print('---------------------------------------')
        index += 1


if __name__ == '__main__':
    run()

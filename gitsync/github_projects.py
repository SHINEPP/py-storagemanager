import json
import logging
import os.path

import git
import requests


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
        print(f'Error: {response.status_code}, Message: {response.text}')
        return []


def run():
    github_root = '/Volumes/WDDATA/git/github-zzl'
    repositories = fetch_repositories()
    print(f'count: {len(repositories)}')

    index = 0
    for repository in repositories:
        path = repository['name']
        if path == 'SHINEPP':
            continue
        clone_url = repository['clone_url']
        local_git = os.path.join(github_root, path)

        print('---------------------------------------')
        print(f'{index} {path}')
        if os.path.exists(local_git):
            print(f'exist')
            repo = None
            try:
                print('origin pull')
                repo = git.Repo(local_git)
                repo.remote().pull()
                print(f'origin pull success')
            except Exception as e:
                logging.error(f'origin pull fail, e = {e}')
            finally:
                repo.close()
        else:
            print(f'clone')
            try:
                git.Repo.clone_from(clone_url, local_git)
                print(f'clone success')
            except Exception as e:
                logging.error(f'clone fail, e = {e}')
        print('---------------------------------------')
        index += 1


if __name__ == '__main__':
    run()

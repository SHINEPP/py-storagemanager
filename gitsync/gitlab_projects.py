import json
import logging
import os.path
import sys
import time

import git
import requests


def fetch_projects():
    query = '''
    query($cursor: String) {
      projects(first: 100, after: $cursor) {
        nodes {
          id
          name
          fullPath
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    '''

    with open('gitlab_access.json', 'r') as file:
        data = json.loads(file.read())
        gitlab_url = 'https://' + data['host']
        access_token = data['token']

    url = f'{gitlab_url}/api/graphql'
    headers = {'Authorization': f'Bearer {access_token}'}

    projects = []

    cursor = None
    while True:
        variables = {'cursor': cursor}
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
        response.raise_for_status()
        result = response.json()
        print(f'response = {json.dumps(result)}')
        projects.extend(result['data']['projects']['nodes'])

        # next page
        page_info = result['data']['projects']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']

    return projects


def run():
    gitlab_root = '/Volumes/WDDATA4T/git/gitlab-ark'
    projects = fetch_projects()

    count = len(projects)
    print(f'total count: {count}')

    with open('gitlab_access.json', 'r') as file:
        data = json.loads(file.read())
        host = data['host']
        token = data['token']

    index = -1

    def progress():
        return f'{round(100 * (index + 1) / count)}% ({index + 1}/{count})'

    for project in projects:
        index += 1
        path = project['fullPath']
        repository_url = f'https://oauth2:{token}@{host}/{path}.git'
        local_git = os.path.join(gitlab_root, path)

        if os.path.exists(local_git):
            repo = None
            start_time = time.time()

            def duration():
                return f'done in {round(time.time() - start_time, 2)}s'

            try:
                print(f'\rCheck out: {progress()} fetch {path}', end='')
                repo = git.Repo(local_git)
                repo.remote().pull()
                print(f'\rCheck out: {progress()} fetch {path} success, {duration()}')
            except Exception as e:
                print(f'\rCheck out: {progress()} fetch {path} fail, {duration()}', file=sys.stderr)
                print(f'e = {e}')
            finally:
                repo.close()
        else:
            start_time = time.time()

            def duration():
                return f'done in {round(time.time() - start_time, 2)}s'

            try:
                print(f'\rCheck out: {progress()} clone {path}', end='')
                git.Repo.clone_from(repository_url, local_git)
                print(f'\rCheck out: {progress()} clone {path} success, {duration()}')
            except Exception as e:
                print(f'\rCheck out: {progress()} clone {path} fail, {duration()}s', file=sys.stderr)
                print(f'e = {e}')


if __name__ == '__main__':
    run()

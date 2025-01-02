import json
import logging
import os.path
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
    print(f'count: {len(projects)}')

    with open('gitlab_access.json', 'r') as file:
        data = json.loads(file.read())
        host = data['host']
        token = data['token']

    index = 0
    for project in projects:
        path = project['fullPath']
        repository_url = f'https://oauth2:{token}@{host}/{path}.git'
        local_git = os.path.join(gitlab_root, path)
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
                print(f'origin pull success, duration: {round(time.time() - start_time, 2)}s')
            except Exception as e:
                logging.error(f'origin pull fail, duration: {round(time.time() - start_time, 2)}s, e = {e}')
            finally:
                repo.close()
        else:
            start_time = time.time()
            print(f'clone')
            try:
                git.Repo.clone_from(repository_url, local_git)
                print(f'clone success, duration: {round(time.time() - start_time, 2)}s')
            except Exception as e:
                logging.error(f'clone fail, duration: {round(time.time() - start_time, 2)}s, e = {e}')
        print('---------------------------------------')
        index += 1


if __name__ == '__main__':
    run()

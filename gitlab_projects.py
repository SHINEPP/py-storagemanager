import json

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
        gitlab_url = data['host']
        access_token = data['token']

    url = f'{gitlab_url}/api/graphql'
    headers = {'Authorization': f'Bearer {access_token}'}

    cursor = None
    while True:
        variables = {'cursor': cursor}
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
        response.raise_for_status()
        result = response.json()
        print(f'response = {json.dumps(result)}')

        page_info = result['data']['projects']['pageInfo']
        if not page_info['hasNextPage']:
            break
        cursor = page_info['endCursor']


if __name__ == '__main__':
    fetch_projects()

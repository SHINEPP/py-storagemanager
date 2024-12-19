import json

import requests


def fetch_projects():
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
        repositories = response.json()
        for repository in repositories:
            print(f'{repository}')
    else:
        print(f'Error: {response.status_code}, Message: {response.text}')


def run():
    fetch_projects()


if __name__ == '__main__':
    run()

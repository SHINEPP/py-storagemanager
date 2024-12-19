import os
import re
import shutil

import git


def walk_git(root_dir):
    if not os.path.isdir(root_dir):
        return
    git_dir = os.path.join(root_dir, '.git')
    if os.path.exists(git_dir):
        yield root_dir
        return

    paths = os.listdir(root_dir)
    for name in paths:
        yield from walk_git(os.path.join(root_dir, name))


def parser_git_ssh(ssh):
    pattern = r'^git@([a-zA-Z0-9._-]+):([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+).git$'
    match = re.match(pattern, ssh)
    if match:
        groups = match.groups()
        host = groups[0]
        user = groups[1]
        path = groups[2]
        return host, user, path
    return None


def parser_git_http(url):
    pattern = r'^https://([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+).git$'
    match = re.match(pattern, url)
    if match:
        groups = match.groups()
        host = groups[0]
        user = groups[1]
        path = groups[2]
        return host, user, path
    return None


def git_url_format(git_dir):
    repo = git.Repo(git_dir)
    url = repo.remote().url

    infos = parser_git_http(url)
    if not infos:
        infos = parser_git_ssh(url)
    if infos:
        host, user, path = infos
        return f'{host}/{user}/{path}'
    return None


def walk_common_github():
    url_format_list = []
    github_dir = '/Volumes/WDDATA/git/github'
    for proj_path in walk_git(github_dir):
        proj_name = proj_path[len(github_dir):].strip(os.path.sep)
        repo = git.Repo(proj_path)
        url = repo.remote().url
        print(f'path: {proj_name}, url: {url}')

        infos = parser_git_http(url)
        if not infos:
            infos = parser_git_ssh(url)
        if infos:
            host, user, path = infos
            url_format_list.append(f'{host}/{user}/{path}')

        try:
            repo.remotes['origin'].pull()
        except git.GitCommandError as e:
            print(f'e = {e}')

    # root_dirs = ['/Users/zhouzhenliang']
    #
    # for root_dir in root_dirs:
    #     print(f'------------------ {root_dir} ------------------')
    #     git_dir = os.path.join(root_dir, 'source', 'github')
    #     for proj_path in walk_git(git_dir):
    #         url_format = git_url_format(proj_path)
    #         if url_format:
    #             print(url_format)
    #             if url_format not in url_format_list:
    #                 dst_dir = os.path.join(github_dir, proj_path[len(git_dir):].strip(os.path.sep))
    #                 print(f'copy to {dst_dir}')
    #                 if not os.path.exists(dst_dir):
    #                     shutil.copytree(proj_path, dst_dir)
    #                     if os.path.exists(dst_dir):
    #                         print(f'copy success')
    #                 else:
    #                     print(f'copy fail, exist: {dst_dir}')
    #             print()
    #     print(f'------------------ {root_dir} ------------------')


if __name__ == '__main__':
    walk_common_github()

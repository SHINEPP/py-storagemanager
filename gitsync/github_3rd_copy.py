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


def sync_3rd_github():
    github_dir = '/Volumes/WDDATA4T/git/github'
    dst_dir = '/Volumes/US100/git/github'
    index = 0
    for proj_path in walk_git(github_dir):
        print('---------------------------------------')
        proj_name = proj_path[len(github_dir):].strip(os.path.sep)
        repo = git.Repo(proj_path)
        url = repo.remote().url
        print(f'index: {index}, path: {proj_name}, url: {url}')

        match = re.search(r'[:/](.+?)/([^/]+).git$', url)
        group = match.group(1).split('/')[-1]
        project = match.group(2)

        print(f'group: {group}, project: {project}')

        project_dir = os.path.join(dst_dir, group, project)

        if not os.path.exists(project_dir):
            print(f'out project_dir: {project_dir}, copy')
            shutil.copytree(proj_path, project_dir, symlinks=True)
        else:
            print(f'out project_dir: {project_dir}, skip')

        repo.close()
        print('---------------------------------------')
        index += 1


if __name__ == '__main__':
    sync_3rd_github()

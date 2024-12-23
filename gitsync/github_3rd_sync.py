import os

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
    github_dir = '/Volumes/WDDATA/git/github'
    for proj_path in walk_git(github_dir):
        proj_name = proj_path[len(github_dir):].strip(os.path.sep)
        repo = git.Repo(proj_path)
        url = repo.remote().url
        print(f'path: {proj_name}, url: {url}')

        try:
            repo.remotes['origin'].pull()
            print(f'origin pull success')
        except git.GitCommandError as e:
            print(f'origin pull fail, e = {e}')


if __name__ == '__main__':
    sync_3rd_github()

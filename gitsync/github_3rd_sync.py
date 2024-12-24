import logging
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
    index = 0
    for proj_path in walk_git(github_dir):
        print('---------------------------------------')
        proj_name = proj_path[len(github_dir):].strip(os.path.sep)
        repo = git.Repo(proj_path)
        url = repo.remote().url
        print(f'index: {index}, path: {proj_name}, url: {url}')
        try:
            repo.remote().pull()
            print(f'origin pull success')
        except git.GitCommandError as e:
            logging.error(f'origin pull fail, e = {e}')
        finally:
            repo.close()
        print('---------------------------------------')
        index += 1


if __name__ == '__main__':
    sync_3rd_github()

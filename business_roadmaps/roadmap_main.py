import math
import time

import git
import sys

master_branches = ('master', 'develop')
app_branches = ('release',)


class ReleaseNode:

    def __init__(self, app: git.Head, master: git.Head, base: git.Commit):
        self.app = app
        self.app_commited_date = app.commit.committed_date
        self.app_commited_datetime = app.commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        self.master = master
        self.base = base
        self.base_commited_date = base.committed_date
        self.base_commited_datetime = base.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')


class BusinessGit:
    def __init__(self, git_dir):
        self.repo = git.Repo(git_dir)
        self.master_heads = []
        self.app_heads = []
        self.master_max_len = 0
        for head in self.repo.heads:
            for master_branch in master_branches:
                if head.name.startswith(master_branch):
                    self.master_heads.append(head)
                    size = len(head.name)
                    if size > self.master_max_len:
                        self.master_max_len = size
                    break
            for app_branch in app_branches:
                if head.name.startswith(app_branch):
                    self.app_heads.append(head)
                    break

    def start(self):
        nodes = []
        app_head_count = len(self.app_heads)
        for i in range(app_head_count):
            app_head = self.app_heads[i]
            app_head_text = f'\r[{i + 1}/{app_head_count}] {app_head.name}'
            print(app_head_text + ' ' * 16, end='')
            master_head, base_commit, features = self._parent_master(app_head.commit.hexsha)
            if master_head and base_commit:
                nodes.append(ReleaseNode(app_head, master_head, base_commit))

        print('\r' + ' ' * 40)

        # 输出结果

        def handle_group_nodes(groups):
            count = len(groups)
            if count == 0:
                return
            for j in range(count):
                n = groups[j]
                base_time = node.base_commited_datetime
                master_name = n.master.name
                master_name = ' ' * (self.master_max_len - len(master_name)) + master_name
                sep = '+-------------->'
                if j == 0:
                    show_name = f'{base_time}	{master_name}'
                else:
                    show_name = f'{" " * len(base_time)}	{" " * len(master_name)}'
                print(f'{show_name}	{sep}	{n.app_commited_datetime}	{n.app.name}')
            groups.clear()
            print()

        group_nodes = []
        new_nodes = sorted(nodes, key=lambda p: -p.app_commited_date)
        for node in new_nodes:
            if len(group_nodes) > 0 and node.base.hexsha != group_nodes[0].base.hexsha:
                handle_group_nodes(group_nodes)
            group_nodes.append(node)
        handle_group_nodes(group_nodes)

    def _parent_master(self, commit: str):

        # 输出features
        features = []
        for head in self.repo.heads:
            commits = self.repo.merge_base(commit, head.commit)
            if commits and commits[0].hexsha == commit:
                distance = self._rev_list_count(commit, head.commit)
                if distance > 0:
                    features.append((distance, head.name))
        features = sorted(features, key=lambda x: x[0])

        # 计算最近的master*
        min_distance = math.inf
        min_distance2 = None
        min_head = None
        base_commit = None
        for base_head in self.master_heads:
            commits = self.repo.merge_base(commit, base_head.commit)
            if not commits or len(commits) == 0:
                continue
            distance1 = self._rev_list_count(commits[0], commit)
            distance2 = self._rev_list_count(commits[0], base_head.commit)
            if distance1 < min_distance or (distance1 == min_distance and distance2 <= min_distance2):
                min_distance = distance1
                min_head = base_head
                min_distance2 = distance2
                base_commit = commits[0]

        return min_head, base_commit, features

    def _rev_list_count(self, commit1, commit2):
        try:
            return int(self.repo.git.execute(['git', 'rev-list', '--count', f'{commit1}..{commit2}']))
        except RuntimeError as e:
            print(f'e = ${e}', file=sys.stderr)
            pass


if __name__ == '__main__':
    business = BusinessGit(sys.argv[1])
    business.start()

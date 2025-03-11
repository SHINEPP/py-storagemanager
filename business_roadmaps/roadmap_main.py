import math

import git
import sys

master_branches = ('master', 'develop')
app_branches = ('release',)


class Node:
    def __init__(self, name: str, commit: git.Commit):
        self.name = name
        self.commit = commit


class ReleaseNode:

    def __init__(self, app: Node, master: Node, base: git.Commit):
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
        self.master_nodes = []
        self.app_nodes = []
        self.master_max_len = 0

        all_heads = {}
        for remote in self.repo.remotes:
            for ref in remote.refs:
                all_heads[ref.remote_head] = ref.commit

        for head in self.repo.heads:
            all_heads[head.name] = head.commit

        self.nodes = [Node(v[0], v[1]) for v in all_heads.items()]

        for node in self.nodes:
            for master_branch in master_branches:
                if node.name.startswith(master_branch):
                    self.master_nodes.append(node)
                    size = len(node.name)
                    if size > self.master_max_len:
                        self.master_max_len = size
                    break
            for app_branch in app_branches:
                if node.name.startswith(app_branch):
                    self.app_nodes.append(node)
                    break

    def start(self):
        nodes = []
        app_head_count = len(self.app_nodes)
        for i in range(app_head_count):
            app_node = self.app_nodes[i]
            app_head_text = f'\r[{i + 1}/{app_head_count}] {app_node.name}'
            print(app_head_text + ' ' * 16, end='')
            master_node, base_commit, features = self._parent_master(app_node.commit.hexsha)
            if master_node and base_commit:
                nodes.append(ReleaseNode(app_node, master_node, base_commit))

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
        for base_head in self.master_nodes:
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

import math
import sys

import git


class BusinessGit:

    def __init__(self, git_dir):
        self.repo = git.Repo(git_dir)
        self.master_heads = []
        for head in self.repo.heads:
            if head.name.startswith('master'):
                self.master_heads.append(head)

    def parent_master(self, commit: str):
        # 判断commit还是branch
        is_in_branch = False
        for head in self.repo.heads:
            if head.name == commit:
                is_in_branch = True
                print(f'branch: {commit}')
                print(f'commit: {head.commit}')
                break

        if not is_in_branch:
            print(f'commit: {commit}')
            for head in self.repo.heads:
                if head.commit.hexsha == commit:
                    print(f'branch: {head.name}')

        # 输出features
        features = []
        for head in self.repo.heads:
            commits = self.repo.merge_base(commit, head.commit)
            if commits and commits[0].hexsha == commit:
                distance = self._rev_list_count(commit, head.commit)
                if distance > 0:
                    features.append((distance, head.name))
        features.sort()
        if len(features) > 0:
            features = sorted(features, key=lambda x: x[0])
            print()
            print('features:')
            for feature in features:
                print(f'[{feature[0]}]{feature[1]}')

        # 计算最近的master*
        min_distance = math.inf
        min_distance2 = None
        min_head = None
        for master_head in self.master_heads:
            if commit == master_head.name:
                continue
            commits = self.repo.merge_base(commit, master_head.commit)
            if not commits or len(commits) == 0:
                continue
            distance = self._rev_list_count(commits[0], commit)
            distance2 = self._rev_list_count(commits[0], master_head.commit)
            if distance < min_distance or (distance == min_distance and distance2 < min_distance2):
                min_distance = distance
                min_head = master_head
                min_distance2 = distance2

        # 输出结果
        print()
        print('source:')
        if min_head:
            print(f'name: {min_head.name}')
            print(f'commit: {min_head.commit}')
            print(f'distance: {min_distance}')
        else:
            print('not found')

    def _rev_list_count(self, commit1, commit2):
        try:
            return int(self.repo.git.execute(['git', 'rev-list', '--count', f'{commit1}..{commit2}']))
        except RuntimeError as e:
            pass


if __name__ == '__main__':
    business = BusinessGit(sys.argv[1])
    business.parent_master(sys.argv[2])

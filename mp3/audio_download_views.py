import os.path
import sys

from mp3.mysql_connection import open_mysql


class AudioViews:

    def __init__(self):
        self.root_dir = '/Volumes/US100/audio'
        self.view_dir = self.root_dir + '/views'
        self.repository = '/kumeiwp/repository'

    def start(self):
        os.makedirs(self.view_dir, exist_ok=True)
        os.chdir(self.view_dir)
        sql = 'SELECT name, local_path FROM audio_kumeiwp_detail_view WHERE download_times > %s'
        with open_mysql() as cursor:
            cursor.execute(sql, 0)
            count = 0
            for row in cursor:
                name = row[0]
                local_path = row[1]
                path = self.root_dir + self.repository + local_path
                if os.path.exists(path):
                    count += 1
                    print(f'{count}. {name}')
                    link = f'{self.view_dir}/{name}'
                    if os.path.exists(link):
                        print(f'{link} exist', file=sys.stderr)
                    else:
                        os.symlink(f'..{self.repository}{local_path}', name)


if __name__ == '__main__':
    impl = AudioViews()
    impl.start()

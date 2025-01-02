import os.path
import shutil
from datetime import datetime

if __name__ == '__main__':
    user_home = os.path.expanduser('~')
    root_dir = '/Volumes/WDDATA4T/shine_ark_backup'
    name = datetime.now().strftime('%Y-%m-%d')
    backup_dir = os.path.join(root_dir, name)
    os.makedirs(backup_dir, exist_ok=True)

    zshrc = os.path.join(user_home, '.zshrc')
    zshrc_dst = os.path.join(backup_dir, '.zshrc')
    shutil.copyfile(zshrc, zshrc_dst)

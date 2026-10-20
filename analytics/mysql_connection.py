import os

import paramiko
import pymysql

'''
代码内通过 paramiko 建立 SSH 通道直连 MySQL，无需再手动执行：
ssh -NL 3307:amv-rj9c24ap86lo3rfb800000116.ads.aliyuncs.com:3306 root@198.11.183.103
'''

SSH_HOST = '198.11.183.103'
SSH_PORT = 22
SSH_USER = 'root'
SSH_KEY_FILE = os.path.expanduser('~/.ssh/id_rsa')

MYSQL_HOST = 'amv-rj9c24ap86lo3rfb800000116.ads.aliyuncs.com'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '2Xga9BKGwk41Fd'


class AnalyticsConnection:
    def __init__(self):
        self._ssh: paramiko.SSHClient
        self._conn: pymysql.Connection
        self._cursor: pymysql.Connection.cursor

    def __enter__(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, key_filename=SSH_KEY_FILE)
        # 通过 SSH 打开到 MySQL 的 direct-tcpip 通道，作为 pymysql 的 socket 使用
        channel = self._ssh.get_transport().open_channel(
            'direct-tcpip', (MYSQL_HOST, MYSQL_PORT), ('127.0.0.1', 0)
        )
        self._conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database='',
            defer_connect=True
        )
        self._conn.connect(sock=channel)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self._cursor.close()
        self._conn.close()
        self._ssh.close()


def open_analytics() -> AnalyticsConnection:
    return AnalyticsConnection()


if __name__ == '__main__':
    with open_analytics() as cursor:
        cursor.execute('SELECT * FROM `macrophage_data_super_storage_cleaner`.raw_data LIMIT 10')
        names = []
        for desc in cursor.description:
            names.append(desc[0])
        print(','.join(names))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

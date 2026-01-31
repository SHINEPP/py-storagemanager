import pymysql

'''
ssh -NL 3307:amv-rj9c24ap86lo3rfb800000116.ads.aliyuncs.com:3306 root@198.11.183.103
'''


class AnalyticsConnection:
    def __init__(self):
        self._conn: pymysql.Connection
        self._cursor: pymysql.Connection.cursor

    def __enter__(self):
        self._conn = pymysql.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='2Xga9BKGwk41Fd',
            database=''
        )
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self._cursor.close()
        self._conn.close()


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

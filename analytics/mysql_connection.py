import pymysql


class AnalyticsConnection:
    def __init__(self):
        self.conn: pymysql.Connection
        self.cursor: pymysql.Connection.cursor

    def __enter__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='2Xga9BKGwk41Fd',
            database=''
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()


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

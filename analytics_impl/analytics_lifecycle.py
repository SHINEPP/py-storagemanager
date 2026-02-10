from analytics import open_analytics


class User:

    def __init__(self, uuid: str):
        self.uuid = uuid
        self.life_time = 0
        self.death_time = 0
        self.last_time = 0


def start():
    app_name = 'device_file_engine'
    app_version = '6'
    start_date = '2026-01-31'
    end_data = '2026-01-31'
    os_version = ''

    sql_where = []
    sql_where.append(f"json_extract(event_parameters, '$.app_version') = '{app_version}'")
    sql_where.append(f"event_date_utc >= '{start_date}' AND event_date_utc <= '{end_data}'")
    if len(os_version) > 0:
        sql_where.append(f"json_extract(event_parameters, '$.os_version')  = '{os_version}'")
    where = ' AND '.join(sql_where)

    sql = f'''
SELECT uuid, event_timestamp
FROM `macrophage_data_{app_name}`.raw_data
WHERE {where}
ORDER BY event_timestamp ASC
    '''.strip() + ';'

    users = []

    def find_user(uuid_t: str) -> User | None:
        for user_t in users:
            if user_t.uuid == uuid_t:
                return user_t
        return None

    print(sql)
    with open_analytics() as cursor:
        cursor.execute(sql)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            uuid = row[0]
            event_timestamp: int = row[1].now()
            user = find_user(uuid)
            print(f'{uuid} -> {event_timestamp}')
            if user is None:
                user = User(uuid)
                users.append(user)
                continue

            duration = event_timestamp - user.last_time
            if duration < 60:
                user.life_time += duration
            else:
                user.death_time += duration
            user.last_time = event_timestamp

    print(f'uuid,life_time,death_time')
    for user in users:
        print(f'{user.uuid},{user.life_time}s,{user.death_time}s')


if __name__ == '__main__':
    start()

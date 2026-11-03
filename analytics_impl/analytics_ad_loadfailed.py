import csv
import os.path
import textwrap
from datetime import datetime, timezone

import pytz

from analytics import open_analytics


def business_events(app_name: str,
                    app_version: str,
                    start_date: datetime,
                    end_date: datetime,
                    output: str,
                    security_path: bool = False,
                    zone: int = 0):
    start_date_s = start_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    end_date_s = end_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # select
    sql_select = []
    csv_header = []

    def append_attribute(sql_v, csv_v):
        sql_select.append(sql_v)
        csv_header.append(csv_v)

    event_date = 'event_date'
    zone_str = '+' + str(zone).zfill(2) + ':00'
    append_attribute(f"DATE(CONVERT_TZ(event_timestamp, '+00:00', '{zone_str}')) AS {event_date}",
                     event_date)
    append_attribute(
        "json_unquote(json_unquote(json_extract(event_parameters, '$.error'))) as ad_error",
        'ad_error')
    if security_path:
        append_attribute(
            "json_unquote(json_unquote(json_extract(event_parameters, '$.security_patch'))) as security_patch",
            'security_patch')
    append_attribute('count(distinct user_id) as user_count', 'user_count')
    append_attribute('count(*) as event_count', 'event_count')
    join_selects = ','.join(sql_select)

    # where
    sql_where = []
    sql_where.append(f"event_name = 'business_interstitialad_loadfailed'")
    sql_where.append(f"json_extract(event_parameters,'$.app_version')  = '{app_version}'")
    sql_where.append(f"event_timestamp >= '{start_date_s}' AND event_timestamp < '{end_date_s}'")
    where = ' AND '.join(sql_where)

    # group
    sql_group = []
    sql_group.append(event_date)
    if security_path:
        sql_group.append('security_patch')
    sql_group.append('ad_error')
    join_groups = ','.join(sql_group)

    # order
    sql_order = []
    sql_order.append(event_date)
    if security_path:
        sql_order.append('security_patch')
    join_orders = ','.join(sql_order)

    sql = textwrap.dedent(f'''
    SELECT {join_selects}
    FROM `macrophage_data_{app_name}`.raw_data
    WHERE {where}
    GROUP BY {join_groups}
    ORDER BY {join_orders} DESC
    LIMIT 0, 5000
    ''').strip() + ';'

    print(sql)

    with open_analytics() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        csv_file = open(output, 'w')
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(csv_header + ['per_user_event_count'])

        for row in rows:
            csv_writer.writerow(list(row) + [round(row[-1] / row[-2], 1)])
        csv_file.close()


def main():
    app_name = 'stealth_browser_2'
    app_version = '8'
    start_day = '2026-11-02'
    end_day = '2026-11-03'
    security_path = False
    zone = 0
    output_dir = '/Users/zhouzhenliang/Desktop/Desktop/temp-analytics'

    date_text = datetime.now().strftime('%m%d%H%M%S')
    output = os.path.join(output_dir, f'{app_name}_ad_loadfailed_{app_version}_{date_text}.csv')

    tz = pytz.FixedOffset(zone * 60)
    start_date = tz.localize(datetime.strptime(start_day, '%Y-%m-%d'))
    end_data = tz.localize(datetime.strptime(end_day, '%Y-%m-%d'))

    business_events(app_name, app_version, start_date, end_data, output, security_path=security_path, zone=zone)


if __name__ == '__main__':
    main()

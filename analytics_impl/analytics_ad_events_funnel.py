import csv
import textwrap
from datetime import datetime

from analytics import open_analytics


def business_events(app_name: str, app_version: str, start_date: str, end_date: str, output: str,
                    security_path: bool = False):
    events = [
        'business_startworker',
        'business_dowork',
        'business_dowork_limit',
        'business_adactivity_chance',
        'business_adactivity_viewed',
        'business_hostactivity_viewed',
        'business_hostactivity_viewed_loadorshow',
        'business_hostactivity_viewed_justshow',
        'business_hostactivity_postresume_loadorshow',
        'business_hostactivity_postresume_justshow',
        'business_interstitialad_loadfailed',
        'business_interstitialad_loaded',
        'business_interstitialad_showad',
        'business_interstitialad_viewed',
        'business_interstitialad_revenue',
        'business_interstitialad_loadfailed',
        'business_interstitialad_clicked',
        'business_interstitialad_close',
        'business_interstitialad_displayfailed',
        'business_startactivity',
        'business_activityviewed']
    join_events = ','.join(map(lambda a: f"'{a}'", events))

    sql_select = []
    csv_header = []
    sql_select.append('event_date_utc')
    csv_header.append('event_date_utc')
    if security_path:
        sql_select.append(
            "json_unquote(json_unquote(json_extract(event_parameters, '$.security_patch'))) as security_patch")
        csv_header.append('security_patch')
    sql_select.append('event_name')
    csv_header.append('event_name')
    sql_select.append('count(distinct user_id) as user_count')
    csv_header.append('user_count')
    sql_select.append('count(*) as event_count')
    csv_header.append('event_count')
    join_selects = ','.join(sql_select)

    sql_where = []
    sql_where.append(f"event_name in ({join_events})")
    sql_where.append(f"json_extract(event_parameters,'$.app_version')  = '{app_version}'")
    sql_where.append(f"event_date_utc >= '{start_date}' AND event_date_utc <= '{end_date}'")
    where = ' AND '.join(sql_where)

    sql_group = []
    sql_group.append('event_date_utc')
    if security_path:
        sql_group.append('security_patch')
    sql_group.append('event_name')
    join_groups = ','.join(sql_group)

    sql_order = []
    sql_order.append('event_date_utc')
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
    app_name = 'chief_file_officer'
    app_version = '5'
    start_date = '2026-02-27'
    end_data = '2026-02-27'

    date_text = datetime.now().strftime('%m%d%H%M%S')
    output = f'/Users/zhouzhenliang/Desktop/Desktop/temp-analytics/{app_name}_events_funnel_{app_version}_{date_text}.csv'

    business_events(app_name, app_version, start_date, end_data, output, security_path=True)


if __name__ == '__main__':
    main()

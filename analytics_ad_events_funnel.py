import csv
from datetime import datetime

from analytics import open_analytics

if __name__ == '__main__':

    app_name = 'file_manager_center'
    app_version = '3'
    start_date = '2025-09-07'
    end_data = '2025-09-07'
    os_version = '35'

    events = [
        'business_dowork',
        'business_startloadactivity',
        'business_loadactivity_viewed',
        'business_interstitialad_startload',
        'business_adactivity_viewed',
        'business_interstitialad_loaded',
        'business_showinterstitialad',
        'business_interstitialad_viewed',
        'business_interstitialad_revenue',
        'business_dowork_limit',
        'business_interstitialad_loadtimeout',
        'business_interstitialad_loadfailed',
        'business_interstitialad_loadfailed_finish',
        'business_interstitialad_displayfailed',
        'business_startactivity',
        'business_activityviewed',
        'business_interstitialad_close']

    events_group = ','.join(map(lambda a: f"'{a}'", events))

    sql_where = []
    sql_where.append(f"event_name in ({events_group})")
    sql_where.append(f"json_extract(event_parameters, '$.app_version')  = '{app_version}'")
    sql_where.append(f"event_date_utc >= '{start_date}' AND event_date_utc <= '{end_data}'")
    if len(os_version) > 0:
        sql_where.append(f"json_extract(event_parameters, '$.os_version')  = '{os_version}'")
    where = ' AND '.join(sql_where)

    sql = f'''
SELECT event_date_utc, event_name, count(distinct user_id) as user_count, count(*) as event_count
FROM `macrophage_data_{app_name}`.raw_data
WHERE {where}
GROUP BY event_date_utc, event_name
ORDER BY event_date_utc DESC
LIMIT 0, 2000
    '''.strip() + ';'

    with open_analytics() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        date_text = datetime.now().strftime('%m%d%H%M%S')
        out_path = f'/Users/zhouzhenliang/Desktop/Desktop/temp-analytics/{app_name}_events_funnel_{app_version}_{date_text}.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        headers = ['event_date_utc', 'component', 'user_count', 'event_count', 'per_user_event_count']
        csv_writer.writerow(headers)

        for row in rows:
            csv_writer.writerow([row[0], row[1], row[2], row[3], round(row[3] / row[2], 1)])
        csv_file.close()

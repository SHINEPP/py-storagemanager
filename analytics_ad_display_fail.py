import csv
from datetime import datetime

from analytics import open_analytics

if __name__ == '__main__':

    app_name = 'file_manager_champ'
    app_version = '4'
    start_date = '2025-09-14'
    end_data = '2025-09-14'

    sql = f'''
SELECT event_date_utc, json_extract(event_parameters, '$.network') as network, count(distinct user_id) as user_count, count(*) as event_count
FROM `macrophage_data_{app_name}`.raw_data
WHERE event_date_utc >= '{start_date}' AND event_date_utc <= '{end_data}'
AND json_extract(event_parameters, '$.app_version')  = '{app_version}'
AND event_name = 'business_interstitialad_displayfailed'
AND json_extract(event_parameters, '$.os_version') = '33'
GROUP BY network
ORDER BY event_date_utc DESC
LIMIT 0, 2000
    '''.strip() + ';'

    with open_analytics() as cursor:
        cursor.execute(sql)
        names = []
        for desc in cursor.description:
            names.append(desc[0])
        names.append('per_user_event_count')

        date_text = datetime.now().strftime('%m%d%H%M%S')
        out_path = f'/Users/zhouzhenliang/Desktop/Desktop/temp-analytics/{app_name}_ad_display_fail_{app_version}_{date_text}.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(names)

        rows = cursor.fetchall()
        for row in rows:
            csv_writer.writerow(list(row) + [round(row[-1] / row[-2], 1)])
        csv_file.close()

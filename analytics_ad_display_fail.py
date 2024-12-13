import csv
from datetime import datetime

from analytics import open_analytics

if __name__ == '__main__':

    sql = '''
SELECT event_date_utc, json_extract(event_parameters, '$.error') as error, count(distinct user_id) as user_count, count(*) as event_count
FROM `macrophage_data_super_storage_cleaner`.raw_data
WHERE event_date_utc >= '2024-12-10' AND event_date_utc <= '2024-12-13'
AND json_extract(event_parameters, '$.app_version')  = '7'
AND event_name = 'business_interstitialad_displayfailed'
GROUP BY event_date_utc, json_extract(event_parameters, '$.error')
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
        out_path = f'/Users/zhouzhenliang/Desktop/temp-analytics/superstoragecleaner_ad_display_fail_1.6_{date_text}.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(names)

        rows = cursor.fetchall()
        for row in rows:
            csv_writer.writerow(list(row) + [round(row[-1] / row[-2], 1)])
        csv_file.close()

import csv
from datetime import datetime

from analytics import open_analytics

if __name__ == '__main__':

    sql = '''
SELECT event_date_utc, event_name, count(distinct user_id) as user_count, count(*) as event_count
FROM `macrophage_data_super_storage_cleaner`.raw_data
WHERE event_name in ('business_dowork', 'business_startloadactivity', 'business_loadactivity_viewed', 'business_adactivity_viewed', 'business_showinterstitialad', 'business_interstitialad_viewed', 'business_interstitialad_revenue', 'business_dowork_limit', 'business_interstitialad_loadtimeout', 'business_interstitialad_loadfailed', 'business_interstitialad_displayfailed', 'business_startactivity', 'business_activityviewed') 
AND json_extract(event_parameters, '$.app_version')  = '7'
AND event_date_utc >= '2024-12-10' AND event_date_utc <= '2024-12-13'
GROUP BY event_date_utc, event_name
ORDER BY event_date_utc DESC
LIMIT 0, 2000
    '''.strip() + ';'

    with open_analytics() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        date_text = datetime.now().strftime('%m%d%H%M%S')
        out_path = f'/Users/zhouzhenliang/Desktop/temp-analytics/superstoragecleaner_events_funnel_1.6_{date_text}.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        headers = ['event_date_utc', 'component', 'user_count', 'event_count', 'unique_user_event_count']
        csv_writer.writerow(headers)

        for row in rows:
            csv_writer.writerow([row[0], row[1], row[2], row[3], round(row[3] / row[2], 1)])
        csv_file.close()
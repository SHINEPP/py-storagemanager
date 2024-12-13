import csv

import pandas as pd
from analytics import open_analytics

ad_activity_names = ['com.anythink.basead.ui.ATLandscapeActivity',
                     'com.mbridge.msdk.activity.MBCommonActivity',
                     'com.bytedance.sdk.openadsdk.activity.TTWebsiteActivity',
                     'com.mbridge.msdk.reward.player.MBRewardVideoActivity',
                     'com.anythink.core.basead.ui.web.WebLandPageActivity',
                     'com.bytedance.sdk.openadsdk.activity.TTFullScreenExpressVideoActivity',
                     'com.facebook.ads.AudienceNetworkActivity',
                     'com.bytedance.sdk.openadsdk.activity.TTFullScreenVideoActivity',
                     'com.inmobi.ads.rendering.InMobiAdActivity',
                     'sg.bigo.ads.api.AdActivity',
                     'com.vungle.ads.internal.ui.VungleActivity',
                     'com.bytedance.sdk.openadsdk.activity.TTLandingPageActivity',
                     'sg.bigo.ads.api.CompanionAdActivity',
                     'com.anythink.expressad.reward.player.ATRewardVideoActivity',
                     'com.anythink.basead.ui.ATPortraitActivity']

if __name__ == '__main__':

    sql1 = '''
SELECT event_date_utc, json_extract(event_parameters, '$.component') as component, count(*) as event_count
FROM `macrophage_data_super_storage_cleaner`.raw_data
WHERE event_name = 'business_startactivity' 
AND json_extract(event_parameters, '$.app_version')  = '7'
AND event_date_utc >= '2024-12-10' AND event_date_utc <= '2024-12-13'
GROUP BY event_date_utc, json_extract(event_parameters, '$.component')
ORDER BY event_date_utc DESC
LIMIT 0, 10000
    '''.strip() + ';'

    sql2 = '''
SELECT event_date_utc, json_extract(event_parameters, '$.component') as component, count(*) as event_count
FROM `macrophage_data_super_storage_cleaner`.raw_data
WHERE event_name = 'business_activityviewed' 
AND json_extract(event_parameters, '$.app_version')  = '7'
AND event_date_utc >= '2024-12-10' AND event_date_utc <= '2024-12-13'
GROUP BY event_date_utc, json_extract(event_parameters, '$.component')
ORDER BY event_date_utc DESC
LIMIT 0, 10000
    '''.strip() + ';'

    with open_analytics() as cursor:
        cursor.execute(sql1)
        rows1 = cursor.fetchall()
        cursor.execute(sql2)
        rows2 = cursor.fetchall()

        out_path = '/Users/zhouzhenliang/Desktop/temp/analytics-20241209/superstoragecleaner_activity_result_1.6-3.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        headers = ['event_date_utc', 'component', 'start_event_count', 'view_event_count']
        csv_writer.writerow(headers)

        for row1 in rows1:
            component = row1[1].strip('"')
            if component not in ad_activity_names:
                continue

            date = row1[0]
            event_count = row1[2]
            csv_rows = [date, component, event_count]

            find = False
            for row2 in rows2:
                if row2[0] == date and row2[1].strip('"') == component:
                    find = True
                    csv_rows.append(row2[2])
                    break
            if not find:
                csv_rows.append(0)

            csv_writer.writerow(csv_rows)

        csv_file.close()

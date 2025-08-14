import csv
from datetime import datetime
import pytz
from analytics import open_analytics

ad_activity_names = [
    'com.anythink.basead.ui.ATLandscapeActivity',
    'com.mbridge.msdk.activity.MBCommonActivity',
    'com.mbridge.msdk.reward.player.MBRewardVideoActivity',
    'com.bytedance.sdk.openadsdk.activity.TTWebsiteActivity',
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
    'com.anythink.basead.ui.ATPortraitActivity'
]

if __name__ == '__main__':

    app_name = 'device_file_radar'
    app_version = 10
    os_version = '36'
    dt = datetime(2025, 8, 3, 0, 0, 0)

    tz = pytz.timezone('Asia/Shanghai')
    dt_tz = tz.localize(dt)
    timestamp = int(dt_tz.timestamp())
    start_hours = int(timestamp / 3600)
    end_hours = start_hours + 24

    sql1 = f'''
SELECT event_date_utc, json_extract(event_parameters, '$.component') as component, count(*) as event_count
FROM `macrophage_data_{app_name}`.raw_data
WHERE event_name = 'business_startactivity' 
AND json_extract(event_parameters, '$.app_version')  = '{app_version}'
AND event_time_epoch_hour >= {start_hours} AND event_time_epoch_hour < {end_hours} AND json_extract(event_parameters, '$.os_version') = '{os_version}'
GROUP BY event_date_utc, json_extract(event_parameters, '$.component')
ORDER BY event_date_utc DESC
LIMIT 0, 10000
    '''.strip() + ';'

    sql2 = f'''
SELECT event_date_utc, json_extract(event_parameters, '$.component') as component, count(*) as event_count
FROM `macrophage_data_{app_name}`.raw_data
WHERE event_name = 'business_activityviewed' 
AND json_extract(event_parameters, '$.app_version')  = '{app_version}'
AND event_time_epoch_hour >= {start_hours} AND event_time_epoch_hour < {end_hours} AND json_extract(event_parameters, '$.os_version') = '{os_version}'
GROUP BY event_date_utc, json_extract(event_parameters, '$.component')
ORDER BY event_date_utc DESC
LIMIT 0, 10000
    '''.strip() + ';'

    with open_analytics() as cursor:
        cursor.execute(sql1)
        rows1 = cursor.fetchall()
        cursor.execute(sql2)
        rows2 = cursor.fetchall()

        date_text = datetime.now().strftime('%m%d%H%M%S')
        out_path = f'/Users/zhouzhenliang/Desktop/temp-analytics/{app_name}_ad_start_activity_vc{app_version}_{os_version}_{date_text}.csv'
        csv_file = open(out_path, 'w')
        csv_writer = csv.writer(csv_file)

        headers = ['event_date_utc', 'component', 'start_event_count', 'view_event_count', 'success_ratio']
        csv_writer.writerow(headers)

        for row1 in rows1:
            component = row1[1].strip('"')
            # if component not in ad_activity_names:
            #     continue

            date = row1[0]
            event_count = row1[2]
            csv_rows = [date, component, event_count]

            find = False
            for row2 in rows2:
                if row2[0] == date and row2[1].strip('"') == component:
                    find = True
                    count = row2[2]
                    csv_rows.append(count)
                    csv_rows.append(round(count / event_count, 3))
                    break
            if not find:
                csv_rows.append(0)
                csv_rows.append('')

            csv_writer.writerow(csv_rows)

        csv_file.close()

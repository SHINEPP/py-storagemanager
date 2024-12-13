import csv

import pandas as pd

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
    csv_path_1 = '/Users/zhouzhenliang/Desktop/temp/analytics-20241209/superstoragecleaner_activity_start_1.6.csv'
    csv_path_2 = '/Users/zhouzhenliang/Desktop/temp/analytics-20241209/superstoragecleaner_activity_view_1.6.csv'
    out_path = '/Users/zhouzhenliang/Desktop/temp/analytics-20241209/superstoragecleaner_activity_result_1.6.csv'

    df1 = pd.read_csv(csv_path_1)
    df2 = pd.read_csv(csv_path_2)

    csv_file = open(out_path, 'w')
    csv_writer = csv.writer(csv_file)

    headers = ['event_date_utc', 'component', 'start_event_count', 'view_event_count']
    csv_writer.writerow(headers)

    for i, row1 in df1.iterrows():
        component = row1.loc['component'].strip('"')
        if component not in ad_activity_names:
            continue

        date = row1.loc['event_date_utc']
        event_count = row1.loc['event_count']
        csv_rows = [date, component, event_count]

        find = False
        for j, row2 in df2.iterrows():
            if row2.loc['event_date_utc'] == date and row2.loc['component'].strip('"') == component:
                find = True
                csv_rows.append(row2.loc['event_count'])
                break
        if not find:
            csv_rows.append(0)

        csv_writer.writerow(csv_rows)

    csv_file.close()

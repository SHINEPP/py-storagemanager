import csv
import os.path

import pandas as pd

if __name__ == '__main__':
    csv_path = '/Users/zhouzhenliang/Desktop/analytics_20241125/device_file_helper_1.csv'
    name1, name2 = os.path.splitext(csv_path)
    out_path = name1 + '_out' + name2
    df = pd.read_csv(csv_path)
    csv_file = open(out_path, 'w')
    csv_writer = csv.writer(csv_file)

    dates = set()
    channels = set()
    for date in df.loc[:, 'event_date_utc']:
        dates.add(date)
    for channel in df.loc[:, 'app_channel']:
        channels.add(channel)

    events = [
        'business_dowork',
        'business_startloadactivity',
        'business_loadactivity_viewed',
        'business_adactivity_viewed',
        'business_showinterstitialad',
        'business_interstitialad_viewed',
        'business_interstitialad_revenue',

        'business_dowork_limit',
        'business_interstitialad_loadtimeout',
        'business_interstitialad_loadfailed',
        'business_interstitialad_displayfailed',
        'business_startactivity',
        'business_activityviewed'
    ]

    # head
    heads = ['date', 'app_channel']
    for i in range(len(events)):
        heads.append(f'event_name_{i + 1}')
        heads.append(f'event_count_{i + 1}')
        heads.append(f'user_count_{i + 1}')
        heads.append(f'avg_count_{i + 1}')
    for i in range(1, len(events)):
        heads.append(f'ratio_{i + 1}')

    csv_writer.writerow(heads)

    # data
    for date in sorted(dates, reverse=True):
        for channel in channels:
            values = []
            for event in events:
                find = False
                for index, row in df.iterrows():
                    if (row.loc['event_date_utc'] == date and
                            row.loc['event_name'] == event and
                            row.loc['app_channel'] == channel):
                        find = True
                        values.append((row.loc['event_count'], row.loc['user_count']))
                        break
                if not find:
                    values.append((0, 0))
            if len(values) != len(events):
                continue

            csv_rows = [date, str(channel).strip('"')]
            for i in range(len(events)):
                csv_rows.append(events[i])
                event_count, user_count = values[i]
                csv_rows.append(str(event_count))
                csv_rows.append(str(user_count))
                if user_count == 0:
                    csv_rows.append('0')
                else:
                    csv_rows.append(str(round(event_count / user_count, 1)))

            for i in range(1, len(events)):
                event_count, user_count = values[i - 1]
                event_count1, user_count1 = values[i]
                if user_count == 0:
                    ratio = 0
                else:
                    ratio = event_count / user_count
                if user_count1 == 0:
                    ratio1 = 0
                else:
                    ratio1 = event_count1 / user_count1
                if ratio == 0:
                    csv_rows.append('0')
                else:
                    csv_rows.append(str(round(100 * ratio1 / ratio, 1)) + '%')

            csv_writer.writerow(csv_rows)

    csv_file.close()

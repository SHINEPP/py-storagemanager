import pandas as pd

if __name__ == '__main__':
    csv_path = '/Users/zhouzhenliang/Desktop/analytics_20241125/device_file_helper_loaderror4.csv'
    df = pd.read_csv(csv_path)

    dates = set()
    channels = set()
    for date in df.loc[:, 'event_date_utc']:
        dates.add(date)
    for channel in df.loc[:, 'app_channel']:
        channels.add(channel)

    events = ['business_loadactivity_viewed',
              'business_adactivity_viewed',
              'business_showinterstitialad',
              'business_interstitialad_viewed']

    # head
    heads = ['date', 'app_channel']
    for i in range(len(events)):
        heads.append(f'event_name_{i + 1}')
        heads.append(f'event_count_{i + 1}')
        heads.append(f'user_count_{i + 1}')
        heads.append(f'avg_count_{i + 1}')
    for i in range(1, len(events)):
        heads.append(f'ratio_{i + 1}')
    print(','.join(heads))

    # data
    for date in sorted(dates, reverse=True):
        for channel in channels:
            values = []
            for event in events:
                for index, row in df.iterrows():
                    if (row.loc['event_date_utc'] == date and
                            row.loc['event_name'] == event and
                            row.loc['app_channel'] == channel):
                        values.append((row.loc['event_count'], row.loc['user_count']))
                        break
            if len(values) != len(events):
                continue

            event_items = []
            for i in range(len(events)):
                event_items.append(events[i])
                event_count, user_count = values[i]
                event_items.append(str(event_count))
                event_items.append(str(user_count))
                event_items.append(str(round(event_count / user_count, 1)))

            ratio_items = []
            for i in range(1, len(events)):
                event_count, user_count = values[i - 1]
                event_count1, user_count1 = values[i]
                ratio = event_count / user_count
                ratio1 = event_count1 / user_count1
                ratio_items.append(str(round(100 * ratio1 / ratio, 1)) + '%')

            f_channel = channel.strip('"')
            print(f'{date}, {f_channel}, {",".join(event_items)}, {",".join(ratio_items)}')

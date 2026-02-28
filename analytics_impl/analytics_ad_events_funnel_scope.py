import csv

import pandas as pd

"""
横向对比event，计算外弹能力漏斗数据
"""


def business_events(csv_path):
    events = [
        'business_adactivity_chance',
        'business_adactivity_viewed',
        'business_interstitialad_revenue'
    ]

    output = csv_path.replace('.csv', '_scope.csv')
    csv_file = open(output, 'w')
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['date_utc', 'security_patch'] + events)

    df = pd.read_csv(csv_path)
    df_unique = df.drop_duplicates(subset=df.columns[:2])

    for row in df_unique.itertuples(index=False):
        date_utc = row[0]
        patch = row[1]
        print(date_utc, patch)

        event_count_values = []
        for event in events:
            result = df[(df["event_date_utc"] == date_utc) &
                        (df["security_patch"] == patch) &
                        (df["event_name"] == event)]
            count = 0
            for row2 in result.itertuples(index=False):
                count = row2.event_count
                break
            print(event, count)
            event_count_values.append(count)

        csv_writer.writerow([date_utc, patch] + event_count_values)
        print('----------------------------------')

    csv_file.close()


def main():
    path = '/Users/zhouzhenliang/Desktop/Desktop/temp-analytics/chief_file_officer_events_funnel_5_0228203625.csv'
    business_events(path)


if __name__ == '__main__':
    main()

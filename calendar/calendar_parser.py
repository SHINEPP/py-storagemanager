import re
from datetime import datetime


def parse_event(event):
    result = {}
    re_event = r'Row: (\d+)(.+)'
    match = re.match(re_event, event)
    if match:
        index = match.group(1)
        values = match.group(2).split(', ')
        result['index'] = index
        for v in values:
            key, value = v.strip().split('=', 1)
            result[key] = value
    return result


if __name__ == '__main__':
    with open('export_events.txt', 'r') as file:
        lines = file.readlines()
    print('title,event_time,dtstart,rrule,duration')
    for line in lines:
        content = line.strip()
        if len(content) > 0:
            row = parse_event(content)
            # print(row)
            title = row['title']
            event_time_stamp = int(row['event_time_stamp'])
            dt = datetime.fromtimestamp(event_time_stamp / 1000)
            event_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            dtstart = int(row['dtstart'])
            dt = datetime.fromtimestamp(dtstart / 1000)
            dtstart_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            rrule = row['rrule']
            duration = row['duration']
            print(f'{title},{event_time},{dtstart_time},{rrule},{duration}')

import re
from datetime import datetime, timedelta

from icalendar import Calendar, Event, Alarm


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


def output_ics(rows: list[dict]):
    # 创建日历对象
    cal = Calendar()

    for row in rows:
        title = row['title']
        event_stamp = int(row['event_time_stamp'])
        event_stamp_date = datetime.fromtimestamp(event_stamp / 1000)
        dtstart = int(row['dtstart'])
        dtstart_date = datetime.fromtimestamp(dtstart / 1000)
        event_uuid = row['event_uuid']
        rrule = row['rrule']

        # 创建事件对象
        event = Event()
        event.add('SUMMARY', title)
        event.add('DTSTAMP', event_stamp_date)
        event.add('DTSTART', dtstart_date)  # 事件开始时间
        dtend = row['dtend']
        if dtend != 'NULL':
            dtend = int(dtend)
            dtend_date = datetime.fromtimestamp(dtend / 1000)
            event.add('DTEND', dtend_date)  # 事件结束时间
        event.add('DESCRIPTION', 'From: HUAWEI Mate 40 Pro')
        event.add('UID', event_uuid)
        event.add('STATUS', 'CONFIRMED')
        event.add('CLASS', 'PUBLIC')
        if rrule != 'NULL':
            print(f'rrule = {rrule}')
            rrule_content = {}
            values = rrule.split(';')
            for v in values:
                key, value = v.split('=')
                if key == 'UNTIL':
                    value = datetime.strptime(value, '%Y%m%dT%H%M%SZ')
                rrule_content[key] = value
            event.add('RRULE', rrule_content)

        # 创建提醒（Alarm）对象
        alarm = Alarm()
        alarm.add('trigger', timedelta(minutes=-10))  # 提前10分钟提醒
        alarm.add('action', 'DISPLAY')  # 显示提醒
        alarm.add('description', '')
        event.add_component(alarm)

        # 添加事件到日历
        cal.add_component(event)

    # 将日历对象保存为 .ics 文件
    with open('calendar_events.ics', 'wb') as f:
        f.write(cal.to_ical())


if __name__ == '__main__':
    with open('export_events.txt', 'r') as file:
        lines = file.readlines()
    in_rows = []
    for line in lines:
        content = line.strip()
        if len(content) > 0:
            in_rows.append(parse_event(content))
    output_ics(in_rows)

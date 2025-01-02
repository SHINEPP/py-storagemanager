from datetime import datetime


def today_date():
    return datetime.now().strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(today_date())

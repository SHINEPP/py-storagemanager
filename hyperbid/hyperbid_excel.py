import os

import pandas as pd


def travel_excel(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            p = os.path.join(root, file)
            if file.endswith('.xlsx') and not file.startswith('.'):
                yield p


def main(by_path):
    revenue = 0
    new_user = 0
    for p in travel_excel(by_path):
        print(p)
        df = pd.read_excel(p)
        rev = df.loc[0]['预估收益']
        new_user += df.loc[0]['新用户']
        revenue += rev
    print(f'revenue: {revenue}, new_user: {new_user}')


if __name__ == '__main__':
    main('/Users/zhouzhenliang/Desktop/Hyperbid-Report')

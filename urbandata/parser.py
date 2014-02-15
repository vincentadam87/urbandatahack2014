import os
import datetime as dt

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.getcwd()), 'data')
ANTI_SOCIAL_FN = os.path.join(DATA_DIR, 'WCC_CleansingAntiSocialBehaviour.csv')
LICENSING_FN = os.path.join(DATA_DIR, 'WCC_Licensing.csv')


def read_file(fn):
    def parse_row(row):
        return row.strip().replace('"', '').split(",")

    with open(fn, 'r') as _file:
        header = parse_row(_file.next())
        header = [h.title() for h in header]
        data = map(parse_row, _file)
        data = zip(*data)
        return dict(zip(header, data))


def get_anti_social_data():
    raw_data = read_file(ANTI_SOCIAL_FN)
    result = {}
    result['date'] = [dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
                      for x in raw_data['Eventdate']]
    for col in ['Blood', 'Urine', 'Vomit', 'Humanfouling']:
        result[col] = [x == 'YES' for x in raw_data[col]]
    for col in ['Lat', 'Long']:
        result[col] = map(float, raw_data[col])
    return result


def get_licensing_data():
    return pd.read_csv(LICENSING_FN,
                       index_col=["RepresentationResponseDate"],
                       parse_dates=["RepresentationResponseDate"])


if __name__ == '__main__':
    raw_data = read_file(ANTI_SOCIAL_FN)
    data = get_anti_social_data()
    print data['Blood']
    print data['date']

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')
ANTI_SOCIAL_FN = os.path.join(DATA_DIR, 'WCC_CleansingAntiSocialBehaviour.csv')
LICENSING_FN = os.path.join(DATA_DIR, 'IssuedLicences.csv')


def get_anti_social_data():
    df = pd.read_csv(ANTI_SOCIAL_FN,
                     index_col=["EventDate"],
                     parse_dates=["EventDate"],
                     true_values=["Yes"],
                     false_values=["NO"],
                     converters={"StreetName": lambda s: s.title()})
    df.columns = [c.title() for c in df.columns]
    return df.sort_index()


def get_licensing_data(only_alcohol_serving=False):
    """
    only_alcohol_serving: filter licencing data to only include pubs, winebars and nightclubs
    """
    df = pd.read_csv(LICENSING_FN,
                     index_col=["IssuedDate"],
                     parse_dates=["IssuedDate"])
    df.columns = [c.title() for c in df.columns]
    if only_alcohol_serving:
        ALCOHOL_TYPES = ['Type - Wine bar', 'Type - Public house or pub restaurant', 'Type - Night clubs and discos']
        df = df[np.array([x in ALCOHOL_TYPES for x in df['Premisesuse'].values])]
    return df.sort_index()


if __name__ == '__main__':
    #print get_anti_social_data().head()
    #print get_licensing_data().head()
    print sum(get_licensing_data()['Premisesuse'] == 'Type - Night clubs and discos')
    print sum(get_licensing_data()['Premisesuse'] == 'Type - Public house or pub restaurant')
    print sum(get_licensing_data()['Premisesuse'] == 'Type - Wine bar')
    #print get_licensing_data(only_alcohol_serving=True).head()


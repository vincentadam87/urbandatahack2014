import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.getcwd()), 'data')
ANTI_SOCIAL_FN = os.path.join(DATA_DIR, 'WCC_CleansingAntiSocialBehaviour.csv')
LICENSING_FN = os.path.join(DATA_DIR, 'WCC_Licensing.csv')


def get_anti_social_data():
    df = pd.read_csv(ANTI_SOCIAL_FN,
                     index_col=["EventDate"],
                     parse_dates=["EventDate"],
                     true_values=["Yes"],
                     false_values=["NO"],
                     converters={"StreetName": lambda s: s.title()})
    df.columns = [c.title() for c in df.columns]
    return df


def get_licensing_data():
    df = pd.read_csv(LICENSING_FN,
                     index_col=["RepresentationResponseDate"],
                     parse_dates=["RepresentationResponseDate"])
    df.columns = [c.title() for c in df.columns]
    return df


if __name__ == '__main__':
    print get_anti_social_data()
    print get_licensing_data()

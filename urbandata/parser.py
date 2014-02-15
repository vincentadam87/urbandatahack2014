import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')
ANTI_SOCIAL_FN = os.path.join(DATA_DIR, 'WCC_CleansingAntiSocialBehaviour.csv')
LICENSING_FN = os.path.join(DATA_DIR, 'IssuedLicences.csv')

GREENWICH = (51, 0)

def lon_lat_distance_in_meters(p1, p2):
    """
    returns the distance in meters both along the lat and longitude
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    #assert 45 < lat1 < 55 and 45 < lat2 < 55, 'Latitude1: %s Latitude2: %s' % (lat1, lat2)

    earth_radius = 6371000.   # meters
    # this distance is independent on where on earth one is
    lat_dist = 2 * math.pi * earth_radius * abs(lat1 - lat2) / 180.
    # this calculation is only correction for Greenwich, data taken from wikipedia
    meters_per_degree = 19.3 * 60 * 60
    lon_dist = abs(lon1 - lon2) * meters_per_degree
    return lat_dist, lon_dist


def distance(p1, p2):
    """
    distance between two points who are represented by langitude and longitude in meters in london approximated by greenwich's properties
    """
    lat_dist, lon_dist = lon_lat_distance_in_meters(p1, p2)
    return math.sqrt(lat_dist ** 2 + lon_dist ** 2)


def get_anti_social_data():
    df = pd.read_csv(ANTI_SOCIAL_FN,
                     index_col=["EventDate"],
                     parse_dates=["EventDate"],
                     true_values=["Yes"],
                     false_values=["NO"],
                     converters={"StreetName": lambda s: s.title()})
    df.columns = [c.title() for c in df.columns]
    xys = zip(df['Lat'].values, df['Long'].values)
    lat_to_gw, lon_to_gw = zip(*[lon_lat_distance_in_meters(xy, GREENWICH) for xy in xys])
    df['lat_to_gw'] = lat_to_gw
    df['lon_to_gw'] = lon_to_gw
    return df.sort_index()


def get_licensing_data(only_alcohol_serving=False):
    """
    only_alcohol_serving: filter licencing data to only include pubs, winebars and nightclubs
    """
    df = pd.read_csv(LICENSING_FN,
                     index_col=["IssuedDate"],
                     parse_dates=["IssuedDate"])
    df.columns = [c.title() for c in df.columns]
    xys = zip(df['Lat'].values, df['Long'].values)
    lat_to_gw, lon_to_gw = zip(*[lon_lat_distance_in_meters(xy, GREENWICH) for xy in xys])
    df['lat_to_gw'] = lat_to_gw
    df['lon_to_gw'] = lon_to_gw
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
    print get_anti_social_data()[['lat_to_gw', 'lon_to_gw']].head()
    #print get_licensing_data(only_alcohol_serving=True).head()


from descartes import PolygonPatch
import fiona
from itertools import chain
from matplotlib.collections import PatchCollection
from matplotlib.pyplot import ylim, xlim
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep

import matplotlib.pyplot as plt
import pandas as pd

def scatter_plot_map(points, shape_filename, x_inch=5, y_inch=5):
    """ 
    stolen from
    http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html#.Uv-emx-jJKZ
    """
    
    # open london shapefile, extract boundaries and width, height of map
    shp = fiona.open(shape_filename)
    bds = shp.bounds
    shp.close()
    extra = 0.01
    ll = (bds[0], bds[1])
    ur = (bds[2], bds[3])
    coords = list(chain(ll, ur))
    w, h = coords[2] - coords[0], coords[3] - coords[1]
    
    # create a Basemap instance, on which maps are plotted on
    # transverse mercator projection, ehibits less distortion
    # over areas with a small east-west extent.
    # This projection requires to specify a central
    # longitude and latitude, which I've set as -2, 49.
    # set up a map dataframe
    m = Basemap(
        projection='tmerc',
        lon_0=-2.,
        lat_0=49.,
        # ellps = 'WGS84',
        llcrnrlon=coords[0] - extra * w,
        llcrnrlat=coords[1] - extra + 0.01 * h,
        urcrnrlon=coords[2] + extra * w,
        urcrnrlat=coords[3] + extra + 0.01 * h,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)
    m.readshapefile(
        shape_filename[:-4],
        'london',
        color='none',
        zorder=2)
    
    # create polygons of map
    df_map = pd.DataFrame({
        'poly': [Polygon(xy) for xy in m.london],
        'ward_name': [ward['NAME'] for ward in m.london_info]})
    df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
    df_map['area_km'] = df_map['area_m'] / 100000
    
    # Create Point objects in map coordinates from dataframe lon and lat values
    map_points = pd.Series(
        [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(points["Long"], points["Lat"])])
    
    plaque_points = MultiPoint(list(map_points.values))
    wards_polygon = prep(MultiPolygon(list(df_map['poly'].values)))
    
    # calculate points that fall within the London boundary
    ldn_points = filter(wards_polygon.contains, plaque_points)
    # Note that the map_points series was created by passing
    # longitude and latitude values to our Basemap instance, m.
    # This converts the coordinates from long and lat degrees to
    # map projection coordinates, in metres. Our df_map dataframe
    # now contains columns holding:
    
    # a polygon for each ward in the shapefile
    # its description
    # its area in square metres
    # its area in square kilometres
    
    # We've also created a prepared geometry object from the
    # combined ward polygons.
    # We've done this in order to speed up our membership-checking
    # operation significantly. We perform the membership check
    # by creating a MultiPolygon from map_points, then filtering
    # using the contains() method, which is a binary predicate
    # returning all points which are contained within wards_polygon.
    # The result is a Pandas series, ldn_points, which we will be
    # using to make our maps.
    
    
    # Let's make a scatter plot
    # ward patches from polygons
    df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
        x,
        fc='#555555',
        ec='#787878', lw=.25, alpha=.9,
        zorder=4))
    
    # draw
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg='w', frame_on=False)
    
    # we don't need to pass points to m() because we 
    # calculated using map_points and shapefile polygons
    dev = m.scatter(
        [geom.x for geom in ldn_points],
        [geom.y for geom in ldn_points],
        5, marker='o', lw=.25,
        facecolor='#33ccff', edgecolor='w',
        alpha=0.9, antialiased=True,
        label='Blue Plaque Locations', zorder=3)
    # plot boroughs by adding the PatchCollection to the axes instance
    ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))
    
    # Draw a map scale
    m.drawmapscale(
        coords[0] + 0.08, coords[1] + 0.015,
        coords[0], coords[1],
        10.,
        barstyle='fancy', labelstyle='simple',
        fillcolor1='w', fillcolor2='#555555',
        fontcolor='#555555',
        zorder=5)
    fig.set_size_inches(x_inch, y_inch)
    ax.set_xlim([19000,30000])
    ax.set_ylim([21000, 30000])
    return fig

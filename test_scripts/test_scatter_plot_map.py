from plot import scatter_plot_map
from urbandata.parser import get_licensing_data

#shape_filename = os.sep.join(os.getcwd().split(os.sep)[:-1]) + os.sep + os.sep.join(["data", "map", "london_wards.shp"])
shape_filename="/home/heiko/daten/Dropbox/urbandatahack/ipython-notebooks/map_inspiration/london/london_wards.shp"
print shape_filename

points = get_licensing_data()[["Long", "Lat"]]

scatter_plot_map(points, shape_filename)

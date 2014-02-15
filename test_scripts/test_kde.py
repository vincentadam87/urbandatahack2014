import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('/home/vincent/Documents/Urbanhack2014/urbandatahack2014')
import urbandata.parser as parser
import urbandata.kde as kde
from scipy import stats
import pandas as pd
filename = './../data/WCC_CleansingAntiSocialBehaviour.csv'

# Loading the data
data_anti_social = parser.get_anti_social_data()
data_pub = parser.get_licensing_data()

#data_vomit = data_anti_social[data_anti_social['Vomit']]

#data_pub = data_licensing[data_licensing['Premisesuse'] == 'Type - Night clubs and discos']

len(data_pub[data_pub['Premisesuse'] == 'Type - Night clubs and discos'])
len(data_pub[data_pub['Premisesuse'] == 'Type - Wine'])
#data_pub

# density estimation on pubs
x_p = np.asarray(data_pub['Long'])
y_p = np.asarray(data_pub['Lat'])
I = np.where(x_p != 0)[0]
x_p =x_p[I]
y_p =y_p[I]

k_p =  kde.get_kernel_density(x_p,y_p)
Z_p = kde.evaluate_kernel_density_on_grid(x_p,y_p,k_p)
kde.plot_kde(x_p,y_p,Z_p)

# evaluating pub density on anti social behavior points

data_as = data_anti_social[data_anti_social['Urine']]
x_as = np.asarray(data_as['Long'])
y_as = np.asarray(data_as['Lat'])
I = np.where(x_as != 0)[0]
x_as =x_as[I]
y_as =y_as[I]

Z_as = kde.evaluate_kernel_density_on_grid(x_as,y_as,k_p)
#kde.plot_kde(x,y,Z)

z_as = kde.evaluate_kernel_density(x_as,y_as,k_p)
plt.hist(z_as)
plt.show()
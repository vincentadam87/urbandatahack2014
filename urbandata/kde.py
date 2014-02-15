from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def get_kernel_density(x,y):
    values = np.vstack([x, y])
    return stats.gaussian_kde(values)

def evaluate_kernel_density_on_grid(x,y,k):
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(k(positions).T, X.shape)
    return Z

def evaluate_kernel_density(x,y,k):
    positions = np.vstack([x, y])
    Z = np.reshape(k(positions).T, x.shape)
    return Z

def make_kde(x,y):
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)
    return Z


def plot_kde(x,y,Z):
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
    ax.plot(x, y, 'k.', markersize=2)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    plt.show()
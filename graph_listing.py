import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')


def graph_listing(listings):
    first = lambda x:x[0]
    second = lambda x:x[1]
    serials = map(first, listings)
    prices = map(second, listings)
    x = np.fromiter(prices, dtype=np.int)
    y = np.fromiter(serials, dtype=np.int)

    area = (10 * np.ones(len(x),dtype=np.int))  # 0 to 15 point radii

    plt.scatter(x, y, s=area, alpha=0.5)
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.show()

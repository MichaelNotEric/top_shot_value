import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from graph_utils import show_graph

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
	
def graph_price_at_time(graph, timestamp, price):
    timestamp64 = np.datetime64(timestamp).astype(datetime.datetime)
    if not graph:
        earlier64 = np.datetime64(timestamp - datetime.timedelta(minutes=10)).astype(datetime.datetime)
        later64 = np.datetime64(datetime.datetime.now() + datetime.timedelta(minutes=10)).astype(datetime.datetime)
        plt.axis([earlier64, later64, 0, 500])
        graph = plt.scatter(np.fromiter([timestamp64], dtype='datetime64[m]'), np.fromiter([price], dtype=np.float), alpha=0.5)        
        plt.show()      
    else:
        graph.set_xdata(np.append(graph.get_xdata(), timestamp))
        graph.set_ydata(np.append(graph.get_ydata(), price))
        plt.show()
    return graph
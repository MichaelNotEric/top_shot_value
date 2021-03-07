import time

def time_func(name, f, *args):
    start = time.time()
    f(*args)
    end = time.time()
    print("Took {0} seconds to {1}".format(int(end - start), name))
from models import *
import pandas as pd
import time


FILE = 'results.txt'
DSIZE = [10000 * i for i in range(1, 11)]
TRIES = 10


def _benchmark(func, datagen, overdata):

    frame = {}
    for index, i in enumerate(overdata):
        array = datagen(i)
        start = time.time()
        tree = func(array)
        stop = time.time()
        make = stop - start
        start = time.time()
        tree.traversal_in_order()
        stop = time.time()
        inorder = (stop-start)
        start = time.time()
        tree.search_max()
        stop = time.time()
        max_ = stop-start

        frame[index] = [str(tree), make, max_, inorder, i]
        if type(tree) is BSTtree:
            start = time.time()
            tree.search_max()
            stop = time.time()
            dsw = stop-start
            frame[index].append(dsw)

    frame = pd.DataFrame.from_dict(frame, orient='index')
    return frame


def main():

    frame = pd.DataFrame()

    for i in range(TRIES):
        frame = pd.concat([_benchmark(BSTtree, gen_data, DSIZE),
                           _benchmark(AVLtree, gen_data, DSIZE),
                           frame],
                          ignore_index=True)

    frame.rename(columns = {0: 'tree',
                            1: 'make time',
                            2: 'max time',
                            3: 'inorder time',
                            4: "dsize",
                            5: 'dsw'},
                 inplace=True)

    frame.to_csv(FILE)


main()

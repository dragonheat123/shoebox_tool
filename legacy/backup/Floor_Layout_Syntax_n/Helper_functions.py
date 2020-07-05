from random import normalvariate
import numpy as np
import matplotlib


def normalChoice(lst, mean=None, stddev=None):


    #data = ','.join(str(v) for v in lst)

    if mean is None:
        # if mean is not specified, use center of list
        mean = (len(lst) - 1) / 2

    if stddev is None:
        # if stddev is not specified, let list be -3 .. +3 standard deviations
        stddev = len(lst) / 6


    while True:
        index = int(normalvariate(mean, stddev) + 0.5)
        if 0 <= index < len(lst):
            return lst[index]


def percentile_bins(array, numBins):
    a = np.array(array)

    percentage = 100.0 / numBins
    bin_widths = [0]
    bin_ranges = []
    for i in range(0, numBins):
        # noinspection PyTypeChecker
        p_min = round ((np.percentile(a, (percentage * i))),20)
        #print 'p_min ', p_min
        bin_widths.append(p_min)
        # noinspection PyTypeChecker
        p_max = round((np.percentile(a, (percentage * (i + 1)))), 20)
        #print 'p_max ', p_max
        bin_ranges.append([round(p_min, 20), round(p_max, 20)])

    return bin_ranges


def NonLinCdict(steps, hexcol_array):
    cdict = {'red': (), 'green': (), 'blue': ()}
    for s, hexcol in zip(steps, hexcol_array):
        rgb =matplotlib.colors.hex2color(hexcol)
        cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
        cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
        cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
    return cdict
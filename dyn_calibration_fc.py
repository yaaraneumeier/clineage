from scipy import optimize
import itertools
from itertools import repeat as rep
from multiprocessing import Pool
from time import sleep, time

import numpy
from order.hist import Histogram
from experimental_data.synthetic_data import get_hists_pairs
from order.calibration.score import distance_from_model


def doWork(input_tuple):
    alg, hist_pairs, cycles_tup = input_tuple
    cycles_26, cycles_47 = cycles_tup
    def mes(up, dw):
        score = 0.0
        for syn_len, syn_hist_26, syn_hist_47 in hist_pairs:
            msmodel = (up, dw, 'mat')
            score += distance_from_model(syn_len, syn_hist_26, cycles_26, msmodel, distance_measure='con')
            score += distance_from_model(syn_len, syn_hist_47, cycles_47, msmodel, distance_measure='con')
    
    def nmes(x):
        assert len(x) % 2 == 0
        up_params = list(x)[:len(x)/2]
        dw_params = list(x)[len(x)/2:]
        up = numpy.poly1d(up_params)
        dw = numpy.poly1d(dw_params)
        return mes(up, dw)

    minimizer_kwargs = dict(method="L-BFGS-B", bounds=[(0, 0.1), (0, 0.5), (0, 0.1), (0, 0.5)], options={'eps' : 1e-3, 'disp' : True})
    res = optimize.basinhopping(nmes, [0.0, 0.003, 0.0, 0.022], minimizer_kwargs=minimizer_kwargs, niter=100)
    return res


def inputs_generator():
    hist_pairs = get_hists_pairs(filename='experimental_data/hist_by_ms_len_as_0_sum.tab')
    alg = 'con'
    for c1, c2 in itertools.product(range(11, 12, 1), range(38, 39, 1)):
        if c2 > c1:
            yield alg, hist_pairs, (c1, c2)


if __name__ == '__main__':
    # pool = Pool(processes=23)
    # rs = pool.map_async(doWork, inputs_generator(), chunksize=1)
    rs = map(doWork, inputs_generator())
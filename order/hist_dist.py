import numpy as np
from scipy.stats import ks_2samp
from preprocessing import sample_depth
from emd import emd
from math import sqrt, log10


def get_lims(hist1, hist2):
    li = min(min(hist1.keys()),min(hist2.keys()))
    ri = max(max(hist1.keys()),max(hist2.keys())) + 1
    if ri == li:
        ri = li + 1
    return li, ri


def pop_dist_sub(hist1, hist2):
    """
    Calculate the distance between two populations in the form of histograms
    Uses sum of deltas between columns hight divided by the number of columns
    """
    li, ri = get_lims(hist1, hist2)
    deltas = [abs(hist2[x]-hist1[x]) for x in range(li, ri)]
    score = float(sum(deltas))/len(range(li, ri))
    return score


def pop_dist_subpeaks(hist1, hist2):
    """
    Calculate the distance between two populations in the form of histograms
    Uses sum of deltas beween columns hight divided by the number of columns
    """
    li, ri = get_lims(hist1, hist2)
    deltas = [abs(hist2[x]-hist1[x]) for x in range(li, ri)]
    score = float(sum(deltas))/len(range(li, ri))
    return score


def pop_dist_ks_2samp(hist1, hist2, reads):
    """
    Calculate the distance between two populations in the form of histograms
    Uses 
    """
    pop1 = inflate_hist(hist1, reads)
    pop2 = inflate_hist(hist2, sample_depth)
    d, p = ks_2samp(pop1, pop2)
    return 1-p


def pop_dist_emd(hist1, hist2):
    """
    Calculate the distance between two populations in the form of histograms
    Uses
    """
    return emd(hist1.keys(), hist2.keys(), hist1.values(), hist2.values())


def pop_dist_corr(hist1, hist2):
    """
    Calculates the General Correlation Coefficient
    """
    li, ri = get_lims(hist1, hist2)
    dot_product = 0
    h1_sum_of_squares = 0
    h2_sum_of_squares = 0
    for x in range(li, ri):
        dot_product += hist1[x]*hist2[x]
        h1_sum_of_squares += hist1[x]**2
        h2_sum_of_squares += hist2[x]**2
    try:
        p = dot_product/sqrt(h1_sum_of_squares*h2_sum_of_squares)
    except ZeroDivisionError:
        print type(hist1), type(hist2)
        print hist1
        print hist2
        raise
    return 1-p


def pop_dist_corr_numpy(hist1, hist2):
    """
    
    """
    li, ri = get_lims(hist1, hist2)
    pmat = np.corrcoef([hist1[x] for x in range(li, ri)], [hist2[x] for x in range(li, ri)])
    return 1-pmat[0][1]


def pop_dist_chisq(hist1, hist2):
    """
    
    """
    li, ri = get_lims(hist1, hist2)
    running_sum = 0
    for x in range(li, ri):
        running_sum += float((hist1[x]-hist2[x])**2)/(hist1[x]+hist2[x]) if hist1[x]+hist2[x]>0 else 0
    return 2*running_sum


def pop_dist_klp(hist1, hist2):
    """
    
    """
    li, ri = get_lims(hist1, hist2)
    running_sum = 0
    for x in range(li, ri):
        running_sum += hist1[x]*log10(hist1[x]/float(hist2[x]))
    return running_sum


def pop_dist_kl(hist1, hist2):
    return (pop_dist_klp(hist1, hist2) + pop_dist_klp(hist2, hist1))/float(2)


def pop_dist(hist1, hist2, method='sub', reads=50):
    """
    Calculate the distance between two populations in the form of histograms
    Method is given as a parameter 
    """
    if method == 'sub':
        return pop_dist_sub(hist1, hist2)
    if method == 'sp':
        return pop_dist_subpeaks(hist1, hist2)
    if method == 'emd':
        return pop_dist_emd(hist1, hist2)
    if method == 'ks':
        return pop_dist_ks_2samp(hist1, hist2, reads)
    if method == 'cor':
        return pop_dist_corr(hist1, hist2)
    if method == 'con':
        return pop_dist_corr_numpy(hist1, hist2)
    if method == 'chi':
        return pop_dist_chisq(hist1, hist2)
    if method == 'kl':
        return pop_dist_kl(hist1, hist2)
    print 'unknown method'
    raise
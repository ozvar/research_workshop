import numpy as np
from scipy import stats


def __compute_md_from_effect_size(sd, effect_size):
    '''
    Docstring here
    '''
    pooled_sd = ((sd ** 2 + sd ** 2) / 2) ** 0.5
    mean_difference = pooled_sd * effect_size
    return abs(mean_difference)


def generate_samples(n, effect_size, sd=1.0):
    '''
    Docstring here
    '''
    higher = effect_size < 0
    mean_difference = __compute_md_from_effect_size(
        sd=sd,
        effect_size=effect_size
    )
    # for easiness we assume a gaussina centered at zero with unit sd
    experimental = np.random.normal(
        loc=0,
        scale=sd,
        size=n
    )
    if higher:
        control = np.random.normal(
            loc=mean_difference,
            scale=sd,
            size=n
        )
    else:
        control = np.random.normal(
            loc=-mean_difference,
            scale=sd,
            size=n
        )
    return experimental, control


def generate_correlated_samples(r, n):
    '''
    Docstring here
    '''
    correlated_data = np.random.multivariate_normal(
        mean=[0, 0],
        cov=[[1, r], [r, 1]],
        size=n
    )
    x, y = correlated_data[:, 0], correlated_data[:, 1]
    rho, p = stats.pearsonr(
        x,
        y
    )
    return x, y, round(rho, 3), round(p, 3)


def cohen_d(t, n):
    '''
    Docstring here
    '''
    d = (2*t) / ((n-1) ** 0.5)
    return d

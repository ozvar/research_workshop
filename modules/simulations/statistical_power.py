from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import numpy as np

from scipy.stats import ttest_ind
from statsmodels.stats.power import tt_ind_solve_power

from utilities.simu_utilities import *
from utilities.viz_utilities import *


def simulate_experiments(sample_sizes, effect_size, n_experiments, alpha=0.05):
    '''
    Docstring here
    '''
    experiments_outcomes = []
    achieved_powers = []
    for size in sample_sizes:

        achieved_power = tt_ind_solve_power(
            effect_size=effect_size,
            nobs1=size,
            alpha=alpha,
            ratio=1.0
        )

        p_values=[]
        effect_sizes=[]
        for experiment in range(n_experiments):

            group_1, group_2 = generate_samples (
                n=size,
                effect_size=effect_size,
                sd=1.0
            )

            t, p = ttest_ind(
                a=group_1,
                b=group_2
            )
            p_values.append(round(p, 3))
            effect_sizes.append(round(cohen_d(t=t, n=size * 2), 3))

        experiments_outcomes.append(
            {'p_values' : p_values,
             'effect_sizes' : effect_sizes
            }
        )
        achieved_powers.append(achieved_power)

    visualize_experiments(
        sizes=sample_sizes,
        experiments=experiments_outcomes,
        powers=achieved_powers,
        alpha=alpha,
        effect_size=effect_size
    )


def simulate_correlations(correlations, sample_sizes):
    '''
    Docstring here
    '''
    for r in correlations:

        x_0, y_0, r_0, p_0 = generate_correlated_samples (
            r=r,
            n=sample_sizes[0]
        )
        x_1, y_1, r_1, p_1 = generate_correlated_samples (
            r=r,
            n=sample_sizes[1]
        )
        visualize_correlation(
            x=[x_0, x_1],
            y=[y_0, y_1],
            r=[r_0, r_1],
            p=[p_0, p_1]
        )


def simulate_file_drawer(sample_size, effect_size_mu, effect_size_sigma,
                         n_experiments, alpha=0.05):
    '''
    Docstring here
    '''
    observed_distribution_effect = []
    real_distribution_effect = np.random.normal(
        loc=effect_size_mu,
        scale=effect_size_sigma,
        size=n_experiments
    )
    for experiment in range(n_experiments):

        sampled_effect = np.random.choice(
            a=real_distribution_effect,
            size=1
        )
        experimental, control = generate_samples (
            n=sample_size,
            effect_size=sampled_effect,
            sd=1.0,
        )
        achieved_power = tt_ind_solve_power(
            effect_size=sampled_effect,
            nobs1=sample_size,
            alpha=alpha,
            ratio=1.0
        )
        t, p = ttest_ind(
            a=experimental,
            b=control
        )
        if p < alpha:
            observed_distribution_effect.append(
                cohen_d(
                    t=t,
                    n=sample_size*2
                )
            )
    visualize_distribution(
        real_distribution=real_distribution_effect,
        observed_distribution=observed_distribution_effect,
        title='Observed Effect Size Distribution of Only Significant Results'
    )


if __name__ == '__main__':

    VIZ_SAVE_PATH = '{}\\figures'.format(
        dirname(dirname(abspath(__file__)))
    )
    simulate_experiments(
        sample_sizes=[5, 10, 20, 50, 100, 200, 400],
        effect_size=0.3,
        n_experiments=100
    )

    simulate_correlations(
        correlations=[0.05, 0.3, 0.6],
        sample_sizes=[30, 30000]
    )
    simulate_file_drawer(
        sample_size=20,
        effect_size_mu=0.5,
        effect_size_sigma=0.05,
        n_experiments=1000,
        alpha=0.05
    )
    

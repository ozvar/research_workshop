import time

import numpy as np

from scipy.stats import ttest_ind
from statsmodels.stats.power import tt_ind_solve_power

import winsound
import playsound

from ..utilities.simu_utilities import cohen_d
from ..utilities.simu_utilities import generate_samples
from ..utilities.simu_utilities import generate_correlated_samples
from ..utilities.viz_utilities import visualize_correlation
from ..utilities.viz_utilities import visualize_distribution
from ..utilities.viz_utilities import visualize_experiments


def p_value_sonata(sample_size, effect_size, n_experiments,
                   threshold=None, sounds_path=None, verbose=True):
    '''
    Docstring here
    '''
    p_values_range = np.arange(0.000, 1.001, 0.001)
    sounds_range = np.flip(np.arange(99, 1101))
    p_to_sound = {
        round(p, 3): sound for p, sound in zip(p_values_range, sounds_range)
    }

    p_values = []
    for experiment in range(n_experiments):

        group_1, group_2 = generate_samples(
            n=sample_size,
            effect_size=effect_size,
            sd=1.0
        )

        t, p = ttest_ind(
            a=group_1,
            b=group_2
        )
        p_values.append(round(p, 3))

    for p in p_values:

        if threshold is not None:
            if p < threshold:
                playsound.playsound('{}\\coin.mp3'.format(sounds_path))
            else:
                playsound.playsound('{}\\china.mp3'.format(sounds_path))
        else:
            winsound.Beep(
                p_to_sound[p],
                250
            )

        time.sleep(0.10)


def simulate_experiments(sample_sizes, effect_size, n_experiments,
                         viz_path, alpha=0.05, verbose=True):
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

        p_values = []
        effect_sizes = []
        for experiment in range(n_experiments):

            group_1, group_2 = generate_samples(
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
            {'p_values': p_values,
             'effect_sizes': effect_sizes
             }
        )
        achieved_powers.append(achieved_power)

    visualize_experiments(
        sizes=sample_sizes,
        experiments=experiments_outcomes,
        powers=achieved_powers,
        alpha=alpha,
        effect_size=effect_size,
        viz_path=viz_path,
        verbose=verbose
    )


def simulate_correlations(correlations, sample_0, sample_1, viz_path,
                          verbose=True):
    '''
    Docstring here
    '''
    for r in correlations:

        x_0, y_0, r_0, p_0 = generate_correlated_samples(
            r=r,
            n=sample_0
        )
        x_1, y_1, r_1, p_1 = generate_correlated_samples(
            r=r,
            n=sample_1
        )
        visualize_correlation(
            x=[x_0, x_1],
            y=[y_0, y_1],
            r=[r_0, r_1],
            p=[p_0, p_1],
            viz_path=viz_path,
            verbose=verbose,
            real_r=r
        )


def simulate_file_drawer(sample_size, effect_size_mu, effect_size_sigma,
                         n_experiments, viz_path, alpha=0.05, verbose=True):
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
        experimental, control = generate_samples(
            n=sample_size,
            effect_size=sampled_effect,
            sd=1.0,
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
        title='Observed Effect Size Distribution of Only Significant Results',
        viz_path=viz_path,
        verbose=True
    )

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
                   alpha=None, sounds_path=None, verbose=True):
    '''
    Function for playing different sounds depending on the p values
    obtained from a series of simulated "experiments". If no alpha
    is provided the sound will increase in tone depending on the 
    value of p otherwie a significant and no significant sound 
    will be played.

    Args:
        - sample_size: an integer specifying the sample size of each 
          of the two groups in the simulated experiments.
        - effect_size: a float specifying the magnitude of the
          difference between the two groups in the simulated 
          experiments (Cohen's d).
        - n_experiments: an integer specifying the number of 
          simulated experiments.
        - alpha: a float specifying the p-value threshold for
          considering the results of an experiment statistically
          significant. Only used when threshold != None.
        - sounds_path: a string specifying the location of the
          sound files played for significant and non-significant 
          results.
        - verbose: a bolean kept only for consistency.
        
    Returns:
        - None
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

        if alpha is not None:
            if p < alpha:
                playsound.playsound('{}\\sig.mp3'.format(sounds_path))
            else:
                playsound.playsound('{}\\non_sig.mp3'.format(sounds_path))
        else:
            winsound.Beep(
                p_to_sound[p],
                250
            )

        time.sleep(0.10)


def simulate_experiments(sample_sizes, effect_size, n_experiments,
                         viz_path, alpha=0.05, verbose=True):
    '''
    Function for simulating and comparing experiments carried out 
    with different sample sizes. For each experiment effect size 
    and alpha are fixed.

    Args:
        - sample_size: an integer specifying the sample size of each 
          of the two groups in the simulated experiments.
        - effect_size: a float specifying the magnitude of the
          difference between the two groups in the simulated 
          experiments (Cohen's d).
        - n_experiments: an integer specifying the number of 
          simulated experiments.
        - viz_path: a string specifying the location where to
          save the plotted results.
        - alpha: a float specifying the p-value threshold for
          considering the results of an experiment statistically
          significant.
        - verbose: a bolean specifying if the plotted results are showed 
          on screen.
        
    Returns:
        - None
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
    Function for simulating and comparing correlations between 
    two groups differing in sample size.

    Args:
        - correlations: an iterable of float containing the r values
          the will be tested.
        - sample_0: an integer specifying the sample size for the
          first group.
        - sample_1: an integer specifying the sample size for the
          second group.
        - viz_path: a string specifying the location where to
          save the plotted results.
        - verbose: a bolean specifying if the plotted results are showed 
          on screen.
        
    Returns:
        - None
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
    Function for simulating and visualizing a file-drawer effect. 
    
    We assume  that the effect size linked to a specific phenomenon under 
    investigation will oscillate (for various reasons: e.g. noise) producing 
    a normal distribution with mean mu and standard deviation sigma. 
    
    We will then sample from this distribution and simulate experiments with 
    the obtained effect size. At this point we will compute and retain only 
    the estimated (not the "real" sampled effect size) effect size for 
    those experiments which appeared to lead to statistically significant 
    results. We will then compare the ground truth distribution of effect 
    sizes with the observed one.

    This simulation aims to show what happens to the estimated effect sizes
    when researchers conduct experiments with low power and decide to report
    only significant results.

    Args:
        - sample size: an integer specifying the sample size of each 
          of the two groups in the simulated experiments.
        - effect_size_mu: a float specifying the mean of the ground 
          truth effect size distribution.
        - effect_size_sigma: a float specifying the std of the ground 
          truth effect size distribution.
        - n_experiments: an integer specifying the number of 
          simulated experiments.          
        - viz_path: a string specifying the location where to
          save the plotted results.
        - alpha: a float specifying the p-value threshold for
          considering the results of an experiment statistically
          significant.
        - verbose: a bolean specifying if the plotted results are showed 
          on screen.
        
    Returns:
        - None
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

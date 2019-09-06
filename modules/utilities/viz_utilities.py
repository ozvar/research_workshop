import matplotlib.pyplot as plt
import seaborn as sns


def visualize_experiments(sizes, experiments, powers,
                          effect_size, viz_path, alpha=0.05, verbose=True):
    '''
    Docstring here
    '''
    sns.set(
        font_scale=1.5,
        style='whitegrid'
    )
    fig, axs = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10, 10)
    )
    for size, experiment, power in zip(sizes, experiments, powers):

        n_experiments = len(experiment['p_values'])

        experiment['p_values'].sort()
        experiment['effect_sizes'].sort(reverse=True)

        axs[0].plot(
            [i for i in range(1, n_experiments + 1)],
            experiment['p_values'],
            marker='.',
            label='N: {} Beta: {}'.format(size * 2, power)
        )
        axs[0].set_xlabel('Experiment Number')
        axs[0].set_ylabel('P value')
        axs[0].set_xlim(1, n_experiments)
        axs[0].set_ylim(0.0, 1.0)
        axs[0].axvline(
            x=int((len(experiment['p_values']) * alpha)),
            linestyle='--',
            c='r'
        )
        axs[0].axhline(
            y=alpha,
            linestyle='--',
            c='r'
        )

        axs[1].plot(
            [i for i in range(1, n_experiments + 1)],
            experiment['effect_sizes'],
            marker='.',
            label='N: {} Beta: {}'.format(size * 2, power)
        )
        axs[1].set_xlabel('Experiment Number')
        axs[1].set_ylabel("Observed Cohen's d")
        axs[1].set_xlim(1, n_experiments)

    plt.suptitle(
        '{} experiments '
        'with alpha {} '
        'and effect size {}'.format(n_experiments, alpha, effect_size)
    )

    plt.legend()
    plt.savefig('{}\\simulated_experiments.jpg'.format(viz_path))
    plt.close()
    if verbose:
        plt.show()


def visualize_correlation(x, y, r, real_r, p, viz_path, verbose=True):
    '''
    Docstring here
    '''
    sns.set(
        font_scale=1.5,
        style='whitegrid'
    )
    fig, axs = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10, 10)
    )

    for index in range(2):

        sns.regplot(
            x=x[index],
            y=y[index],
            ax=axs[index],
            scatter_kws={'s': 10}
        )
        axs[index].set_xlabel('Variable X')
        axs[index].set_ylabel('Variable Y')
        axs[index].set_title(
            'N {} - '
            'Cor Coef {} - '
            'P Value {} '.format(len(x[index]), r[index], p[index])
        )

    plt.savefig('{}\\simulated_correlations_{}.jpg'.format(viz_path, real_r))
    plt.close()
    if verbose:
        plt.show()


def visualize_distribution(real_distribution, observed_distribution,
                           title, viz_path, metric="Cohen's D", verbose=True):
    '''
    Docstring here
    '''
    sns.set(
        font_scale=1.5,
        style='whitegrid'
    )
    plt.figure(figsize=(10, 10))
    sns.distplot(
        a=real_distribution,
        hist=False,
        color='b',
        kde_kws={'shade': True},
        label='Real Distribution {}'.format(metric)
    )
    sns.distplot(
        a=observed_distribution,
        hist=False,
        color='r',
        kde_kws={'shade': True},
        label='Observed Distribution {}'.format(metric)
    )
    plt.xlabel(metric)
    plt.ylabel('Density')
    plt.title(title)
    plt.savefig('{}\\simulated_filedrawer.jpg'.format(viz_path))
    plt.close()
    if verbose:
        plt.show()

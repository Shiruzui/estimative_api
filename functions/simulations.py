import numpy as np


def run_monte_carlo_simulation(tasks, num_iterations, distribution_type):
    if distribution_type == 'normal':
        return monte_carlo_simulation_normal(tasks, num_iterations)
    else:
        return monte_carlo_simulation_triangular(tasks, num_iterations)


def monte_carlo_simulation_triangular(tasks, num_iterations):
    pert_random = np.random.triangular(
        [task['min'] for task in tasks],
        [task['likely'] for task in tasks],
        [task['max'] for task in tasks],
        size=(num_iterations, len(tasks))
    )
    return np.sum(pert_random, axis=1)


def monte_carlo_simulation_normal(tasks, num_iterations):
    pert_random = np.random.normal(
        loc=[task['mean'] for task in tasks],
        scale=[task['std_dev'] for task in tasks],
        size=(num_iterations, len(tasks))
    )
    return np.sum(pert_random, axis=1)

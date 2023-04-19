import numpy as np


def run_monte_carlo_simulation(tasks, num_iterations, distribution_type):
    if distribution_type == 'normal':
        return monte_carlo_simulation_normal(tasks, num_iterations)
    else:
        return monte_carlo_simulation_triangular(tasks, num_iterations)


def monte_carlo_simulation_triangular(tasks, num_iterations):
    total_durations = []
    for _ in range(num_iterations):
        iteration_duration = 0
        for task in tasks:
            pert_random = np.random.triangular(
                task['min'], task['likely'], task['max'])
            iteration_duration += pert_random
        total_durations.append(iteration_duration)
    return total_durations


def monte_carlo_simulation_normal(tasks, num_iterations):
    total_durations = []
    for _ in range(num_iterations):
        iteration_duration = 0
        for task in tasks:
            pert_random = np.random.normal(
                loc=task['mean'], scale=task['std_dev'])
            iteration_duration += pert_random
        total_durations.append(iteration_duration)
    return total_durations

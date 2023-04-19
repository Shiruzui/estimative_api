import numpy as np


def calculate_mean_std_dev(tasks):
    for task in tasks:
        task['mean'] = (task['min'] + 4 * task['likely'] + task['max']) / 6
        task['std_dev'] = (task['max'] - task['min']) / 6
    return tasks


def calculate_mean(total_durations):
    mean_duration = np.mean(total_durations)
    return round(mean_duration, 2)


def calculate_median(total_durations):
    median_duration = np.median(total_durations)
    return round(median_duration, 2)


def calculate_std_dev(total_durations):
    std_dev_duration = np.std(total_durations)
    return round(std_dev_duration, 2)


def calculate_percentiles(percentiles, total_durations):
    percentiles_values = {}
    for percentile in percentiles:
        value = np.percentile(total_durations, percentile)
        percentiles_values[f'P{percentile}'] = round(value, 2)

    return percentiles_values

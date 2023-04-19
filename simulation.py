import os
import matplotlib.pyplot as plt
from pyimgur import Imgur
import numpy as np


def calculate_mean_std_dev(tasks):
    for task in tasks:
        task['mean'] = (task['min'] + 4 * task['likely'] + task['max']) / 6
        task['std_dev'] = (task['max'] - task['min']) / 6
    return tasks


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


CLIENT_ID = '56f8eb244ea13c1'


def create_and_upload_histogram(img_opt, total_durations, mean_duration, median_duration, calc_uuid):
    plt.figure(figsize=(img_opt['width'], img_opt['height']))
    plt.title(img_opt['title'])
    plt.hist(total_durations, bins=img_opt['bins'], density=img_opt['density'],
             alpha=img_opt['alpha'], label=img_opt['label'])
    plt.axvline(mean_duration, color='red',
                linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(median_duration, color='green',
                linestyle='dotted', linewidth=2, label='Mediana')
    plt.xlabel(img_opt['xlabel'])
    plt.ylabel(img_opt['ylabel'])
    plt.legend()

    temp_folder = check_temp_folder()

    filename = f"{temp_folder}/{calc_uuid}.png"
    plt.savefig(filename)
    # plt.close()
    imgur_link = upload_imgur(filename, calc_uuid)
    os.remove(filename)
    return imgur_link


def check_temp_folder():
    temp_folder = "temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    return temp_folder


def upload_imgur(filename: str, calc_uuid: str):
    imgur = Imgur(client_id=CLIENT_ID)
    image = imgur.upload_image(filename, title=calc_uuid)
    return image.link

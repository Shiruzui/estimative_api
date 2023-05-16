import uuid

import numpy as np

from functions.image_generator import create_and_upload_histogram
from functions.simple_statistics import calculate_mean_std_dev, calculate_mean, calculate_median, calculate_std_dev, \
    calculate_percentiles
from functions.simulations import run_monte_carlo_simulation
from response.post_response import to_post_response
from validations.validations import TaskSchema


def process_post_request(args):
    tasks_schema = TaskSchema(many=True)
    tasks = args["tasks"]
    if isinstance(tasks, list):
        tasks = tasks_schema.load(tasks)
    else:
        tasks = [tasks_schema.load(tasks)]

    iterations = args['iterations']
    distribution_type = args['type']
    percentiles = args["percentiles"]
    participants = args['participants']

    if isinstance(percentiles, int):
        percentiles = [percentiles]

    image = args['image']
    img_opt = image['img_opt']

    tasks = calculate_mean_std_dev(tasks=tasks)
    total_durations = run_monte_carlo_simulation(
        tasks, iterations, distribution_type, participants)

    mean_duration = calculate_mean(total_durations)
    median_duration = calculate_median(total_durations)
    std_dev_duration = calculate_std_dev(total_durations)
    calculated_percentiles = calculate_percentiles(
        percentiles, total_durations)

    calc_uuid = f'CALC_{str(uuid.uuid4()).upper()}'

    imgur_url = None
    if image['plot']:
        imgur_url = create_and_upload_histogram(
            img_opt, total_durations, mean_duration, median_duration, calc_uuid)

    response_payload = to_post_response(tasks, mean_duration, median_duration,
                                        std_dev_duration, distribution_type, iterations, calculated_percentiles,
                                        imgur_url)
    return response_payload, None, 201

from datetime import datetime
import uuid
from database import Database
from simulation import calculate_mean, calculate_mean_std_dev, calculate_median, calculate_percentiles, calculate_std_dev, create_and_upload_histogram, run_monte_carlo_simulation
from validations import task_schema, tasks_schema


def process_request(args, calc_uuid=None, is_update=False):
    db = Database("db/results.json")

    if is_update:
        existing_data = db.get(calc_uuid)
        if not existing_data:
            return None, {"message": "Estimativa não encontrada"}, 404

        # Atualiza os campos existentes com os novos valores fornecidos na requisição
        existing_data.update(args)
        args = existing_data

    tasks = args["tasks"]
    if isinstance(tasks, list):
        tasks = tasks_schema.load(tasks)
    else:
        tasks = [task_schema.load(tasks)]

    iterations = args['iterations']
    distribution_type = args['type']
    percentiles = args["percentiles"]

    if isinstance(percentiles, int):
        percentiles = [percentiles]

    image = args['image']
    img_opt = image['img_opt']

    tasks = calculate_mean_std_dev(tasks=tasks)
    total_durations = run_monte_carlo_simulation(
        tasks, iterations, distribution_type)

    mean_duration = calculate_mean(total_durations)
    median_duration = calculate_median(total_durations)
    std_dev_duration = calculate_std_dev(total_durations)
    calculated_percentiles = calculate_percentiles(
        percentiles, total_durations)

    if not calc_uuid:
        calc_uuid = f'CALC_{str(uuid.uuid4()).upper()}'

    imgur_url = None
    if image['plot']:
        imgur_url = create_and_upload_histogram(
            img_opt, total_durations, mean_duration, median_duration, calc_uuid)

    response_payload = to_response(calc_uuid, tasks, mean_duration, median_duration,
                                   std_dev_duration, distribution_type, iterations, calculated_percentiles, image['plot'], imgur_url)

    if is_update:
        response_payload["updated_at"] = datetime.now().strftime(
            '%Y-%m-%d_%H:%M:%S')

    db.set(calc_uuid, response_payload)

    return response_payload, None, 200


def to_response(calc_uuid, tasks, mean, median, std_dev, _type, iterations, percentiles, generate_image, image_link):
    response = {
        "id": calc_uuid
    }

    if generate_image:
        response["image_url"] = image_link

    response |= {
        "tasks": tasks,
        "iterations": iterations,
        "type": _type,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "perncetiles": percentiles,
        "created_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
    }

    return response

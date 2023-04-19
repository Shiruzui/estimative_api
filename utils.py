from datetime import datetime
import uuid
from database import Database
from simulation import calculate_mean, calculate_mean_std_dev, calculate_median, calculate_percentiles, calculate_std_dev, create_and_upload_histogram, run_monte_carlo_simulation


def process_request(request_data, calc_uuid=None, is_update=False):
    db = Database("db/results.json")
    if is_update:
        existing_data = db.get(calc_uuid)
        if not existing_data:
            return None, {"message": "Estimativa não encontrada"}, 404

        # Atualiza os campos existentes com os novos valores fornecidos na requisição
        existing_data.update(request_data)
        request_data = existing_data

    if not request_data or 'tasks' not in request_data:
        return None, {"message": "Dados necessários não fornecidos"}, 400

    tasks = request_data['tasks']
    iterations = request_data.get('iterations', 1000)
    distribution_type = request_data.get('type', 'triangular')
    percentiles = request_data.get('percentiles', [50, 70, 90, 100])
    image = request_data.get('image', {"plot": True})
    img_opt = image.get('img_opt', {
        "width": 5,
        "height": 5,
        "bins": 20,
        "density": True,
        "alpha": 0.75,
        "label": "Duração do projeto",
        "xlabel": "Dias",
        "ylabel": "Probabilidade",
        "title": "Estimativa do projeto"
    })

    generate_image = image.get('plot', True)

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

    imgur_url = create_and_upload_histogram(img_opt,
                                            total_durations, mean_duration, median_duration, calc_uuid)

    response_payload = to_response(calc_uuid, tasks, mean_duration, median_duration,
                                   std_dev_duration, distribution_type, iterations, calculated_percentiles, imgur_url, generate_image)

    if is_update:
        response_payload["updated_at"] = datetime.now().strftime(
            '%Y-%m-%d_%H:%M:%S')

    db.set(calc_uuid, response_payload)

    return response_payload, None, 200


def to_response(calc_uuid, tasks, mean, median, std_dev, _type, iterations, percentiles, image_link, generate_image):
    response = {
        "id": calc_uuid,
        "tasks": tasks,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "type": _type,
        "iterations": iterations,
        "perncetiles": percentiles,
        "created_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    }

    if generate_image:
        response["image_url"] = image_link

    return response

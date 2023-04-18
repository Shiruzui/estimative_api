def process_request(request_data, calc_uuid=None):
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
        "title'": "Estimativa do projeto"
    })

    # Validação dos dados e cálculos
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

    imgur_url = create_and_upload_histogram(
        img_opt, total_durations, mean_duration, median_duration, calc_uuid)

    response_payload = to_response(calc_uuid, tasks, mean_duration, median_duration,
                                   std_dev_duration, distribution_type, iterations, calculated_percentiles, imgur_url)

    # Adicionar o campo "updated_at" se calc_uuid for fornecido
    if calc_uuid:
        response_payload["updated_at"] = datetime.now().strftime(
            '%Y-%m-%d_%H:%M:%S')

    db = Database("db/results.json")
    db.set(calc_uuid, response_payload)

    return response_payload, None, None


def to_response(calc_uuid, tasks, mean, median, std_dev, _type, iterations, percentiles, image_link):
    return {
        "id": calc_uuid,
        "tasks": tasks,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "type": _type,
        "iterations": iterations,
        "perncetiles": percentiles,
        "image_url": image_link,
        "created_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    }

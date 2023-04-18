import uuid
from flask import Flask, make_response, request, jsonify
from database import Database
from simulation import calculate_mean, calculate_mean_std_dev, calculate_median, calculate_percentiles, calculate_std_dev, create_and_upload_histogram, run_monte_carlo_simulation, to_response
from messages import INDEX_MESSAGE

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def default():
    return jsonify({"message": INDEX_MESSAGE})


@app.route('/estimative', methods=['GET'])
def get_all_estimatives():
    db = Database("db/results.json")
    estimatives = [value for key, value in db.items()]
    return (
        jsonify(estimatives)
        if estimatives
        else (jsonify({"message": "Estimativas não encontrada."}), 400)
    )


@app.route('/estimative/<calc_uuid>', methods=['GET'])
def get_estimative(calc_uuid):
    db = Database("db/results.json")
    estimative = db.get(calc_uuid)
    return (
        jsonify(estimative)
        if estimative
        else make_response(
            jsonify({"message": "Estimativa não encontrada"}), 404
        )
    )


@app.route('/estimative', methods=['POST'])
def calculate():
    data = request.get_json()

    if not data or 'tasks' not in data:
        return jsonify({"message": "Dados necessários não fornecidos"}), 400

    tasks = data['tasks']
    iterations = data.get('iterations', 1000)
    distribution_type = data.get('type', 'triangular')
    percentiles = data.get('percentiles', [50, 70, 90, 100])
    image = data.get('image', {"plot": True})
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

    calc_uuid = f'CALC_{str(uuid.uuid4()).upper()}'
    imgur_url = create_and_upload_histogram(img_opt,
                                            total_durations, mean_duration, median_duration, calc_uuid)

    response_payload = to_response(calc_uuid, tasks, mean_duration, median_duration,
                                   std_dev_duration, distribution_type, iterations, calculated_percentiles, imgur_url)

    db = Database("db/results.json")
    db.set(calc_uuid, response_payload)

    return jsonify(response_payload), 201


if __name__ == '__main__':
    app.run(debug=True)

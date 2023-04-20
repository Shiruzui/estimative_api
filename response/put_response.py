from utils.utils import get_formatted_current_date


def to_put_response(calc_uuid, tasks, mean_duration, median_duration,
                    std_dev_duration, distribution_type, iterations, calculated_percentiles,
                    imgur_url, created_at):
    response = {
        "id": calc_uuid
    }
    if imgur_url:
        response['image_url'] = imgur_url

    response |= {
        "tasks": tasks,
        "iterations": iterations,
        "type": distribution_type,
        "mean_duration": mean_duration,
        "median_duration": median_duration,
        "std_dev_duration": std_dev_duration,
        "percentiles": calculated_percentiles,
        "created_at": created_at,
        "updated_at": get_formatted_current_date()
    }

    return response

from utils.utils import get_formatted_current_date


def to_post_response(tasks, mean, median, std_dev, _type, iterations, percentiles, image_link):
    response = {}

    if image_link:
        response["image_url"] = image_link

    response |= {
        "tasks": tasks,
        "iterations": iterations,
        "type": _type,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "perncetiles": percentiles,
        "created_at": get_formatted_current_date(),
    }

    return response

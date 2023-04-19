import os
import matplotlib.pyplot as plt
from pyimgur import Imgur
from utils.utils import check_temp_folder


CLIENT_ID = os.environ.get("IMGUR_API_KEY")


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
    plt.close()
    imgur_link = upload_imgur(filename, calc_uuid)
    os.remove(filename)
    return imgur_link


def upload_imgur(filename: str, calc_uuid: str):
    imgur = Imgur(client_id=CLIENT_ID)
    image = imgur.upload_image(filename, title=calc_uuid)
    return image.link

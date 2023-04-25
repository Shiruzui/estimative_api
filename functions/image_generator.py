import os
import matplotlib.pyplot as plt
from pyimgur import Imgur
from utils.utils import check_temp_folder


CLIENT_ID = os.environ.get("IMGUR_API_KEY")

def create_and_upload_histogram(img_opt, total_durations, mean_duration, median_duration, calc_uuid):
    plt.rcParams.update({'font.size': img_opt['font_size']})
    plt.figure(figsize=(img_opt['width'], img_opt['height']))
    plt.title(img_opt['title'])
    plt.hist(total_durations, bins=img_opt['bins'], density=img_opt['density'],
             alpha=img_opt['alpha'], label=img_opt['label'], color=img_opt['dist_color'])
    plt.axvline(mean_duration, color=img_opt['mean_color'],
                linestyle='dashed', linewidth=4, label='Média')
    plt.axvline(median_duration, color=img_opt['median_color'],
                linestyle='dotted', linewidth=4, label='Mediana')
    plt.xlabel(img_opt['xlabel'])
    plt.ylabel(set_ylabel(['ylabel']))
    plt.legend()

    if img_opt['grid']:
        plt.grid(color='grey', alpha=.75)

    

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
    image.privacy = 'hidden'
    image.update()
    return image.link

# def upload_imgur(filename: str, calc_uuid: str):
#     imgur = Imgur(client_id=CLIENT_ID)
#     image = imgur.upload_image(filename, title=calc_uuid)
#     return image.link


def set_ylabel(density:bool):
    return 'Densidade de probabilidade"' if density else 'Frequência'
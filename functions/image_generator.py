import os
import io
import base64
import requests
import matplotlib.pyplot as plt

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
    plt.ylabel(set_ylabel(img_opt['density']))
    plt.legend()

    if img_opt['grid']:
        plt.grid(color='grey', alpha=.75)

    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    plt.close()

    img_data.seek(0)
    imgur_link = upload_imgur(img_data, calc_uuid)

    return imgur_link


def upload_imgur(img_data, calc_uuid):
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
    data = {"image": base64.b64encode(img_data.read()).decode('ascii'), "type": "base64", "name": f"{calc_uuid}.png", "title": calc_uuid}
    response = requests.post('https://api.imgur.com/3/upload', headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['data']['link']
    else:
        raise Exception(f"Upload failed: {response.json()}")


def set_ylabel(density: bool):
    return 'Densidade de probabilidade' if density else 'Frequência'

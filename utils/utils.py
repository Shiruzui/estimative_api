import os
from datetime import datetime


def get_formatted_current_date() -> str:
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


def check_folder_existence(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


def check_temp_folder():
    temp_folder = "temp"
    return check_folder_existence(temp_folder)

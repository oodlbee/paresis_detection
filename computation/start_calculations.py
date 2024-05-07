
import os
from typing import Callable
from pathlib import Path

from computation.get_video_symmetries import get_video_symmetries


def main_start(event, queue, video_file_path:str, markup_file_path:str, save_to_path:str):
    
    # Changing file paths type
    video_file_path = Path(video_file_path)
    markup_file_path = Path(markup_file_path)
    save_to_path = Path(save_to_path)

    video_file_path = str(video_file_path)
    markup_file_path = str(markup_file_path)

    get_video_symmetries(event, queue, video_file_path, markup_file_path, save_to_path)
    
    


def get_list_of_files(dir_path):
    """Makes a list of strings of file's paths from directiory"""
    list_of_file = Path.iterdir(dir_path)           
    all_files = []
    for file in list_of_file:
        full_path = dir_path.joinpath(file)
        if Path.is_dir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)             
    return all_files


if __name__ == "__main__":
    main_start(
        'application/app_handlers/temp/20180125_Mordashov_1.mp4',
        'application/app_handlers/temp/markup.xlsx',
        'application/app_handlers/temp'
        )
import sys
import json
import imageio
import os
import pandas as pd
from pathlib import Path

from get_video_points import get_video_points
from get_video_symmetries import get_video_symmetries


def main_start(predictor_file_path, video_file_path, markup_file_path, save_to_files):

    video_file_name = os.path.basename(video_file_path)
    points_file_path = save_to_files + '/points/'
    if not os.path.exists(points_file_path):
        os.makedirs(points_file_path)
    aux_video_file_name = Path(video_file_name)
    points_file_name = str(aux_video_file_name.stem) + '_points.csv'
    points_full_file_name = save_to_files + '/points/' + points_file_name

    symmetries_file_path = save_to_files + '/symmetries/'
    if not os.path.exists(symmetries_file_path):
        os.makedirs(symmetries_file_path)
    aux_video_file_name = Path(video_file_name)
    symmetries_file_name = str(aux_video_file_name.stem) + '_symmetry.csv'
    symmetries_full_file_name = symmetries_file_path + symmetries_file_name

    get_video_points(video_file_path, markup_file_path, points_full_file_name, predictor_file_path)
    get_video_symmetries(video_file_path, points_full_file_name, symmetries_full_file_name)


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
    project_folder =  Path().resolve()
    video_path = project_folder.joinpath('data/video')
    markup_path = project_folder.joinpath('data/markup.xlsx')
    write_path = project_folder.joinpath('data/processed')
    predictor_file_path = project_folder.joinpath('models/shape_predictor_68_face_landmarks.dat')

    video_path_list = get_list_of_files(video_path)

    for video_path in video_path_list:
        name = video_path.name.split('.')[0]
        write_path = project_folder.joinpath('data/processed/' + name)
        main_start(str(predictor_file_path), str(video_path), str(markup_path), str(write_path))
    
    # with open("paths.json", "r") as data_json:
    #     data_dict = json.load(data_json)
    #     for key in data_dict:
    #         # print(data_dict[key])


    #     video_file_path = 'F://PyCharm Community Edition 2022.1.3//projects//paresis_files//20180305_Трухановский.mp4'
    #     markup_file_path = 'F://PyCharm Community Edition 2022.1.3//projects//paresis_files//Разметка упражнений.xlsx'
    #     save_to_files = 'F://PyCharm Community Edition 2022.1.3//projects//paresis_files//'
    #     predictor_file_path = 'F:/PyCharm Community Edition 2022.1.3/projects/paresis_detection/models/shape_predictor_68_face_landmarks.dat'

    # if len(sys.argv) > 1:
    #     video_file_path = str(sys.argv[1])
    #     markup_file_path = str(sys.argv[2])
    #     save_to_files = str(sys.argv[3])
    #     predictor_file_path = str(sys.argv[4])

    # main_start(predictor_file_path, video_file_path, markup_file_path, save_to_files)
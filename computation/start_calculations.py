
import os
from typing import Callable
from pathlib import Path

from computation.get_video_points import get_video_points
from computation.get_video_symmetries import get_video_symmetries


def main_start(event, queue, predictor_file_path:str, video_file_path:str, markup_file_path:str, save_to_path:str):
    
    # Changing file paths type
    predictor_file_path = Path(predictor_file_path)
    video_file_path = Path(video_file_path)
    markup_file_path = Path(markup_file_path)
    save_to_path = Path(save_to_path)

    points_file_path = save_to_path/'points'
    if not points_file_path.exists():
        points_file_path.mkdir()
    points_file_name = str(video_file_path.stem) + '_points.csv'
    points_full_file_path = str(points_file_path/points_file_name)

    symmetries_file_path = save_to_path /'symmetries'
    if not os.path.exists(symmetries_file_path):
        os.makedirs(symmetries_file_path)
    symmetries_file_name = str(video_file_path.stem) + '_symmetry.csv'
    symmetries_full_file_path = str(symmetries_file_path/symmetries_file_name)


    video_file_path = str(video_file_path)
    markup_file_path = str(markup_file_path)
    predictor_file_path = str(predictor_file_path)
    
    get_video_points(event, queue, video_file_path, markup_file_path, points_full_file_path, predictor_file_path)
    get_video_symmetries(video_file_path, points_full_file_path, symmetries_full_file_path)


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
        'models/shape_predictor_68_face_landmarks.dat',
        'application/app_handlers/temp/20180125_Mordashov_1.mp4',
        'application/app_handlers/temp/markup.xlsx',
        'application/app_handlers/temp'
        )
    # project_folder =  Path().resolve()
    # video_path = project_folder.joinpath('data/video')
    # markup_path = project_folder.joinpath('data/markup.xlsx')
    # write_path = project_folder.joinpath('data/processed')
    # predictor_file_path = project_folder.joinpath('models/shape_predictor_68_face_landmarks.dat')

    # video_path_list = get_list_of_files(video_path)

    # for video_path in video_path_list:
    #     name = video_path.name.split('.')[0]
    #     write_path = project_folder.joinpath('data/processed/' + name)
    #     main_start(str(predictor_file_path), str(video_path), str(markup_path), str(write_path))
    
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
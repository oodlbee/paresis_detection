import os
import pandas as pd


def collect_folder_symmetries(symmetries_folder_path, folder_symmetries_full_file_name):
    folder_symmetries = pd.DataFrame()
    for _, _, files in os.walk(symmetries_folder_path):
        counter = 0
        for symmetries_file_name in files:
            file_name, file_extension = os.path.splitext(symmetries_file_name)
            if file_extension == '.csv':
                symmetries_full_file_name = os.path.join(symmetries_folder_path,
                                                         symmetries_file_name)
                video_symmetries = pd.read_csv(symmetries_full_file_name)
                if counter == 0:
                    folder_symmetries = video_symmetries
                else:
                    folder_symmetries = pd.concat([folder_symmetries, video_symmetries])

                counter += 1

    folder_symmetries.to_csv(path_or_buf=folder_symmetries_full_file_name, sep=',',
                             na_rep='NaN', index=False, decimal='.')

import imageio
import pandas as pd
from pathlib import Path

from get_video_points import get_video_points
from get_video_symmetries import get_video_symmetries

def main():
    # import of trained prediction model
    predictor_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection/models/'
    predictor_file_name = 'shape_predictor_68_face_landmarks.dat'
    predictor_full_file_name = predictor_file_path + predictor_file_name

    # import video
    video_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection_data/videos/'
    video_file_name = '20180305_Трухановский.mp4'
    video_full_file_name = video_file_path + video_file_name
    # return object which can be used to read data and metadata from file
    video = imageio.get_reader(video_full_file_name)

    # fills with new points ???
    points_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection_data/points/'
    aux_video_file_name = Path(video_file_name)
    points_file_name = str(aux_video_file_name.stem) + '_points.csv'
    points_full_file_name = points_file_path + points_file_name

    # symmetry file ???
    symmetries_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection_data/symmetries/'
    aux_video_file_name = Path(video_file_name)
    symmetries_file_name = str(aux_video_file_name.stem) + '_symmetry.csv'
    symmetries_full_file_name = symmetries_file_path + symmetries_file_name

    # timeline markup
    markup_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection_data/markup/'
    markup_file_name = 'Разметка упражнений.xlsx'
    markup_full_file_name = markup_file_path + markup_file_name
    markup = pd.read_excel(markup_full_file_name, sheet_name=0)

    get_video_points(video_full_file_name, markup_full_file_name, points_full_file_name, predictor_full_file_name)
    get_video_symmetries(video_full_file_name, points_full_file_name, symmetries_full_file_name)

if __name__ == "__main__":
    main()
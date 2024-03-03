import dlib
import imageio
import numpy as np
from pathlib import Path
import pandas as pd
from computation.utils import shape_to_row_array

def get_video_points(event, queue, video_full_file_name, markup_full_file_name, points_full_file_name, predictor_full_file_name):
    video_file_name = Path(video_full_file_name).stem
    markup = pd.read_excel(markup_full_file_name, sheet_name=0)
    markup = markup[markup['file_name'] == video_file_name].to_dict()

    video_reader = imageio.get_reader(video_full_file_name)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_full_file_name)

    exercises_dict = {
        'eyebrows_raising': [],
        'left_eye_squeezing': [],
        'right_eye_squeezing': [],
        'eyes_squeezing': [],
        'smile': [],
        'forced_smile': [],
        'cheeks_puffing': [],
        'lips_struggling': [],
        'articulation': [],
        'forced_articulation': []
    }
    # Stucture of dict: {exercise name: [begin frama num, end frame num], ...}

    for exercise in exercises_dict.keys():
        exercises_dict[exercise] = [markup[exercise + '_begin'][0], markup[exercise + '_end'][0]]
    
    video_points = []
    for frame_num, image in enumerate(video_reader):
        rects = detector(image, 1)

        print(frame_num)

        if len(rects) == 1:
            shape = predictor(image, rects[0])

            frame_validity = 'valid'
            row_array_points = shape_to_row_array(shape)

            frame_type = 'rest_state'
            for exercise, (begin, end) in exercises_dict.items():
                if begin <= frame_num < end:
                    frame_type = exercise
                    break
        else:
            frame_validity = 'damaged'
            frame_type = 'damaged_frame'
            row_array_points = [np.nan] * (68 * 2)

        frame_points = [frame_num, frame_validity, frame_type] + row_array_points
        video_points.append(frame_points)
        queue.put(frame_num / video_reader.get_length())
        event.set()
        
    video_points_column_names = ['frame_num', 'frame_validity', 'frame_type']
    for i in range(0, 68):
        str_point_num = str(i + 1)
        str_point_num = 'p_' + str_point_num.zfill(2)
        str_point_num_x = str_point_num + '_x'
        str_point_num_y = str_point_num + '_y'
        video_points_column_names.append(str_point_num_x)
        video_points_column_names.append(str_point_num_y)

    df_video_points = pd.DataFrame(data=video_points, columns=video_points_column_names)
    df_video_points = df_video_points.convert_dtypes()
    df_video_points.to_csv(path_or_buf=points_full_file_name, sep=',', na_rep='NaN', index=False, decimal='.')
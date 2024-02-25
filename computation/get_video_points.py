import dlib
import imageio
import numpy as np
import os
import pandas as pd
from computation.utils import shape_to_row_array

def get_video_points(execute_event, progress_update, video_full_file_name, markup_full_file_name, points_full_file_name, predictor_full_file_name):

    markup = pd.read_excel(markup_full_file_name, sheet_name=0)

    video = imageio.get_reader(video_full_file_name)
    video_file_name = os.path.basename(video_full_file_name)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_full_file_name)

    exercises_dict = {}
    # Stucture of dict: {exercise name: [begin frama num, end frame num], ...}

    # (01) Eyebrows raising
    exercises_dict['eyebrows_raising'] = [
        markup.loc[markup['file_name'] == video_file_name, 'eyebrows_raising_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'eyebrows_raising_end'].values[0]
    ]

    # (02) Left eye squeezing
    exercises_dict['left_eye_squeezing'] = [
        markup.loc[markup['file_name'] == video_file_name, 'left_eye_squeezing_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'left_eye_squeezing_end'].values[0]
    ]

    # (03) Right eye squeezing
    exercises_dict['right_eye_squeezing'] = [
        markup.loc[markup['file_name'] == video_file_name, 'right_eye_squeezing_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'right_eye_squeezing_end'].values[0]
    ]

    # (04) Left and right eyes squeezing
    exercises_dict['eyes_squeezing'] = [
        markup.loc[markup['file_name'] == video_file_name, 'eyes_squeezing_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'eyes_squeezing_end'].values[0]
    ]

    # (05) Smile
    exercises_dict['smile'] = [
        markup.loc[markup['file_name'] == video_file_name, 'smile_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'smile_end'].values[0]
    ]

    # (06) Forced smile
    exercises_dict['forced_smile'] = [
        markup.loc[markup['file_name'] == video_file_name, 'forced_smile_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'forced_smile_end'].values[0]
    ]

    # (07) Cheeks puffing
    exercises_dict['cheeks_puffing'] = [
        markup.loc[markup['file_name'] == video_file_name, 'cheeks_puffing_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'cheeks_puffing_end'].values[0]
    ]

    # (08) Lips struggling
    exercises_dict['lips_struggling'] = [
        markup.loc[markup['file_name'] == video_file_name, 'lips_struggling_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'lips_struggling_end'].values[0]
    ]

    # (09) Articulation
    exercises_dict['articulation'] = [
        markup.loc[markup['file_name'] == video_file_name, 'articulation_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'articulation_end'].values[0]
    ]

    # (10) Forced articulation
    exercises_dict['forced_articulation'] = [
        markup.loc[markup['file_name'] == video_file_name, 'forced_articulation_begin'].values[0],
        markup.loc[markup['file_name'] == video_file_name, 'forced_articulation_end'].values[0]
    ]
    
    video_points = []

    for frame_num in range(video.get_length()):
        if execute_event.is_set():
            break
        image = video.get_data(frame_num)
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
        progress_update(frame_num, video.get_length())

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

import dlib
import imageio
import numpy as np
import os
import pandas as pd

from utils import shape_to_row_array


def get_video_points(video_full_file_name, markup_full_file_name, points_full_file_name, predictor_full_file_name):

    markup = pd.read_excel(markup_full_file_name, sheet_name=0)


    video = imageio.get_reader(video_full_file_name)
    video_file_name = os.path.basename(video_full_file_name)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_full_file_name)

    # (01) Eyebrows raising
    eyebrows_raising_begin = markup.loc[markup['file_name'] == video_file_name, 'eyebrows_raising_begin'].values[0]
    eyebrows_raising_end = markup.loc[markup['file_name'] == video_file_name, 'eyebrows_raising_end'].values[0]

    # (02) Left eye squeezing
    left_eye_squeezing_begin = markup.loc[markup['file_name'] == video_file_name, 'left_eye_squeezing_begin'].values[0]
    left_eye_squeezing_end = markup.loc[markup['file_name'] == video_file_name, 'left_eye_squeezing_end'].values[0]

    # (03) Right eye squeezing
    right_eye_squeezing_begin = markup.loc[markup['file_name'] == video_file_name,
                                           'right_eye_squeezing_begin'].values[0]
    right_eye_squeezing_end = markup.loc[markup['file_name'] == video_file_name, 'right_eye_squeezing_end'].values[0]

    # (04) Left and right eyes squeezing
    eyes_squeezing_begin = markup.loc[markup['file_name'] == video_file_name, 'eyes_squeezing_begin'].values[0]
    eyes_squeezing_end = markup.loc[markup['file_name'] == video_file_name, 'eyes_squeezing_end'].values[0]

    # (05) Smile
    smile_begin = markup.loc[markup['file_name'] == video_file_name, 'smile_begin'].values[0]
    smile_end = markup.loc[markup['file_name'] == video_file_name, 'smile_end'].values[0]

    # (06) Forced smile
    forced_smile_begin = markup.loc[markup['file_name'] == video_file_name, 'forced_smile_begin'].values[0]
    forced_smile_end = markup.loc[markup['file_name'] == video_file_name, 'forced_smile_end'].values[0]

    # (07) Cheeks puffing
    cheeks_puffing_begin = markup.loc[markup['file_name'] == video_file_name, 'cheeks_puffing_begin'].values[0]
    cheeks_puffing_end = markup.loc[markup['file_name'] == video_file_name, 'cheeks_puffing_end'].values[0]

    # (08) Lips struggling
    lips_struggling_begin = markup.loc[markup['file_name'] == video_file_name, 'lips_struggling_begin'].values[0]
    lips_struggling_end = markup.loc[markup['file_name'] == video_file_name, 'lips_struggling_end'].values[0]

    # (09) Articulation
    articulation_begin = markup.loc[markup['file_name'] == video_file_name, 'articulation_begin'].values[0]
    articulation_end = markup.loc[markup['file_name'] == video_file_name, 'articulation_end'].values[0]

    # (10) Forced articulation
    forced_articulation_begin = markup.loc[markup['file_name'] == video_file_name,
                                           'forced_articulation_begin'].values[0]
    forced_articulation_end = markup.loc[markup['file_name'] == video_file_name, 'forced_articulation_end'].values[0]

    video_points = []

    for frame_num, _ in enumerate(video):
        print('frame_num is: ', frame_num)

        image = video.get_data(frame_num)
        rects = detector(image, 1)

        if len(rects) == 1:
            shape = predictor(image, rects[0])

            frame_validity = 'valid'
            row_array_points = shape_to_row_array(shape)

            if (eyebrows_raising_begin <= frame_num) and (frame_num < eyebrows_raising_end):
                frame_type = 'eyebrows_raising'
            elif (left_eye_squeezing_begin <= frame_num) and (frame_num < left_eye_squeezing_end):
                frame_type = 'left_eye_squeezing'
            elif (right_eye_squeezing_begin <= frame_num) and (frame_num < right_eye_squeezing_end):
                frame_type = 'right_eye_squeezing'
            elif (eyes_squeezing_begin <= frame_num) and (frame_num < eyes_squeezing_end):
                frame_type = 'eyes_squeezing'
            elif (smile_begin <= frame_num) and (frame_num < smile_end):
                frame_type = 'smile'
            elif (forced_smile_begin <= frame_num) and (frame_num < forced_smile_end):
                frame_type = 'forced_smile'
            elif (cheeks_puffing_begin <= frame_num) and (frame_num < cheeks_puffing_end):
                frame_type = 'cheeks_puffing'
            elif (lips_struggling_begin <= frame_num) and (frame_num < lips_struggling_end):
                frame_type = 'lips_struggling'
            elif (articulation_begin <= frame_num) and (frame_num < articulation_end):
                frame_type = 'articulation'
            elif (forced_articulation_begin <= frame_num) and (frame_num < forced_articulation_end):
                frame_type = 'forced_articulation'
            else:
                frame_type = 'rest_state'
        else:
            frame_validity = 'damaged'
            frame_type = 'damaged_frame'
            row_array_points = [np.nan] * (68 * 2)

        frame_points = [frame_num, frame_validity, frame_type] + row_array_points
        video_points.append(frame_points)

    # Generate column names for dataframe with points coordinates
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

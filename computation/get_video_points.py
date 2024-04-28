import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
from pathlib import Path
from mediapipe.python.solutions import face_mesh
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList


from computation.utils import shape_to_row_array
from computation import utils
from computation import constants


def calculate_distances(frame_type:str, result_dict:dict, image:np.array, model_results:NormalizedLandmarkList):
    # distances for forehead
    # left
    left_eye = utils.get_coords(model_results, image.shape[:2], constants.LEFT_EYE_POINTS)
    left_eyebrow = utils.get_coords(model_results, image.shape[:2], constants.LEFT_EYEBROW_POINTS)

    left_eye_center = utils.calculate_geom_center(left_eye)
    left_eyebrow_center = utils.calculate_geom_center(left_eyebrow)

    left_forehead_distance = utils.calculate_euclidean_norm(left_eye_center, left_eyebrow_center)

    # right
    right_eye = utils.get_coords(model_results, image.shape[:2], constants.RIGHT_EYE_POINTSR)
    right_eyebrow = utils.get_coords(model_results, image.shape[:2], constants.RIGHT_EYEBROW_POINTS)

    right_eye_center = utils.calculate_geom_center(right_eye)
    right_eyebrow_center = utils.calculate_geom_center(right_eyebrow)

    right_forehead_distance = utils.calculate_euclidean_norm(right_eye_center, right_eyebrow_center)

    # distances for lips
    # left



    if frame_type == 'rest':
        result_dict[frame_type]['forehead']['left'] += left_forehead_distance
        result_dict[frame_type]['forehead']['right'] += right_forehead_distance
    else:
        result_dict[frame_type]['forehead']['left']  = max(left_forehead_distance, result_dict[frame_type])
        result_dict[frame_type]['forehead']['right']  = max(right_forehead_distance, result_dict[frame_type])




def get_video_points(event, queue, video_full_file_name, markup_full_file_name, points_full_file_name, predictor_full_file_name):
    video_file_name = Path(video_full_file_name).stem
    markup = pd.read_excel(markup_full_file_name, sheet_name=0)
    markup = markup[markup['file_name'] == video_file_name].to_dict()

    exercises_dict = constants.EXCERCISE_DICT
    # Stucture of dict: {exercise name: [begin frama num, end frame num], ...}

    for exercise in exercises_dict.keys():
        exercises_dict[exercise] = [markup[exercise + '_begin'][0], markup[exercise + '_end'][0]]


    distances_dict = constants.DISTANCES_EMPTY_DICT  

    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=False,
                            refine_landmarks=True,
                            max_num_faces=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.8) as face_mesh_model:

        cap = cv2.VideoCapture(video_file_name)
        frame_num = 0
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            frame_type = 'rest'
            for exercise, (begin, end) in exercises_dict.items():
                if begin <= frame_num < end:
                    frame_type = exercise
                    break

            model_results = face_mesh_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).multi_face_landmarks[0]



            # print(get_coords(model_results,  frame.shape[0: 2], ))

            frame_num += 1
            

        else:


        cap.release()
        cv2.destroyAllWindows()


    # video_points = []
    # for frame_num, image in enumerate(video_reader):
    #     rects = detector(image, 1)

    #     print(frame_num)

    #     if len(rects) == 1:
    #         shape = predictor(image, rects[0])

    #         frame_validity = 'valid'
    #         row_array_points = shape_to_row_array(shape)

    #         frame_type = 'rest_state'
    #         for exercise, (begin, end) in exercises_dict.items():
    #             if begin <= frame_num < end:
    #                 frame_type = exercise
    #                 break
    #     else:
    #         frame_validity = 'damaged'
    #         frame_type = 'damaged_frame'
    #         row_array_points = [np.nan] * (68 * 2)

    #     frame_points = [frame_num, frame_validity, frame_type] + row_array_points
    #     video_points.append(frame_points)
    #     queue.put(frame_num / video_reader.get_length())
    #     event.set()
        
    # video_points_column_names = ['frame_num', 'frame_validity', 'frame_type']
    # for i in range(0, 68):
    #     str_point_num = str(i + 1)
    #     str_point_num = 'p_' + str_point_num.zfill(2)
    #     str_point_num_x = str_point_num + '_x'
    #     str_point_num_y = str_point_num + '_y'
    #     video_points_column_names.append(str_point_num_x)
    #     video_points_column_names.append(str_point_num_y)

    # df_video_points = pd.DataFrame(data=video_points, columns=video_points_column_names)
    # df_video_points = df_video_points.convert_dtypes()
    # df_video_points.to_csv(path_or_buf=points_full_file_name, sep=',', na_rep='NaN', index=False, decimal='.')
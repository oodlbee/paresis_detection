import cv2
import json 
import pandas as pd
import numpy as np
import mediapipe as mp
from pathlib import Path
from computation.calculate import calculate_distances, calculate_symmetries
from computation import constants

def get_video_symmetries(event, queue, video_full_file_name, markup_full_file_name, save_to_path):
    video_file_name = Path(video_full_file_name).stem
    markup = pd.read_excel(markup_full_file_name, sheet_name=0)
    markup = markup[markup['file_name'] == video_file_name].to_dict()

    exercises_dict = constants.EXCERCISE_DICT
    # Stucture of dict: {exercise name: [begin frama num, end frame num], ...}

    for exercise in exercises_dict.keys():
        exercises_dict[exercise] = [markup[exercise + '_begin'][0], markup[exercise + '_end'][0]]

    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(static_image_mode=False,
                            refine_landmarks=True,
                            max_num_faces=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.8) as face_mesh_model:

        cap = cv2.VideoCapture(str(video_full_file_name))
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frame_num == 0:
            print('ERRROR')
            return
       

        distances = constants.DISTANCES_EMPTY_DICT
        frame_num = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame_num += 1

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            frame_type = 'empty_frame'
            for exercise, (begin, end) in exercises_dict.items():
                if begin <= frame_num < end:
                    frame_type = exercise
                    break

            if frame_type == 'empty_frame':
                continue
            frame.flags.writeable = False
            model_results = face_mesh_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).multi_face_landmarks
            frame.flags.writeable = True
            if not model_results:
                print("no face detected {}")
                continue

            model_results = model_results[0]
            distances = calculate_distances(frame_type, distances, frame, model_results)

            queue.put(frame_num / total_frame_num)
            event.set()

        cap.release()

    symmetries, distances = calculate_symmetries(distances)

    with open(save_to_path / "distances.json", "w") as out_file: 
        json.dump(distances, out_file)

    with open(save_to_path / "symmetries.json", "w") as out_file: 
        json.dump(symmetries, out_file)
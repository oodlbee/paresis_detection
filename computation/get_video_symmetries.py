import cv2
import json 
import logging
import constants
import pandas as pd
import mediapipe as mp
from utils import timed_log
from copy import deepcopy
from calculate import calculate_distances, calculate_symmetries

logger = logging.getLogger('comp_logger')



@timed_log(logger)
def get_video_symmetries(video_full_file_name, markup_full_file_name, save_to_path, event=None, queue=None):
    video_file_name = video_full_file_name.stem
    markup = pd.read_excel(markup_full_file_name, sheet_name=0)
    markup = markup[markup['file_name'] == video_file_name].to_dict()

    exercises_dict = deepcopy(constants.EXCERCISE_DICT)
    # Stucture of dict: {exercise name: [begin frama num, end frame num], ...}

    for exercise in exercises_dict.keys():
        exercises_dict[exercise] = [markup[exercise + '_begin'][0], markup[exercise + '_end'][0]]

    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(static_image_mode=False,
                            refine_landmarks=True,
                            max_num_faces=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.8) as face_mesh_model:
        logger.debug('Model initializied successfully')

        cap = cv2.VideoCapture(str(video_full_file_name))
        total_frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frame_num == 0:
            logger.error('There is 0 frames in videofile')
            raise Exception('Empty videofile')
        
        logger.debug('Cv2 cap initializied successfully')
        
        distances = deepcopy(constants.DISTANCES_EMPTY_DICT)
        frame_num = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame_num += 1

            if not ret:
                logger.info("Can't receive frame or End of stream")
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
                logger.warning("No face detected. Continue...")
                continue
   
            model_results = model_results[0]
            distances = calculate_distances(frame_type, distances, frame, model_results)

            if (event != None) and (queue != None) and (frame_num % 10 == 0):
                queue.put(frame_num / total_frame_num)
                event.set()

        cap.release()
        logger.debug("Cv2 cap released")

    symmetries, distances = calculate_symmetries(distances)

    with open(save_to_path / "distances.json", "w") as out_file: 
        json.dump(distances, out_file)
    logger.debug(f"Distances saved on {out_file}")

    with open(save_to_path / "symmetries.json", "w") as out_file: 
        json.dump(symmetries, out_file)
    logger.debug(f"Symmetries saved on {out_file}")
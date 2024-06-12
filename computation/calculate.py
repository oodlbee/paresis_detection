import constants
import numpy as np
import logging
import compute_utils as utils
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

logger = logging.getLogger('comp_logger')


def calculate_distances(frame_type: str, distances: dict, image: np.array, model_results: NormalizedLandmarkList):
    size = image.shape[0: 2]

    left_eye_coords = utils.get_3d_coords(model_results,  size, constants.LEFT_EYE_POINTS)
    right_eye_coords = utils.get_3d_coords(model_results,  size, constants.RIGHT_EYE_POINTS)
    # left_eyebrow_coords = utils.get_3d_coords(model_results,  size, constants.LEFT_EYEBROW_POINTS)
    # right_eyebrow_coords = utils.get_3d_coords(model_results,  size, constants.RIGHT_EYEBROW_POINTS)

    left_eyebrow_coords = utils.get_3d_coords(model_results,  size, constants.LEFT_TOP_EYEBROW_POINTS)
    right_eyebrow_coords = utils.get_3d_coords(model_results,  size, constants.RIGHT_TOP_EYEBROW_POINTS)

    left_eye_center = utils.calculate_geom_center(left_eye_coords)
    right_eye_center = utils.calculate_geom_center(right_eye_coords)
    left_eyebrow_center = utils.calculate_geom_center(left_eyebrow_coords)
    right_eyebrow_center = utils.calculate_geom_center(right_eyebrow_coords)

    # normalize_dist = utils.calculate_euclidean_norm(left_eye_center, right_eye_center)

    left_forehead_dist = utils.calculate_euclidean_norm(left_eye_center, left_eyebrow_center)
    right_forehead_dist = utils.calculate_euclidean_norm(right_eye_center, right_eyebrow_center)
    # # normalize
    # left_forehead_dist = utils.calculate_euclidean_norm(left_eye_center, left_eyebrow_center) / normalize_dist
    # right_forehead_dist = utils.calculate_euclidean_norm(right_eye_center, right_eyebrow_center) / normalize_dist



    # mouth
    mouth_coords = utils.get_3d_coords(model_results,  size, constants.LIPS_POINTS)
    left_mouth_corner = utils.get_3d_coords(model_results,  size, constants.LEFT_LIP_CORNER)
    right_mouth_corner = utils.get_3d_coords(model_results,  size, constants.RIGHT_LIP_CORNER)

    mouth_center = utils.calculate_geom_center(mouth_coords)
    left_mouth_dist = utils.calculate_euclidean_norm(left_mouth_corner, mouth_center)
    right_mouth_dist = utils.calculate_euclidean_norm(right_mouth_corner, mouth_center)

    # left_mouth_dist = utils.calculate_euclidean_norm(left_mouth_corner, mouth_center) / normalize_dist
    # right_mouth_dist = utils.calculate_euclidean_norm(right_mouth_corner, mouth_center) / normalize_dist


    # image = cv2.circle(image, mouth_center.astype(int), 3, color=(0, 0, 255))

    # image = cv2.circle(image, left_eye_center.astype(int), 3, color=(0, 0, 255))
    # image = cv2.circle(image, right_eye_center.astype(int), 3, color=(0, 0, 255))

    # image = cv2.circle(image, left_eyebrow_center.astype(int), 3, color=(0, 0, 255))
    # image = cv2.circle(image, right_eyebrow_center.astype(int), 3, color=(0, 0, 255))

    # image = cv2.circle(image, left_mouth_corner[0].astype(int), 3, color=(0, 0, 255))
    # image = cv2.circle(image, right_mouth_corner[0].astype(int), 3, color=(0, 0, 255))

    # cv2.imshow("frame", image)
    # if cv2.waitKey(1) == ord("q"):
    #     cv2.destroyAllWindows()
    #     return 

    if frame_type == 'rest':
        distances[frame_type]['forehead']['left'] += left_forehead_dist
        distances[frame_type]['forehead']['right'] += right_forehead_dist
        distances[frame_type]['mouth']['left'] += left_mouth_dist
        distances[frame_type]['mouth']['right'] += right_mouth_dist
        distances[frame_type]['count_frames'] += 1
    else:
        distances[frame_type]['forehead']['left'].append(left_forehead_dist)
        distances[frame_type]['forehead']['right'].append(right_forehead_dist)
        distances[frame_type]['mouth']['left'].append(left_mouth_dist)
        distances[frame_type]['mouth']['right'].append(right_mouth_dist)
        distances[frame_type]['count_frames'] += 1
    
    return distances


def calculate_symmetries(distances):
    exersice_symmetries = constants.SYMMETRIES_DICT

    # calculate mean for rest
    distances['rest']['forehead']['left'] /= distances['rest']['count_frames']
    distances['rest']['forehead']['right'] /= distances['rest']['count_frames']
    distances['rest']['mouth']['left'] /= distances['rest']['count_frames']
    distances['rest']['mouth']['right'] /= distances['rest']['count_frames']

    distances['rest']['forehead']['left'] = distances['rest']['forehead']['left']
    distances['rest']['forehead']['right'] = distances['rest']['forehead']['right']
    distances['rest']['mouth']['left'] = distances['rest']['mouth']['left']
    distances['rest']['mouth']['right'] = distances['rest']['mouth']['right']

    for exercise in exersice_symmetries.keys():
        if exercise == 'rest':
            continue

        exersice_symmetries[exercise] = {}
        if distances[exercise]['forehead']['left'] == []:
            continue

        left_bias_forehead = np.max(np.abs(np.array(distances[exercise]['forehead']['left']) - distances['rest']['forehead']['left']))
        right_bias_forehead = np.max(np.abs(np.array(distances[exercise]['forehead']['right']) - distances['rest']['forehead']['right']))

        if (left_bias_forehead == 0) or (right_bias_forehead == 0):
            forehead_symmetry = 0
        else:
            forehead_symmetry = left_bias_forehead / right_bias_forehead if right_bias_forehead > left_bias_forehead else right_bias_forehead / left_bias_forehead

        left_bias_mouth= np.max(np.abs(np.array(distances[exercise]['mouth']['left']) - distances['rest']['mouth']['left']))
        right_bias_mouth = np.max(np.abs(np.array(distances[exercise]['mouth']['right']) - distances['rest']['mouth']['right']))

        if (left_bias_mouth == 0) or (right_bias_mouth == 0):
            mouth_symmetry = 0
        else:
            mouth_symmetry = left_bias_mouth / right_bias_mouth if right_bias_mouth > left_bias_mouth else right_bias_mouth / left_bias_mouth

        exersice_symmetries[exercise]['forehead'] = forehead_symmetry
        exersice_symmetries[exercise]['mouth'] = mouth_symmetry
        
    return exersice_symmetries, distances



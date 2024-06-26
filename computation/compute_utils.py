import numpy as np
from typing import Tuple
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList


def get_coords(landmarks: NormalizedLandmarkList, init_image_shape: Tuple[int, int], points: list) -> np.array:
    image_hight, image_width = init_image_shape
    return np.array([(landmarks.landmark[idx].x * image_width, landmarks.landmark[idx].y * image_hight) for idx in  points]).astype(int)

def get_3d_coords(landmarks: NormalizedLandmarkList, init_image_shape: Tuple[int, int], points: list) -> np.array:
    image_hight, image_width = init_image_shape
    return np.array([
        (landmarks.landmark[idx].x * image_width, landmarks.landmark[idx].y * image_width, landmarks.landmark[idx].z * image_hight) for idx in  points]
        ).astype(int)

def calculate_geom_center(point_group: np.array):
    return np.mean(point_group, axis=0)


def calculate_euclidean_norm(point_first: np.array, point_second: np.array):
    return np.linalg.norm(point_first - point_second)


def shape_to_np_array(lib_shape, data_type="int"):
    # Initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=data_type)
    # Loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (lib_shape.part(i).x, lib_shape.part(i).y)
    # Return the list of (x, y)-coordinates
    return coords


def shape_to_row_array(lib_shape):
    # Initialize an empty list of coordinates
    coords = []
    for i in range(0, 68):
        coords.append(int(lib_shape.part(i).x))
        coords.append(int(lib_shape.part(i).y))
    # Return the row vector of coordinates (x-coordinate then y coordinate,
    # then next x-coordinate and so on...
    return coords


def row_array_to_np_array(row_array, data_type="int"):
    # Initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=data_type)
    # Loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (row_array[i * 2], row_array[i * 2 + 1])
    # Return the list of (x, y)-coordinates
    return coords

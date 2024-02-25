import numpy as np
import pandas as pd

from computation.get_frame_distances import get_frame_distances
from computation.utils import row_array_to_np_array


def get_segment_distances(points_full_file_name, frame_type):

    df_video_points = pd.read_csv(filepath_or_buffer=points_full_file_name)
    df_video_points = df_video_points.loc[df_video_points['frame_type'] == frame_type]
    segment_frames_qty = df_video_points.shape[0]

    if frame_type != 'damaged_frame':

        segment_right_eyebrow_dist = []
        segment_left_eyebrow_dist = []
        segment_mouth_right_corner_dist = []
        segment_mouth_left_corner_dist = []

        for i, row in df_video_points.iterrows():
            # Skip first three columns (frame_num, frame_validity, frame_type)
            points = row_array_to_np_array(row.values[3:])

            right_eyebrow_dist, left_eyebrow_dist, \
                mouth_right_corner_dist, mouth_left_corner_dist = get_frame_distances(points)

            segment_right_eyebrow_dist.append(right_eyebrow_dist)
            segment_left_eyebrow_dist.append(left_eyebrow_dist)
            segment_mouth_right_corner_dist.append(mouth_right_corner_dist)
            segment_mouth_left_corner_dist.append(mouth_left_corner_dist)
    else:
        segment_right_eyebrow_dist = np.nan
        segment_left_eyebrow_dist = np.nan
        segment_mouth_right_corner_dist = np.nan
        segment_mouth_left_corner_dist = np.nan

    return (segment_right_eyebrow_dist, segment_left_eyebrow_dist,
            segment_mouth_right_corner_dist, segment_mouth_left_corner_dist,
            segment_frames_qty)

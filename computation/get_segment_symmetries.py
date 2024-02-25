import numpy as np


def get_segment_symmetries(segment_right_eyebrow_dist, segment_left_eyebrow_dist,
                           segment_mouth_right_corner_dist, segment_mouth_left_corner_dist,
                           rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
                           rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist):

    if (len(segment_right_eyebrow_dist) == 0) or (len(segment_left_eyebrow_dist) == 0) or \
            (len(segment_mouth_right_corner_dist) == 0) or (len(segment_mouth_left_corner_dist) == 0) or \
            (len(rest_state_right_eyebrow_dist) == 0) or (len(rest_state_left_eyebrow_dist) == 0) or \
            (len(rest_state_mouth_right_corner_dist) == 0) or (len(rest_state_mouth_left_corner_dist) == 0):
        forehead_symmetry = np.nan
        mouth_symmetry = np.nan
        return forehead_symmetry, mouth_symmetry

    else:
        segment_right_eyebrow_shift = max(
            np.abs(np.array(segment_right_eyebrow_dist) - np.mean(rest_state_right_eyebrow_dist)))
        segment_left_eyebrow_shift = max(
            np.abs(np.array(segment_left_eyebrow_dist) - np.mean(rest_state_left_eyebrow_dist)))
        segment_mouth_right_corner_shift = max(
            np.abs(np.array(segment_mouth_right_corner_dist) - np.mean(rest_state_mouth_right_corner_dist)))
        segment_mouth_left_corner_shift = max(
            np.abs(np.array(segment_mouth_left_corner_dist) - np.mean(rest_state_mouth_left_corner_dist)))

        # Forehead symmetry calculation
        if (segment_right_eyebrow_shift > segment_left_eyebrow_shift) \
                and (segment_right_eyebrow_shift != 0):
            forehead_symmetry = segment_left_eyebrow_shift / segment_right_eyebrow_shift
        elif (segment_right_eyebrow_shift < segment_left_eyebrow_shift) \
                and (segment_left_eyebrow_shift != 0):
            forehead_symmetry = segment_right_eyebrow_shift / segment_left_eyebrow_shift
        else:
            forehead_symmetry = np.nan

        # Mouth symmetry calculation
        if (segment_mouth_right_corner_shift > segment_mouth_left_corner_shift) \
                and (segment_mouth_right_corner_shift != 0):
            mouth_symmetry = segment_mouth_left_corner_shift / segment_mouth_right_corner_shift
        elif (segment_mouth_right_corner_shift < segment_mouth_left_corner_shift) \
                and (segment_mouth_left_corner_shift != 0):
            mouth_symmetry = segment_mouth_right_corner_shift / segment_mouth_left_corner_shift
        else:
            mouth_symmetry = np.nan

        if not np.isnan(forehead_symmetry):
            forehead_symmetry = round(forehead_symmetry, 3)

        if not np.isnan(mouth_symmetry):
            mouth_symmetry = round(mouth_symmetry, 3)

        return forehead_symmetry, mouth_symmetry

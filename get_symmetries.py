import numpy as np


def get_symmetries(exercise_right_eyebrow_dist, exercise_left_eyebrow_dist,
                   exercise_mouth_right_corner_dist, exercise_mouth_left_corner_dist,
                   rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
                   rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist):

    if (len(exercise_right_eyebrow_dist) == 0) or (len(exercise_left_eyebrow_dist) == 0) or \
            (len(exercise_mouth_right_corner_dist) == 0) or (len(exercise_mouth_left_corner_dist) == 0) or \
            (len(rest_state_right_eyebrow_dist) == 0) or (len(rest_state_left_eyebrow_dist) == 0) or \
            (len(rest_state_mouth_right_corner_dist) == 0) or (len(rest_state_mouth_left_corner_dist) == 0):
        forehead_symmetry = np.nan
        mouth_symmetry = np.nan
        return forehead_symmetry, mouth_symmetry

    else:
        exercise_right_eyebrow_shift = max(
            np.abs(np.array(exercise_right_eyebrow_dist) - np.mean(rest_state_right_eyebrow_dist)))
        exercise_left_eyebrow_shift = max(
            np.abs(np.array(exercise_left_eyebrow_dist) - np.mean(rest_state_left_eyebrow_dist)))
        exercise_mouth_right_corner_shift = max(
            np.abs(np.array(exercise_mouth_right_corner_dist) - np.mean(rest_state_mouth_right_corner_dist)))
        exercise_mouth_left_corner_shift = max(
            np.abs(np.array(exercise_mouth_left_corner_dist) - np.mean(rest_state_mouth_left_corner_dist)))

        # Forehead symmetry calculation
        if (exercise_right_eyebrow_shift > exercise_left_eyebrow_shift) \
                and (exercise_right_eyebrow_shift != 0):
            forehead_symmetry = exercise_left_eyebrow_shift / exercise_right_eyebrow_shift
        elif (exercise_right_eyebrow_shift < exercise_left_eyebrow_shift) \
                and (exercise_left_eyebrow_shift != 0):
            forehead_symmetry = exercise_right_eyebrow_shift / exercise_left_eyebrow_shift
        else:
            forehead_symmetry = np.nan

        # Mouth symmetry calculation
        if (exercise_mouth_right_corner_shift > exercise_mouth_left_corner_shift) \
                and (exercise_mouth_right_corner_shift != 0):
            mouth_symmetry = exercise_mouth_left_corner_shift / exercise_mouth_right_corner_shift
        elif (exercise_mouth_right_corner_shift < exercise_mouth_left_corner_shift) \
                and (exercise_mouth_left_corner_shift != 0):
            mouth_symmetry = exercise_mouth_right_corner_shift / exercise_mouth_left_corner_shift
        else:
            mouth_symmetry = np.nan

        if not np.isnan(forehead_symmetry):
            forehead_symmetry = round(forehead_symmetry, 3)

        if not np.isnan(mouth_symmetry):
            mouth_symmetry = round(mouth_symmetry, 3)

        return forehead_symmetry, mouth_symmetry

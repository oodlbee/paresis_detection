import numpy as np
import os
import pandas as pd

from get_segment_distances import get_segment_distances
from get_segment_symmetries import get_segment_symmetries


def get_video_symmetries(video_full_file_name, points_full_file_name, symmetries_full_file_name):
    video_file_name = os.path.basename(video_full_file_name)

    # (01) Eyebrows raising
    (eyebrows_raising_right_eyebrow_dist, eyebrows_raising_left_eyebrow_dist,
     eyebrows_raising_mouth_right_corner_dist, eyebrows_raising_mouth_left_corner_dist,
     eyebrows_raising_frames_qty) = get_segment_distances(points_full_file_name, 'eyebrows_raising')

    # (02) Left eye squeezing
    (left_eye_squeezing_right_eyebrow_dist, left_eye_squeezing_left_eyebrow_dist,
     left_eye_squeezing_mouth_right_corner_dist, left_eye_squeezing_mouth_left_corner_dist,
     left_eye_squeezing_frames_qty) = get_segment_distances(points_full_file_name, 'left_eye_squeezing')

    # (03) Right eye squeezing
    (right_eye_squeezing_right_eyebrow_dist, right_eye_squeezing_left_eyebrow_dist,
     right_eye_squeezing_mouth_right_corner_dist, right_eye_squeezing_mouth_left_corner_dist,
     right_eye_squeezing_frames_qty) = get_segment_distances(points_full_file_name, 'right_eye_squeezing')

    # (04) Left and right eyes squeezing
    (eyes_squeezing_right_eyebrow_dist, eyes_squeezing_left_eyebrow_dist,
     eyes_squeezing_mouth_right_corner_dist, eyes_squeezing_mouth_left_corner_dist,
     eyes_squeezing_frames_qty) = get_segment_distances(points_full_file_name, 'eyes_squeezing')

    # (05) Smile
    (smile_right_eyebrow_dist, smile_left_eyebrow_dist,
     smile_mouth_right_corner_dist, smile_mouth_left_corner_dist,
     smile_frames_qty) = get_segment_distances(points_full_file_name, 'smile')

    # (06) Forced smile
    (forced_smile_right_eyebrow_dist, forced_smile_left_eyebrow_dist,
     forced_smile_mouth_right_corner_dist, forced_smile_mouth_left_corner_dist,
     forced_smile_frames_qty) = get_segment_distances(points_full_file_name, 'forced_smile')

    # (07) Cheeks puffing
    (cheeks_puffing_right_eyebrow_dist, cheeks_puffing_left_eyebrow_dist,
     cheeks_puffing_mouth_right_corner_dist, cheeks_puffing_mouth_left_corner_dist,
     cheeks_puffing_frames_qty) = get_segment_distances(points_full_file_name, 'cheeks_puffing')

    # (08) Lips struggling
    (lips_struggling_right_eyebrow_dist, lips_struggling_left_eyebrow_dist,
     lips_struggling_mouth_right_corner_dist, lips_struggling_mouth_left_corner_dist,
     lips_struggling_frames_qty) = get_segment_distances(points_full_file_name, 'lips_struggling')

    # (09) Articulation
    (articulation_right_eyebrow_dist, articulation_left_eyebrow_dist,
     articulation_mouth_right_corner_dist, articulation_mouth_left_corner_dist,
     articulation_frames_qty) = get_segment_distances(points_full_file_name, 'articulation')

    # (10) Forced articulation
    (forced_articulation_right_eyebrow_dist, forced_articulation_left_eyebrow_dist,
     forced_articulation_mouth_right_corner_dist, forced_articulation_mouth_left_corner_dist,
     forced_articulation_frames_qty) = get_segment_distances(points_full_file_name, 'forced_articulation')

    # (11) Rest state
    (rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
     rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist,
     rest_state_frames_qty) = get_segment_distances(points_full_file_name, 'rest_state')

    # (12) Damaged frames
    (_, _, _, _, damaged_frames_qty) = get_segment_distances(points_full_file_name, 'damaged_frame')

    total_frames_qty = (eyebrows_raising_frames_qty + left_eye_squeezing_frames_qty +
                        right_eye_squeezing_frames_qty + eyes_squeezing_frames_qty +
                        smile_frames_qty + forced_smile_frames_qty +
                        cheeks_puffing_frames_qty + lips_struggling_frames_qty +
                        articulation_frames_qty + forced_articulation_frames_qty +
                        rest_state_frames_qty + damaged_frames_qty)

    # (01) Eyebrows raising
    eyebrows_raising_forehead_symmetry, eyebrows_raising_mouth_symmetry = get_segment_symmetries(
        eyebrows_raising_right_eyebrow_dist, eyebrows_raising_left_eyebrow_dist,
        eyebrows_raising_mouth_right_corner_dist, eyebrows_raising_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (02) Left eye squeezing
    left_eye_squeezing_forehead_symmetry, left_eye_squeezing_mouth_symmetry = get_segment_symmetries(
        left_eye_squeezing_right_eyebrow_dist, left_eye_squeezing_left_eyebrow_dist,
        left_eye_squeezing_mouth_right_corner_dist, left_eye_squeezing_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (03) Right eye squeezing
    right_eye_squeezing_forehead_symmetry, right_eye_squeezing_mouth_symmetry = get_segment_symmetries(
        right_eye_squeezing_right_eyebrow_dist, right_eye_squeezing_left_eyebrow_dist,
        right_eye_squeezing_mouth_right_corner_dist, right_eye_squeezing_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (04) Left and right eyes squeezing
    eyes_squeezing_forehead_symmetry, eyes_squeezing_mouth_symmetry = get_segment_symmetries(
        eyes_squeezing_right_eyebrow_dist, eyes_squeezing_left_eyebrow_dist,
        eyes_squeezing_mouth_right_corner_dist, eyes_squeezing_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (05) Smile
    smile_forehead_symmetry, smile_mouth_symmetry = get_segment_symmetries(
        smile_right_eyebrow_dist, smile_left_eyebrow_dist,
        smile_mouth_right_corner_dist, smile_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (06) Forced smile
    forced_smile_forehead_symmetry, forced_smile_mouth_symmetry = get_segment_symmetries(
        forced_smile_right_eyebrow_dist, forced_smile_left_eyebrow_dist,
        forced_smile_mouth_right_corner_dist, forced_smile_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (07) Cheeks puffing
    cheeks_puffing_forehead_symmetry, cheeks_puffing_mouth_symmetry = get_segment_symmetries(
        cheeks_puffing_right_eyebrow_dist, cheeks_puffing_left_eyebrow_dist,
        cheeks_puffing_mouth_right_corner_dist, cheeks_puffing_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (08) Lips struggling
    lips_struggling_forehead_symmetry, lips_struggling_mouth_symmetry = get_segment_symmetries(
        lips_struggling_right_eyebrow_dist, lips_struggling_left_eyebrow_dist,
        lips_struggling_mouth_right_corner_dist, lips_struggling_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (09) Articulation
    articulation_forehead_symmetry, articulation_mouth_symmetry = get_segment_symmetries(
        articulation_right_eyebrow_dist, articulation_left_eyebrow_dist,
        articulation_mouth_right_corner_dist, articulation_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    # (10) Forced articulation
    forced_articulation_forehead_symmetry, forced_articulation_mouth_symmetry = get_segment_symmetries(
        forced_articulation_right_eyebrow_dist, forced_articulation_left_eyebrow_dist,
        forced_articulation_mouth_right_corner_dist, forced_articulation_mouth_left_corner_dist,
        rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
        rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
    )

    print('eyebrows_raising_frames_qty is: ', eyebrows_raising_frames_qty)
    print('left_eye_squeezing_frames_qty is: ', left_eye_squeezing_frames_qty)
    print('right_eye_squeezing_frames_qty is: ', right_eye_squeezing_frames_qty)
    print('eyes_squeezing_frames_qty is: ', eyes_squeezing_frames_qty)
    print('smile_frames_qty is: ', smile_frames_qty)
    print('forced_smile_frames_qty is: ', forced_smile_frames_qty)
    print('cheeks_puffing_frames_qty is: ', cheeks_puffing_frames_qty)
    print('lips_struggling_frames_qty is: ', lips_struggling_frames_qty)
    print('articulation_frames_qty is: ', articulation_frames_qty)
    print('forced_articulation_frames_qty is: ', forced_articulation_frames_qty)
    print('rest_state_frames_qty is: ', rest_state_frames_qty)
    print('damaged_frames_qty is: ', damaged_frames_qty)
    print('total_frames_qty is: ', total_frames_qty)

    df_symmetries = pd.DataFrame()

    df_symmetries['file_name'] = [video_file_name]

    # (01) Eyebrows raising
    df_symmetries['eyebrows_raising_forehead_symmetry'] = np.array([eyebrows_raising_forehead_symmetry])
    df_symmetries['eyebrows_raising_mouth_symmetry'] = np.array([eyebrows_raising_mouth_symmetry])
    df_symmetries['eyebrows_raising_frames_qty'] = np.array([eyebrows_raising_frames_qty])

    # (02) Left eye squeezing
    df_symmetries['left_eye_squeezing_forehead_symmetry'] = np.array([left_eye_squeezing_forehead_symmetry])
    df_symmetries['left_eye_squeezing_mouth_symmetry'] = np.array([left_eye_squeezing_mouth_symmetry])
    df_symmetries['left_eye_squeezing_frames_qty'] = np.array([left_eye_squeezing_frames_qty])

    # (03) Right eye squeezing
    df_symmetries['right_eye_squeezing_forehead_symmetry'] = np.array([right_eye_squeezing_forehead_symmetry])
    df_symmetries['right_eye_squeezing_mouth_symmetry'] = np.array([right_eye_squeezing_mouth_symmetry])
    df_symmetries['right_eye_squeezing_frames_qty'] = np.array([right_eye_squeezing_frames_qty])

    # (04) Left and right eyes squeezing
    df_symmetries['eyes_squeezing_forehead_symmetry'] = np.array([eyes_squeezing_forehead_symmetry])
    df_symmetries['eyes_squeezing_mouth_symmetry'] = np.array([eyes_squeezing_mouth_symmetry])
    df_symmetries['eyes_squeezing_frames_qty'] = np.array([eyes_squeezing_frames_qty])

    # (05) Smile
    df_symmetries['smile_forehead_symmetry'] = np.array([smile_forehead_symmetry])
    df_symmetries['smile_mouth_symmetry'] = np.array([smile_mouth_symmetry])
    df_symmetries['smile_frames_qty'] = np.array([smile_frames_qty])

    # (06) Forced smile
    df_symmetries['forced_smile_forehead_symmetry'] = np.array([forced_smile_forehead_symmetry])
    df_symmetries['forced_smile_mouth_symmetry'] = np.array([forced_smile_mouth_symmetry])
    df_symmetries['forced_smile_frames_qty'] = np.array([forced_smile_frames_qty])

    # (07) Cheeks puffing
    df_symmetries['cheeks_puffing_forehead_symmetry'] = np.array([cheeks_puffing_forehead_symmetry])
    df_symmetries['cheeks_puffing_mouth_symmetry'] = np.array([cheeks_puffing_mouth_symmetry])
    df_symmetries['cheeks_puffing_frames_qty'] = np.array([cheeks_puffing_frames_qty])

    # (08) Lips struggling
    df_symmetries['lips_struggling_forehead_symmetry'] = np.array([lips_struggling_forehead_symmetry])
    df_symmetries['lips_struggling_mouth_symmetry'] = np.array([lips_struggling_mouth_symmetry])
    df_symmetries['lips_struggling_frames_qty'] = np.array([lips_struggling_frames_qty])

    # (09) Articulation
    df_symmetries['articulation_forehead_symmetry'] = np.array([articulation_forehead_symmetry])
    df_symmetries['articulation_mouth_symmetry'] = np.array([articulation_mouth_symmetry])
    df_symmetries['articulation_frames_qty'] = np.array([articulation_frames_qty])

    # (10) Forced articulation
    df_symmetries['forced_articulation_forehead_symmetry'] = np.array([forced_articulation_forehead_symmetry])
    df_symmetries['forced_articulation_mouth_symmetry'] = np.array([forced_articulation_mouth_symmetry])
    df_symmetries['forced_articulation_frames_qty'] = np.array([forced_articulation_frames_qty])

    # (11) Rest state
    df_symmetries['rest_state_frames_qty'] = np.array([rest_state_frames_qty])

    # (12) Damaged frames
    df_symmetries['damaged_frames_qty'] = np.array([damaged_frames_qty])

    # Total frames
    df_symmetries['total_frames_qty'] = np.array([total_frames_qty])

    df_symmetries.to_csv(path_or_buf=symmetries_full_file_name, sep=',', na_rep='NaN', index=False, decimal='.')

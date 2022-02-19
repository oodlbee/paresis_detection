import dlib
import imageio
import numpy as np
import pandas as pd
from pathlib import Path

from get_distances import get_distances
from get_symmetries import get_symmetries


def shape_to_np_array(lib_shape, data_type="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=data_type)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (lib_shape.part(i).x, lib_shape.part(i).y)
    # return the list of (x, y)-coordinates
    return coords


predictor_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection/models/'
predictor_file_name = 'shape_predictor_68_face_landmarks.dat'
predictor_full_file_name = predictor_file_path + predictor_file_name

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_full_file_name)

video_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection/videos/'
video_file_name = '20180221_Плужников.mp4'
video_full_file_name = video_file_path + video_file_name
video = imageio.get_reader(video_full_file_name)

csv_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection/csv_files/'
aux_video_file_name = Path(video_file_name)
csv_file_name = str(aux_video_file_name.stem) + '.csv'
csv_full_file_name = csv_file_path + csv_file_name

markup_file_path = 'C:/Users/Andrew/PycharmProjects/paresis_detection/markup/'
markup_file_name = 'Разметка упражнений.xlsx'
markup_full_file_name = markup_file_path + markup_file_name
markup = pd.read_excel(markup_full_file_name, sheet_name=0)

# (01) Eyebrows raising
eyebrows_raising_begin = markup.loc[markup['file_name'] == video_file_name,
                                    'eyebrows_raising_begin'].values[0]
eyebrows_raising_end = markup.loc[markup['file_name'] == video_file_name,
                                  'eyebrows_raising_end'].values[0]

# (02) Left eye squeezing
left_eye_squeezing_begin = markup.loc[markup['file_name'] == video_file_name,
                                      'left_eye_squeezing_begin'].values[0]
left_eye_squeezing_end = markup.loc[markup['file_name'] == video_file_name,
                                    'left_eye_squeezing_end'].values[0]

# (03) Right eye squeezing
right_eye_squeezing_begin = markup.loc[markup['file_name'] == video_file_name,
                                       'right_eye_squeezing_begin'].values[0]
right_eye_squeezing_end = markup.loc[markup['file_name'] == video_file_name,
                                     'right_eye_squeezing_end'].values[0]

# (04) Left and right eyes squeezing
eyes_squeezing_begin = markup.loc[markup['file_name'] == video_file_name,
                                  'eyes_squeezing_begin'].values[0]
eyes_squeezing_end = markup.loc[markup['file_name'] == video_file_name,
                                'eyes_squeezing_end'].values[0]

# (05) Smile
smile_begin = markup.loc[markup['file_name'] == video_file_name,
                         'smile_begin'].values[0]
smile_end = markup.loc[markup['file_name'] == video_file_name,
                       'smile_end'].values[0]

# (06) Forced smile
forced_smile_begin = markup.loc[markup['file_name'] == video_file_name,
                                'forced_smile_begin'].values[0]
forced_smile_end = markup.loc[markup['file_name'] == video_file_name,
                              'forced_smile_end'].values[0]

# (07) Cheeks puffing
cheeks_puffing_begin = markup.loc[markup['file_name'] == video_file_name,
                                  'cheeks_puffing_begin'].values[0]
cheeks_puffing_end = markup.loc[markup['file_name'] == video_file_name,
                                'cheeks_puffing_end'].values[0]

# (08) Lips struggling
lips_struggling_begin = markup.loc[markup['file_name'] == video_file_name,
                                   'lips_struggling_begin'].values[0]
lips_struggling_end = markup.loc[markup['file_name'] == video_file_name,
                                 'lips_struggling_end'].values[0]

# (09) Articulation
articulation_begin = markup.loc[markup['file_name'] == video_file_name,
                                'articulation_begin'].values[0]
articulation_end = markup.loc[markup['file_name'] == video_file_name,
                              'articulation_end'].values[0]

# (10) Forced articulation
forced_articulation_begin = markup.loc[markup['file_name'] == video_file_name,
                                       'forced_articulation_begin'].values[0]
forced_articulation_end = markup.loc[markup['file_name'] == video_file_name,
                                     'forced_articulation_end'].values[0]


# (01) Eyebrows raising
eyebrows_raising_right_eyebrow_dist = []
eyebrows_raising_left_eyebrow_dist = []
eyebrows_raising_mouth_right_corner_dist = []
eyebrows_raising_mouth_left_corner_dist = []
eyebrows_raising_frames_qty = 0

# (02) Left eye squeezing
left_eye_squeezing_right_eyebrow_dist = []
left_eye_squeezing_left_eyebrow_dist = []
left_eye_squeezing_mouth_right_corner_dist = []
left_eye_squeezing_mouth_left_corner_dist = []
left_eye_squeezing_frames_qty = 0

# (03) Right eye squeezing
right_eye_squeezing_right_eyebrow_dist = []
right_eye_squeezing_left_eyebrow_dist = []
right_eye_squeezing_mouth_right_corner_dist = []
right_eye_squeezing_mouth_left_corner_dist = []
right_eye_squeezing_frames_qty = 0

# (04) Left and right eyes squeezing
eyes_squeezing_right_eyebrow_dist = []
eyes_squeezing_left_eyebrow_dist = []
eyes_squeezing_mouth_right_corner_dist = []
eyes_squeezing_mouth_left_corner_dist = []
eyes_squeezing_frames_qty = 0

# (05) Smile
smile_right_eyebrow_dist = []
smile_left_eyebrow_dist = []
smile_mouth_right_corner_dist = []
smile_mouth_left_corner_dist = []
smile_frames_qty = 0

# (06) Forced smile
forced_smile_right_eyebrow_dist = []
forced_smile_left_eyebrow_dist = []
forced_smile_mouth_right_corner_dist = []
forced_smile_mouth_left_corner_dist = []
forced_smile_frames_qty = 0

# (07) Cheeks puffing
cheeks_puffing_right_eyebrow_dist = []
cheeks_puffing_left_eyebrow_dist = []
cheeks_puffing_mouth_right_corner_dist = []
cheeks_puffing_mouth_left_corner_dist = []
cheeks_puffing_frames_qty = 0

# (08) Lips struggling
lips_struggling_right_eyebrow_dist = []
lips_struggling_left_eyebrow_dist = []
lips_struggling_mouth_right_corner_dist = []
lips_struggling_mouth_left_corner_dist = []
lips_struggling_frames_qty = 0

# (09) Articulation
articulation_right_eyebrow_dist = []
articulation_left_eyebrow_dist = []
articulation_mouth_right_corner_dist = []
articulation_mouth_left_corner_dist = []
articulation_frames_qty = 0

# (10) Forced articulation
forced_articulation_right_eyebrow_dist = []
forced_articulation_left_eyebrow_dist = []
forced_articulation_mouth_right_corner_dist = []
forced_articulation_mouth_left_corner_dist = []
forced_articulation_frames_qty = 0

# (11) Rest state
rest_state_right_eyebrow_dist = []
rest_state_left_eyebrow_dist = []
rest_state_mouth_right_corner_dist = []
rest_state_mouth_left_corner_dist = []
rest_state_frames_qty = 0

# (12) Damaged frames
damaged_frames_qty = 0

total_frames_qty = 0
counted_frames_qty = 0

for frame_num, _ in enumerate(video):
# for frame_num in range(0, 50):
    print('frame_num is: ', frame_num)
    image = video.get_data(frame_num)
    rects = detector(image, 1)
    if len(rects) == 1:
        shape = predictor(image, rects[0])
        points = shape_to_np_array(shape)

        right_eyebrow_dist, left_eyebrow_dist, \
            mouth_right_corner_dist, mouth_left_corner_dist = get_distances(points)

        # (01) Eyebrows raising
        if (eyebrows_raising_begin <= frame_num) and (frame_num < eyebrows_raising_end):
            eyebrows_raising_right_eyebrow_dist.append(right_eyebrow_dist)
            eyebrows_raising_left_eyebrow_dist.append(left_eyebrow_dist)
            eyebrows_raising_mouth_right_corner_dist.append(mouth_right_corner_dist)
            eyebrows_raising_mouth_left_corner_dist.append(mouth_left_corner_dist)
            eyebrows_raising_frames_qty += 1

        # (02) Left eye squeezing
        elif (left_eye_squeezing_begin <= frame_num) and (frame_num < left_eye_squeezing_end):
            left_eye_squeezing_right_eyebrow_dist.append(right_eyebrow_dist)
            left_eye_squeezing_left_eyebrow_dist.append(left_eyebrow_dist)
            left_eye_squeezing_mouth_right_corner_dist.append(mouth_right_corner_dist)
            left_eye_squeezing_mouth_left_corner_dist.append(mouth_left_corner_dist)
            left_eye_squeezing_frames_qty += 1

        # (03) Right eye squeezing
        elif (right_eye_squeezing_begin <= frame_num) and (frame_num < right_eye_squeezing_end):
            right_eye_squeezing_right_eyebrow_dist.append(right_eyebrow_dist)
            right_eye_squeezing_left_eyebrow_dist.append(left_eyebrow_dist)
            right_eye_squeezing_mouth_right_corner_dist.append(mouth_right_corner_dist)
            right_eye_squeezing_mouth_left_corner_dist.append(mouth_left_corner_dist)
            right_eye_squeezing_frames_qty += 1

        # (04) Left and right eyes squeezing
        elif (eyes_squeezing_begin <= frame_num) and (frame_num < eyes_squeezing_end):
            eyes_squeezing_right_eyebrow_dist.append(right_eyebrow_dist)
            eyes_squeezing_left_eyebrow_dist.append(left_eyebrow_dist)
            eyes_squeezing_mouth_right_corner_dist.append(mouth_right_corner_dist)
            eyes_squeezing_mouth_left_corner_dist.append(mouth_left_corner_dist)
            eyes_squeezing_frames_qty += 1

        # (05) Smile
        elif (smile_begin <= frame_num) and (frame_num < smile_end):
            smile_right_eyebrow_dist.append(right_eyebrow_dist)
            smile_left_eyebrow_dist.append(left_eyebrow_dist)
            smile_mouth_right_corner_dist.append(mouth_right_corner_dist)
            smile_mouth_left_corner_dist.append(mouth_left_corner_dist)
            smile_frames_qty += 1

        # (06) Forced smile
        elif (forced_smile_begin <= frame_num) and (frame_num < forced_smile_end):
            forced_smile_right_eyebrow_dist.append(right_eyebrow_dist)
            forced_smile_left_eyebrow_dist.append(left_eyebrow_dist)
            forced_smile_mouth_right_corner_dist.append(mouth_right_corner_dist)
            forced_smile_mouth_left_corner_dist.append(mouth_left_corner_dist)
            forced_smile_frames_qty += 1

        # (07) Cheeks puffing
        elif (cheeks_puffing_begin <= frame_num) and (frame_num < cheeks_puffing_end):
            cheeks_puffing_right_eyebrow_dist.append(right_eyebrow_dist)
            cheeks_puffing_left_eyebrow_dist.append(left_eyebrow_dist)
            cheeks_puffing_mouth_right_corner_dist.append(mouth_right_corner_dist)
            cheeks_puffing_mouth_left_corner_dist.append(mouth_left_corner_dist)
            cheeks_puffing_frames_qty += 1

        # (08) Lips struggling
        elif (lips_struggling_begin <= frame_num) and (frame_num < lips_struggling_end):
            lips_struggling_right_eyebrow_dist.append(right_eyebrow_dist)
            lips_struggling_left_eyebrow_dist.append(left_eyebrow_dist)
            lips_struggling_mouth_right_corner_dist.append(mouth_right_corner_dist)
            lips_struggling_mouth_left_corner_dist.append(mouth_left_corner_dist)
            lips_struggling_frames_qty += 1

        # (09) Articulation
        elif (articulation_begin <= frame_num) and (frame_num < articulation_end):
            articulation_right_eyebrow_dist.append(right_eyebrow_dist)
            articulation_left_eyebrow_dist.append(left_eyebrow_dist)
            articulation_mouth_right_corner_dist.append(mouth_right_corner_dist)
            articulation_mouth_left_corner_dist.append(mouth_left_corner_dist)
            articulation_frames_qty += 1

        # (10) Forced articulation
        elif (forced_articulation_begin <= frame_num) and (frame_num < forced_articulation_end):
            forced_articulation_right_eyebrow_dist.append(right_eyebrow_dist)
            forced_articulation_left_eyebrow_dist.append(left_eyebrow_dist)
            forced_articulation_mouth_right_corner_dist.append(mouth_right_corner_dist)
            forced_articulation_mouth_left_corner_dist.append(mouth_left_corner_dist)
            forced_articulation_frames_qty += 1

        # Rest state
        else:
            rest_state_right_eyebrow_dist.append(right_eyebrow_dist)
            rest_state_left_eyebrow_dist.append(left_eyebrow_dist)
            rest_state_mouth_right_corner_dist.append(mouth_right_corner_dist)
            rest_state_mouth_left_corner_dist.append(mouth_left_corner_dist)
            rest_state_frames_qty += 1

    else:
        damaged_frames_qty += 1

    counted_frames_qty += 1

total_frames_qty = eyebrows_raising_frames_qty + left_eye_squeezing_frames_qty + \
                   right_eye_squeezing_frames_qty + eyes_squeezing_frames_qty + \
                   smile_frames_qty + forced_smile_frames_qty + \
                   cheeks_puffing_frames_qty + lips_struggling_frames_qty + \
                   articulation_frames_qty + forced_articulation_frames_qty + \
                   rest_state_frames_qty + damaged_frames_qty

# (01) Eyebrows raising
eyebrows_raising_forehead_symmetry, eyebrows_raising_mouth_symmetry = get_symmetries(
    eyebrows_raising_right_eyebrow_dist, eyebrows_raising_left_eyebrow_dist,
    eyebrows_raising_mouth_right_corner_dist, eyebrows_raising_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (02) Left eye squeezing
left_eye_squeezing_forehead_symmetry, left_eye_squeezing_mouth_symmetry = get_symmetries(
    left_eye_squeezing_right_eyebrow_dist, left_eye_squeezing_left_eyebrow_dist,
    left_eye_squeezing_mouth_right_corner_dist, left_eye_squeezing_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (03) Right eye squeezing
right_eye_squeezing_forehead_symmetry, right_eye_squeezing_mouth_symmetry = get_symmetries(
    right_eye_squeezing_right_eyebrow_dist, right_eye_squeezing_left_eyebrow_dist,
    right_eye_squeezing_mouth_right_corner_dist, right_eye_squeezing_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (04) Left and right eyes squeezing
eyes_squeezing_forehead_symmetry, eyes_squeezing_mouth_symmetry = get_symmetries(
    eyes_squeezing_right_eyebrow_dist, eyes_squeezing_left_eyebrow_dist,
    eyes_squeezing_mouth_right_corner_dist, eyes_squeezing_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (05) Smile
smile_forehead_symmetry, smile_mouth_symmetry = get_symmetries(
    smile_right_eyebrow_dist, smile_left_eyebrow_dist,
    smile_mouth_right_corner_dist, smile_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (06) Forced smile
forced_smile_forehead_symmetry, forced_smile_mouth_symmetry = get_symmetries(
    forced_smile_right_eyebrow_dist, forced_smile_left_eyebrow_dist,
    forced_smile_mouth_right_corner_dist, forced_smile_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (07) Cheeks puffing
cheeks_puffing_forehead_symmetry, cheeks_puffing_mouth_symmetry = get_symmetries(
    cheeks_puffing_right_eyebrow_dist, cheeks_puffing_left_eyebrow_dist,
    cheeks_puffing_mouth_right_corner_dist, cheeks_puffing_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (08) Lips struggling
lips_struggling_forehead_symmetry, lips_struggling_mouth_symmetry = get_symmetries(
    lips_struggling_right_eyebrow_dist, lips_struggling_left_eyebrow_dist,
    lips_struggling_mouth_right_corner_dist, lips_struggling_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (09) Articulation
articulation_forehead_symmetry, articulation_mouth_symmetry = get_symmetries(
    articulation_right_eyebrow_dist, articulation_left_eyebrow_dist,
    articulation_mouth_right_corner_dist, articulation_mouth_left_corner_dist,
    rest_state_right_eyebrow_dist, rest_state_left_eyebrow_dist,
    rest_state_mouth_right_corner_dist, rest_state_mouth_left_corner_dist
)

# (10) Forced articulation
forced_articulation_forehead_symmetry, forced_articulation_mouth_symmetry = get_symmetries(
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
print('counted_frames_qty is:', counted_frames_qty)

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

df_symmetries.to_csv(path_or_buf=csv_full_file_name, sep=',', na_rep='NaN', index=False, decimal='.')

LIPS_POINTS = [
    0, 13, 14, 17, 37, 39, 40, 61, 78, 80,
    81, 82, 84, 87, 88, 91, 95, 146, 178, 181,
    185, 191, 267, 269, 270, 291, 308, 310, 311, 312,
    314, 317, 318, 321, 324, 375, 402, 405, 409, 415
    ]
LEFT_LIP_CORNER = [61]
RIGHT_LIP_CORNER = [291]
LEFT_EYE_POINTS = [
    249, 263, 362, 373, 374, 380, 381, 382,
    384, 385, 386, 387, 388, 390, 398, 466
    ]
RIGHT_EYE_POINTS = [
    7, 33, 133, 144, 145, 153, 154, 155,
    157, 158, 159, 160, 161, 163, 173, 246
    ]
LEFT_EYEBROW_POINTS = [276, 282, 283, 285, 293, 295, 296, 300, 334, 336]

RIGHT_EYEBROW_POINTS = [46, 52, 53, 55, 63, 65, 66, 70, 105, 107]

EXCERCISE_DICT = {
    'rest': [],
    'eyebrows_raising': [],
    'left_eye_squeezing': [],
    'right_eye_squeezing': [],
    'eyes_squeezing': [],
    'smile': [],
    'forced_smile': [],
    'cheeks_puffing': [],
    'lips_struggling': [],
    'articulation': [],
    'forced_articulation': []
}

SYMMETRIES_DICT = {
    'eyebrows_raising': {},
    'left_eye_squeezing': {},
    'right_eye_squeezing': {},
    'eyes_squeezing': {},
    'smile': {},
    'forced_smile': {},
    'cheeks_puffing': {},
    'lips_struggling': {},
    'articulation': {},
    'forced_articulation': {}
}

DISTANCES_EMPTY_DICT = {
    'rest': {
        'forehead': {'left': 0.0, 'right': 0.0},
        'mouth': {'left': 0.0, 'right': 0.0},
        'count_frames': 0
    },

    'eyebrows_raising': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'left_eye_squeezing': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'right_eye_squeezing': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'eyes_squeezing': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'smile': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'forced_smile': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'cheeks_puffing': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'lips_struggling': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'articulation': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
    'forced_articulation': {
        'forehead': {'left': [], 'right': []},
        'mouth': {'left': [], 'right': []},
        'count_frames': 0
    },
}

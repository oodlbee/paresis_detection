import math


def get_distances(points):

    # Right eyebrow (points from 18 to 22)
    sum_x = 0
    sum_y = 0
    count = 0
    for i in range(17, 22):
        sum_x += points[i][0]
        sum_y += points[i][1]
        count += 1
    right_eyebrow_center_x = int(sum_x / count)
    right_eyebrow_center_y = int(sum_y / count)

    # Left eyebrow (points from 23 to 27)
    sum_x = 0
    sum_y = 0
    count = 0
    for i in range(22, 27):
        sum_x += points[i][0]
        sum_y += points[i][1]
        count += 1
    left_eyebrow_center_x = int(sum_x / count)
    left_eyebrow_center_y = int(sum_y / count)

    # Right eye center (points from 37 to 42)
    sum_x = 0
    sum_y = 0
    count = 0
    for i in range(36, 42):
        sum_x += points[i][0]
        sum_y += points[i][1]
        count += 1
    right_eye_center_x = int(sum_x / count)
    right_eye_center_y = int(sum_y / count)

    # Left eye center (points from 43 to 48)
    sum_x = 0
    sum_y = 0
    count = 0
    for i in range(42, 47):
        sum_x += points[i][0]
        sum_y += points[i][1]
        count += 1
    left_eye_center_x = int(sum_x / count)
    left_eye_center_y = int(sum_y / count)

    # Mouth center (points 52, 58, 63, 67)
    sum_x = 0
    sum_y = 0
    count = 0
    for i in [51, 57, 62, 66]:
        sum_x += points[i][0]
        sum_y += points[i][1]
        count += 1
    mouth_center_x = int(sum_x / count)
    mouth_center_y = int(sum_y / count)

    # Mouth right corner (point 49)
    mouth_right_corner_x = points[48][0]
    mouth_right_corner_y = points[48][1]

    # Mouth left corner (point 55)
    mouth_left_corner_x = points[54][0]
    mouth_left_corner_y = points[54][1]

    right_eyebrow_dist = math.sqrt((right_eyebrow_center_x - right_eye_center_x) ** 2 +
                                   (right_eyebrow_center_y - right_eye_center_y) ** 2)
    right_eyebrow_dist = round(right_eyebrow_dist, 1)

    left_eyebrow_dist = math.sqrt((left_eyebrow_center_x - left_eye_center_x) ** 2 +
                                  (left_eyebrow_center_y - left_eye_center_y) ** 2)
    left_eyebrow_dist = round(left_eyebrow_dist, 1)

    mouth_right_corner_dist = math.sqrt((mouth_right_corner_x - mouth_center_x) ** 2 +
                                        (mouth_right_corner_y - mouth_center_y) ** 2)
    mouth_right_corner_dist = round(mouth_right_corner_dist)

    mouth_left_corner_dist = math.sqrt((mouth_left_corner_x - mouth_center_x) ** 2 +
                                       (mouth_left_corner_y - mouth_center_y) ** 2)
    mouth_left_corner_dist = round(mouth_left_corner_dist, 1)

    return (right_eyebrow_dist, left_eyebrow_dist,
            mouth_right_corner_dist, mouth_left_corner_dist)

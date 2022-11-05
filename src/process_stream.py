import os
import sys
import numpy as np
import cv2

sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 2)))

from src.redis_utils import get_redis

STREAM_URL = os.getenv('STREAM_URL')
STREAM_URL = 'rtsp://rtsp:qdhihmLp9SZpP3rq9L@192.168.1.131:554/av_stream/ch0'

BLUR_KERNEL = (5, 5)
FRAMES_COUNT = 48

SNAKE_RECTANGLE = {
    'y1': 685,
    'y2': 845,
    'x1': 704,
    'x2': 810
}

CEILING_INNER_RECTANGLE = {
    'y1': 390,
    'y2': 395,
    'x1': 1520,
    'x2': 1525
}

CEILING_OUTER_RECTANGLE = {
    'y1': 410,
    'y2': 415,
    'x1': 1400,
    'x2': 1405
}

redis_client = get_redis()


def recognize_green_white(image, rectangle):
    y1 = rectangle.get('y1')
    y2 = rectangle.get('y2')
    x1 = rectangle.get('x1')
    x2 = rectangle.get('x2')

    cropped_image = image[y1:y2, x1:x2]

    blurred = cv2.blur(cropped_image, BLUR_KERNEL)

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    green_mask = cv2.inRange(hsv, (36, 100, 100), (80, 255, 255))
    white_mask = cv2.inRange(hsv, (0, 0, 255), (0, 0, 255))

    green_imask = green_mask > 0
    white_imask = white_mask > 0

    green_white = np.zeros_like(blurred, np.uint8)
    green_white[green_imask] = blurred[green_imask]
    green_white[white_imask] = blurred[white_imask]

    avg_color_per_row = np.average(green_white, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    return avg_color


def is_green_or_white(average):
    if average[0] > 60 and average[1] > 70 and average[2] > 40:
        return True
    return False


def is_white(average):
    if average[1] > 150 and average[2] > 150:
        return True
    return False


def process_frames(image, framebuffer, processing_rectangle, white_only=False):
    if len(framebuffer) >= FRAMES_COUNT:
        framebuffer.pop(0)

    framebuffer.append(
        recognize_green_white(image, processing_rectangle)
    )
    avg = np.average(np.array(framebuffer), axis=0)
    print(avg, processing_rectangle)

    if white_only:
        return is_white(avg)
    else:
        return is_green_or_white(avg)

def main(stream_url):
    snake_framebuffer = []
    ceiling_inner_framebuffer = []
    ceiling_outer_framebuffer = []
    vcap = cv2.VideoCapture(STREAM_URL)
    while True:
        ret, frame = vcap.read()

        snake_res = process_frames(frame, snake_framebuffer, SNAKE_RECTANGLE)
        ceiling_inner_res = process_frames(frame, ceiling_inner_framebuffer, CEILING_INNER_RECTANGLE, True)
        ceiling_outer_res = process_frames(frame, ceiling_outer_framebuffer, CEILING_OUTER_RECTANGLE, True)

        # print(snake_res, ceiling_inner_res, ceiling_outer_res)

        redis_client.set('snake', 1 if snake_res else 0)
        redis_client.set('ceiling_inner', 1 if ceiling_inner_res else 0)
        redis_client.set('ceiling_outer', 1 if ceiling_outer_res else 0)


if __name__ == '__main__':
    main(STREAM_URL)


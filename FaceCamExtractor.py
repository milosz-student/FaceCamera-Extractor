import os
import cv2
import dlib
import random
import statistics

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop

SAMPLES_NUMBER = 10      # numbers of frames to detect face
THRESHOLD_VALUE = 1.1    # threshold value to reject some data
CAMERA_CUT = [300, 168]  # width, height of extracted camera
FACE_RATIO = [0.7, 0.3]  # 70% of height are below mid point and rest is above
VIDEO_RES = [1920, 1080] # video resolution from input file


def average(list):
    if len(list) == 0:
        return None
    return sum(list) / len(list)


def get_materials(path):
    files = os.listdir(path)
    names = []
    for file in files:
        name = os.path.splitext(file)[0]
        if (
            name not in names
            and "min" not in name
            and "out" not in name
            and "shr" not in name
            and "cut" not in name
            and "camera" not in name
        ):
            names.append(name)
    return names


def reject_extreme_values(data, threshold=THRESHOLD_VALUE):
    q1 = statistics.median_low(data)
    q3 = statistics.median_high(data)
    iqr = q3 - q1
    lower_limit = q1 - threshold * iqr
    upper_limit = q3 + threshold * iqr
    new_data = [x for x in data if lower_limit <= x <= upper_limit]
    return new_data


class FaceCamExtractor:
    def __init__(self, files_path):
        self.path = files_path
        self.materials = get_materials(files_path)

    def extract_all(self):
        for name in self.materials:
            if not os.path.exists(f"{self.path}\\{name}_camera.mp4"):
                print(f"Detecting face for {name}")
                self.detect_face(name)
            else:
                print(f"Camera cut already exists {name}")

    def detect_face(self, name):
        video = cv2.VideoCapture(f"{self.path}\\{name}.mp4")
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_nums = random.sample(range(1, frame_count), SAMPLES_NUMBER)

        x_, y_ = [], []

        for num in frame_nums:

            video.set(cv2.CAP_PROP_POS_FRAMES, num)
            ret, frame = video.read()
            detector = dlib.get_frontal_face_detector()
            faces = detector(frame, 1)

            if len(faces) > 0:
                face_coords = faces[0]

                face_center_x = int((face_coords.left() + face_coords.right()) / 2)
                face_center_y = int((face_coords.top() + face_coords.bottom()) / 2)
                print(
                    f"Found potential face on coordinates: {face_center_x} {face_center_y}"
                )
                x_.append(face_center_x)
                y_.append(face_center_y)

        video.release()
        if len(x_) > 0:

            input_filename = f"{self.path}\\{name}.mp4"
            output_filename = f"{self.path}\\{name}_camera.mp4"

            video = VideoFileClip(input_filename)

            x_ = reject_extreme_values(x_)
            y_ = reject_extreme_values(y_)

            x, y = average(x_), average(y_)
            width = CAMERA_CUT[0]
            height = CAMERA_CUT[1]

            x_values = [x - width // 2, x + width // 2]
            y_values = [y - FACE_RATIO[0] * height, y + FACE_RATIO[1] * height]

            if y_values[1] > VIDEO_RES[1]:
                tmp = y_values[1] - VIDEO_RES[1]
                y_values[0] -= tmp
                y_values[1] = VIDEO_RES[1]
            if y_values[0] < 0:
                tmp = y_values[0] * (-1)
                y_values[1] += tmp
                y_values[0] = 0
            if x_values[1] > VIDEO_RES[0]:
                tmp = x_values[1] - VIDEO_RES[0]
                x_values[0] -= tmp
                x_values[1] = VIDEO_RES[0]
            if x_values[0] < 0:
                tmp = x_values[0] * (-1)
                x_values[1] += tmp
                x_values[0] = 0

            cropped_video = crop(
                video, x1=x_values[0], y1=y_values[0], x2=x_values[1], y2=y_values[1]
            )

            cropped_video.write_videofile(output_filename, audio=False, threads=6)
            print(f"saved camera for {name}")

            video = cv2.VideoCapture(output_filename)
            video.set(cv2.CAP_PROP_POS_FRAMES, 10)
            ret, frame = video.read()
            cv2.imwrite(f"{path}\\{name}_scr_cut.png", frame)
            print(f"saved screen cut for {name}")


path = "test\\folder0"
asd = FaceCamExtractor(path)
asd.extract_all()

import cv2
import mediapipe as mp
import numpy as np
import math
import time

import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from hand_tracking_module import VanzeDetector

if __name__ == '__main__':
    # configuração do codec de video e resolucao
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cam_width = 1920
    cam_height = 1080
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

    hand_detector = VanzeDetector()

    # Ajustar o pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    vol = 0
    vol_bar = 400

    while True:
        # Leitura de frame
        _, img = capture.read()

        # Maniputalçai de frame
        img = hand_detector.find_hands(img)
        landmark_list = hand_detector.find_position(img)

        if landmark_list:
            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            img = hand_detector.draw_in_position(img, [x1, x2, center_x], [y1, y2, center_y])
            cv2.putText(img, f"{int(vol * 100)}%", (x2, y2), cv2.FONT_HERSHEY_DUPLEX, 1, (30, 186, 35),
                        3)
            cv2.line(img, (x1, y1), (x2, y2), (30, 186, 35), 3)

            length = math.hypot(x2 - x1, y2 - y1)
            #print(length)
            hand_range = [80, 325]

            vol = (length - hand_range[0]) / hand_range[1]

            if vol > 1: vol = 1
            if vol < 0: vol = 0

            vol_bar = np.interp(length, hand_range, [400, 150])
            vol_percentage = np.interp(length, hand_range, [0, 100])

            volume.SetMasterVolumeLevelScalar(vol, None)

        # Desenhar a barra do volume
        cv2.rectangle(img, (50, 150), (85, 400), (30, 30, 186), 3)

        # Completar o interior da barra de volume
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (30, 186, 35), cv2.FILLED)

        # Exibição de Frame
        cv2.imshow('Video', img)
        cv2.waitKey(1)

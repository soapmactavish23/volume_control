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
    # Ajustar o pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # configuração do codec de video e resolucao
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cam_width = 1920
    cam_height = 1080
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

    while True:
        _, img = capture.read()

        cv2.imshow('Video', img)
        cv2.waitKey(1)

import cv2
import zmq
import imutils
from time import time

cap = cv2.VideoCapture(0)
context = zmq.Context()
dst = context.socket(zmq.PUSH)
dst.bind("tcp://127.0.0.1:5557")

while True:
    ret, frame = cap.read()
    #frame = imutils.resize(frame, height=2960, width=1440)
    dst.send_pyobj(dict(frame=frame, ts=time()))

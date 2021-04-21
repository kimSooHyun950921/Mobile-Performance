import cv2
import zmq
import imutils
from time import time
camera_index=input('input camera_index:')
cap = cv2.VideoCapture(int(camera_index))
context = zmq.Context()
dst = context.socket(zmq.PUB)
dst.bind("tcp://127.0.0.1:5557")

frameno = 0

while True:
    ret, frame = cap.read()
    ts = time()
    frameno += 1
    dst.send_pyobj(frame)
    dst.send_pyobj(dict(frame=frame, ret=ret,ts=time()))

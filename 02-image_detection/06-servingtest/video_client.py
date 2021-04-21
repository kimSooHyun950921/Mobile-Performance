import cv2
import zmq
from time import time
from time import sleep
context = zmq.Context()
src = context.socket(zmq.PULL)
src.connect("tcp://127.0.0.1:5557")

dst1 = context.socket(zmq.PUSH)
dst1.connect("tcp://127.0.0.1:5558")

dst2 = context.socket(zmq.PUSH)
dst2.connect("tcp://127.0.0.1:5559")

count = 0
delay = 0.0

while True:
    msg = src.recv_pyobj()
    ts = msg['ts']
    frame = msg['frame']
    tnow = time()
    count += 1
    delay += tnow - ts

    if count % 150 == 0:
        print(delay/count)
        delay = 0.0
        count = 0

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst1.send_pyobj(frame)
    sleep(0.001)
    dst2.send_pyobj(frame)

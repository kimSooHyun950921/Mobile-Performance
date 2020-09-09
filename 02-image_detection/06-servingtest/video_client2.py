import cv2
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PULL)
zmq_socket.bind("tcp://127.0.0.1:5555")

while True:
    frame = zmq_socket.recv_pyobj()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

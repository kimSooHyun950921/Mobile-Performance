import signal
import asyncio
import threading
import numpy as np
import cv2
import time
import zmq
import sys

class Recording():
    def __init__(self, name):
        self.zmq_context = zmq.Context()
        self.src = self.zmq_context.socket(zmq.SUB)
        self.src.connect('tcp://127.0.0.1:5557')
        self.src.setsockopt_string(zmq.SUBSCRIBE, "")
        self.file_name = name
        self.fps=29
        frame = self.src.recv_pyobj()
        meta = self.src.recv_pyobj()
        self.writer = cv2.VideoWriter(self.file_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                      self.fps, (frame.shape[1], frame.shape[0]))
        self.is_start = False
        self.is_interrupted = False

    def write(self):
        while self.is_interrupted == False:
            frame = self.src.recv_pyobj()
            meta = self.src.recv_pyobj()
            self.writer.write(frame)
        self.writer.release()
        #self.src.close()

    def signal_handler(self, sig, frame):
        print("signal first")
        self.is_interrupted = True
        self.is_start = False
        self.writer.release()
        self.src.close()
        self.zmq_context.destroy()
        with open('done.txt','w') as f:
            f.write("DONE")
        print("close")
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename','-f',
                        required=True,
                        help='input file name')

    args = parser.parse_args()
    recording = Recording(args.filename)

    
    recording = Recording(args.filename)
    signal.signal(signal.SIGINT, recording.signal_handler)
    recording.is_start = True
    recording.write()
    

import threading
import numpy as np
import cv2
#from change_axis import ChangeAxis
import time
import zmq

class Recording():
    def __init__(self, name):
        self.zmq_context = zmq.Context()
        self.src = self.zmq_context.socket(zmq.SUB)
        self.src.connect('tcp://127.0.0.1:5557')
        self.src.setsockopt_string(zmq.SUBSCRIBE, "")
        self.frameno = 0
        self.fremote_frameno = 0
        self.writer = None
        self.is_start = False
        self.file_name = name
        self.fps=29
    
    def write(self):
        while True:
            frame = self.src.recv_pyobj()
            meta = self.src.recv_pyobj()
            self.frameno += 1
            self.last_frame_delay = int((time.time()-meta['ts']) * 1000)
            if self.is_start == False and self.writer:
                self.writer.release()
            if self.is_start == False:
                self.writer = cv2.VideoWriter(self.file_name,
                                              cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                              self.fps, (frame.shape[1], frame.shape[0]))
                self.is_start = True
            self.writer.write(frame)
        

    def __del__(self):
        self.ist_start = False
        self.writer.release()




class VideoStreaming(object):
    def __init__(self):
        print("TEST1")
        self.zmq_context = zmq.Context()
        self.cap = self.zmq_context.socket(zmq.SUB)
        self.cap.connect('tcp://127.0.0.1:5557')
        self.cap.setsockopt_string(zmq.SUBSCRIBE, "")
        self.frameno = 0
        self.remote_frameno = 0
        
    def __del__(self):
        self.cap.release()
        
    def resolution(self, capture, weight, height):
        capture.set(3, weight)
        capture.set(4, height)
        return capture

    def get_frame(self):
        frame = self.cap.recv_pyobj()
        meta = self.cap.recv_pyobj()
        return frame

    def start_record(self, file_name):
        self.is_record = True
        self.recording = Recording(file_name, self.cap)
        self.recording.write(self.is_record)

    def recoring(self, is_recording):
        self.recording.write(self.is_record)

    def stop_record(self):
        self.reocrding.write(False)


def get_fps():
    cam = VideoStreaming()

    num_frames = 300
    print("Capturing {0} frames".format(num_frames))

    start = time.time()
    for i in range(0, num_frames):
        ret, frame = cam.get_frame()#video.read()
    end = time.time()

    seconds = end - start
    print("Time taken: {0} seconds".format(seconds))

    fps = num_frames / seconds
    return fps


if __name__ == "__main__":
    #fps = get_fps()
    #print("fps:", fps)
    cam = VideoStreaming()
    is_ok = False
    print("START")
    count = 0
    try:
        while(True):
            ret, frame = cam.get_frame()
            height = frame.shape[0]
            width = frame.shape[1]

            vis = frame.copy()

            lower_red = np.array([30, 150, 50])
            upper_red = np.array([255, 255, 180])
            name = '{}.avi'.format(count)
            if cam.is_record == False:
                cam.start_record("TEST.avi")
            if cam.is_record==True and count % 1000:
                cam.stop_record()
            is_ok = True
            count += 1
            cv2.imshow('frame', vis)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # When everything done, release the capture
    except KeyboardInterrupt as e:
         print("[CTRL-C] is captured!!")
         cam.cap_res.release()
         cam.stop_record()
         cv2.destroyAllWindows()
    

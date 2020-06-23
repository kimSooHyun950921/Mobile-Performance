import threading
import numpy as np
import cv2
from change_axis import ChangeAxis
import time

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # 1280 720
        self.video = cv2.VideoWriter(self.name, fourcc, 29.0, (1920,1080))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.video.write(frame)

        self.video.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.video.release()



class VideoStreaming(object):
    def __init__(self):
        print("TEST1")
        self.cap = cv2.VideoCapture(2)
        self.cap_res = self.resolution(self.cap, 1920, 1080)
        self.is_record = False
        self.recordingThread = None
        self.out = None
    def __del__(self):
        self.cap.release()
        
    def resolution(self, capture, weight, height):
        capture.set(3, weight)
        capture.set(4, height)
        return capture

    def get_frame(self):
        ret, frame = self.cap_res.read()
        return ret, frame

    def start_record(self, file_name):
        self.is_record = True
        self.recordingThread = RecordingThread(file_name, self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        if self.recordingThread != None:
            self.recordingThread.stop()


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
    fps = get_fps()
    print("fps:", fps)
    cam = VideoStreaming()
    ch = ChangeAxis(390, 695, 40, 100, 445, 13)
    #mser = cv2.MSER_create()
    
    try:
        while(True):
            ret, frame = cam.get_frame()
            height = frame.shape[0]
            width = frame.shape[1]
            print(width, height)
            vis_contrast = frame.copy()
            gray_vis = cv2.cvtColor(vis_contrast, cv2.COLOR_BGR2GRAY)

            clahe = cv2.createCLAHE(clipLimit=8.0, tileGridSize=(16,16))
            cl1 = clahe.apply(gray_vis)

            vis = frame.copy()
            #hsv = cv2.cvtColor(cl1, cv2.COLOR_BGR2HSV)

            lower_red = np.array([30, 150, 50])
            upper_red = np.array([255, 255, 180])

            #mask = cv2.inRange(cl1, lower_red, upper_red)
            #res = cv2.bitwise_and(frame, frame, mask=mask)

            edges = cv2.Canny(cl1, 120, 125)
            arr = np.array(edges)
            result = np.where(arr==np.amax(arr))
            print(len(list(zip(result[0], result[1]))))
            print("FRAME END")            
            #regions, _ = mser.detectRegions(image_enhanced)
            #t_regions =[for p in regions]
            #hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

            #for i in regions:
            #x = int(len(i)/2)
            #       print(i[x][0], i[x][1])
            cv2.circle(vis, (960, 540), 1,(0, 0, 255), 10)

            for i in range(0, width):
                pixel = vis[0, i]
                if pixel[0] != 0 or pixel[1] !=0 or pixel[2] !=0:
                    print("get all x:", i)

            cv2.rectangle(vis, (707,43), (780, 108), (0,255,0), 10)
            cv2.rectangle(vis, (793,54), (1043,97), (0,255,0), 10)
            cv2.rectangle(vis, (1043,58), (1078,93), (0,255,0), 10)
            cv2.rectangle(vis, (1103,46),(1161,105), (0,255,0), 10)




            cv2.imshow('frame', edges)
            #cv2.imshow('frame', cl1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # When everything done, release the capture
    except KeyboardInterrupt as e:
         print("[CTRL-C] is captured!!")
         cam.cap_res.release()
         cv2.destroyAllWindows()
    

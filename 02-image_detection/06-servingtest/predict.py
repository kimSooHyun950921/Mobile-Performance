import cv2
import camera
import numpy
from predict_clickable import Predict
import tornado
import zmq
import json
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
define('port', default=8889, help='port to listen on')

class Streaming():
    def __init__(self):
        self.camera = camera.VideoStreaming()
    
    def stream(self):
        while True:
            ret, frame = self.camera.get_frame()
            vis = frame.copy()
            yield vis


class RecordingHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        
        self.write("Hello World")


class PredictHandler(tornado.web.RequestHandler):
    def initialize(self, predict):
        self.predict = predict

    @tornado.gen.coroutine
    def get(self):
        box_list = []
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PULL)
        zmq_socket.bind("tcp://127.0.0.1:5558")
        print("recv_img")
        frame = zmq_socket.recv_pyobj()
        print(frame.shape)
        boxes, scores, labels = self.predict.predict(frame)
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score > 0.35:
                b = box.astype(int)
                box_list.append(b)
        BOX = {"box":box_list}
        self.write(json.dumps(BOX))
        print(json.dumps(BOX))
        self.finish()





class ImageHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', \
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')

        #self.served_image_timestamp = time.time()
        my_boundary = b"--jpgboundary"
        while True:
            ret, frame = video_camera.get_frame()
            ret, jpg = cv2.imencode('.JPEG', frame)
            jpg_bytes = jpg.tobytes()
            self.write(my_boundary)
            self.write("Content-type: image/jpeg\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(jpg_bytes))
            self.write(jpg_bytes)
            yield self.flush()



def main():
    predict = Predict()

    app = Application([
      ('/video_feed', ImageHandler),
      ('/predict', PredictHandler, {'predict': predict}),
      ('/recording', RecordingHandler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()



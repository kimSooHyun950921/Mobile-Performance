import cv2
import camera
import numpy
import tornado
import zmq
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
define('port', default=8888, help='port to listen on')
class Streaming():
    def __init__(self):
        self.camera = camera.VideoStreaming()
    
    def stream(self):
        while True:
            ret, frame = self.camera.get_frame()
            vis = frame.copy()
            yield vis
class StreamingHandler(web.RequestHandler):

    @web.asynchronus
    @gen.coroutine
    def get(self):
        client = httpclient.AsyncHTTPClient()
        self.write('some opening')
        self.flush()

        requests = [
            httpclient.HTTPRequest(
                url = 'http://0.0.0.0/video_feed/',
                streaming_callback = self.on_chunck
            )
        ]
        self.write('close streming!')
        self.finish()


class RecordingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")


class PredictHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")


class ImageHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', \
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', \
        'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')
        
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PULL)
        zmq_socket.bind("tcp://127.0.0.1:5559")
        print("bind")
        my_boundary = b"--jpgboundary"
        #video_camera = camera.VideoStreaming()
        while True:
            #ret, frame = video_camera.get_frame()
            frame = zmq_socket.recv_pyobj()
            print("GET IMG")
            ret, jpg = cv2.imencode('.JPEG', frame)
            jpg_bytes = jpg.tobytes()
            self.write(my_boundary)
            self.write("Content-type: image/jpeg\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(jpg_bytes))
            self.write(jpg_bytes)
            yield self.flush()



def main():
    app = Application([
      ('/video_feed', ImageHandler),
      ('/predict', PredictHandler),
      ('/recording', RecordingHandler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()



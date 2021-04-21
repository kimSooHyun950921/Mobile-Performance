import cv2
import threading
import numpy
import tornado
import zmq
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
define('port', default=8888, help='port to listen on')

class RecordingThread(threading.Thread):
    def __init__(self, name, zmq_socket):
        threading.Thread.__init__(self)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(name, fourcc, 25.0, (1920, 1080))
        self.is_running = True
        self.zmq_socket = zmq_socket

    def run(self):
        while self.is_running:
            frame = self.zmq_socket.recv_pyobj()
            self.video.write(frame)
        print("release!")
        self.video.release()
        
    def stop(self):
        self.is_running = False
        #self.__del__()

    def __del__(self):
        print("release2")
        self.video.release()


class StreamingHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        client = httpclient.AsyncHTTPClient()
        self.write('some opening')
        self.flush()

        requests = [
            httpclient.HTTPRequest(
                url = 'http://0.0.0.0/video_feed/',
                streaming_callback = self.on_chunck
            ) for delay in [5, 4, 3, 2, 1]
        ]
        self.write('close streming!')
        self.finish()



class RecordingHandler(tornado.web.RequestHandler):
    def initialize(self, zmq_socket):
        self.zmq_socket = zmq_socket

    @tornado.gen.coroutine
    def post(self):
        global recording
        #recording = None
        appname = self.get_body_argument("appname")
        status = self.get_body_argument("status")
        print(appname, status)
        if status == "true":
            recording = RecordingThread('./data/'+appname+'.mp4', self.zmq_socket)
            recording.start()
        elif status == "false":
            if recording == None:
                self.write('No Recording Start Record False')
            else:
                recording.stop()
                recording.join()
                recording = None



class PredictHandler(tornado.web.RequestHandler):
    def initialize(self, zmq_socket):
        self.zmq_socket = zmq_socket
    
    @tornado.gen.coroutine
    def post(self):
        app_name = self.get_pody_argument("name")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #path = 
        out = cv2.Videowriter('', fourcc, 20.0)
        while True:
            frame = self.zmq_socket.recv_pyobj()



class ImageHandler(tornado.web.RequestHandler):
    def initialize(self, zmq_socket):
        self.zmq_socket = zmq_socket

    @tornado.gen.coroutine
    def get(self):
        ioloop = tornado.ioloop.IOLoop.current()

        self.set_header('Cache-Control', \
                        'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Content-Type', \
        'multipart/x-mixed-replace;boundary=--jpgboundary')
        self.set_header('Connection', 'close')
        
        print("bind")
        my_boundary = b"--jpgboundary"
        while True:
            frame = self.zmq_socket.recv_pyobj()
            print("GET IMG")
            ret, jpg = cv2.imencode('.JPEG', frame)
            jpg_bytes = jpg.tobytes()
            self.write(my_boundary)
            self.write("Content-type: image/jpeg\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(jpg_bytes))
            self.write(jpg_bytes)
            yield self.flush()



def main():
    context = zmq.Context()
    zmq_socket_streaming = context.socket(zmq.PULL)
    zmq_socket_recording = context.socket(zmq.PULL)
    zmq_socket_streaming.bind("tcp://127.0.0.1:5558")
    zmq_socket_recording.bind("tcp://127.0.0.1:5560")

    app = Application([
      ('/video_feed', ImageHandler, {'zmq_socket':zmq_socket_streaming}),
      ('/predict', PredictHandler),
      ('/recording', RecordingHandler, {'zmq_socket':zmq_socket_recording})
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()



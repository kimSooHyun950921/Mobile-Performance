import cv2
import numpy
from predict import Predict
import tornado
import zmq
import json
import pandas as pd
import time
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from change_axis_qhd import ChangeAxis
define('port', default=8889, help='port to listen on')

class PredictHandler(tornado.web.RequestHandler):
    def initialize(self, predict, ch, error_table):
        self.predict = predict
        self.ch = ch
        self.et = error_table

    @tornado.gen.coroutine
    def get(self):
        box_list = []
        print("recv_img")
        zmq_context = zmq.Context()
        src = zmq_context.socket(zmq.SUB)
        src.connect('tcp://127.0.0.1:5557')
        src.setsockopt_string(zmq.SUBSCRIBE, "")
        
        frame = src.recv_pyobj()
        meta = src.recv_pyobj()
        print("start predict from now on")
        try:
            boxes, scores, labels = self.predict.predict(frame)
        except Exception as e:
            boxes = [[0,0,0,0]]
            scores = [[0]]
            labels = [['_']]
        box_list = list()
        print("predict end")
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score > 0.25:
                b = box.astype(int).tolist()
                b = [self.ch.c_x(b[0]), self.ch.c_y(b[1]), \
                     self.ch.c_x(b[2]), self.ch.c_y(b[3])]
                print("RESULT", b)
                box_list.append(b)
        BOX = {"box":box_list}
        self.write(json.JSONEncoder().encode((BOX)))
        print(json.dumps(BOX))
        src.close()
        zmq_context.destroy()
        self.finish()


    def find_axis(self, min_axis, max_axis, xy):
        '''
            input: 최대- 최소 입력 좌표
            return: 가장 가까운 입력 좌표 찾기
            1. 최대- 최소값에 들어가는 좌표가 아니라면, 반환
            2. 그렇지 않다면 절반과 비교
            2-2. 중간값사이에 값이 있다면 아무 좌표나 반환
            3. 절반과 비교시 그사이에들어가 있지 않다면 반환
            4. 그렇지 않다면 절반과 비교
            5. 더이상 나눌 수 없는 범위가 오면 반환'''
        if xy == 'x':
            index_table = self.et.index.to_list()
        elif xy == 'y':
            index_table = self.et.columns.to_list()
        min_i = 0
        max_i = len(index_table) - 1
        if float(index_table[min_i]) > min_axis and float(index_table[max_i]) < max_axis:
            return None
        else:
            while max_i - min_i > 0:
                mid = int((min_i + max_i)/2)
                if float(index_table[mid]) == min_axis:
                    return min_axis
                if float(index_table[mid]) == max_axis:
                    return max_axis
                if float(index_table[mid]) < min_axis and float(index_table[mid]) < max_axis:
                    min_i = mid+1
                elif float(index_table[mid]) > min_axis and float(index_table[mid]) > max_axis:
                    max_i = mid-1
                else:
                    return index_table[mid]
        return index_table[min_i]




def main():
    predict = Predict()
    zmq_context = zmq.Context()
    src = zmq_context.socket(zmq.SUB)
    src.connect('tcp://127.0.0.1:5557')
    src.setsockopt_string(zmq.SUBSCRIBE, "")
    ch = ChangeAxis(640, 480, 65, 150,\
                    y_reverse=1,
                    bias_x=-30, bias_y=75)
    et = pd.read_csv('error_table.csv')

    app = Application([
      ('/predict', PredictHandler, {'predict': predict, 'ch':ch,'error_table':et}),
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()



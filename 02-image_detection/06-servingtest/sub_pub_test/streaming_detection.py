import json
import os
import asyncio
import camera
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import camera
import cv2
import subprocess
import os
import time
import zmq
import requests
import signal
import pandas as pd
import datetime
#import predict_clickable as pc
video_camera = None
recording_camera = None
record_proc =  None
app = Flask(__name__) 
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


def generate_axis(width, height):
    start = (i, j)
    end = ()


def draw_subline(width, height, vis):
    line_list = generate_axis(width, height)
    for i in line_list:
        cv2.line(vis, i[0], i[1], (154, 231, 197) ,1)
    return vis


def gn():
    global video_camera
    video_camera = camera.VideoStreaming()
    mser = cv2.MSER_create()
    out = ''
    num = 0

    while True:
        frame = video_camera.get_frame()
        ret, jpg = cv2.imencode('.JPEG', frame)
        jpg_bytes = jpg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')
    cam.cap_res.release()
    video.release()

@app.route('/video_feed')
def video_feed():
    print(type(gn()))
    return Response(gn(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


def get_path(file_name):
    device = file_name.split('_')[0]
    mp4_name = file_name.split('_')[1]
    
    default_path = '/home/kimsoohyun/00-Research/02-Graph/05-data/avi/'  
    path = os.path.join(default_path, get_curdate(),device,'{}.avi'.format(file_name))
    return path

def change_name(mp4_name):
    try:
        file_path = '/home/kimsoohyun/00-Research/02-Graph/data/cut_point'
        file_name = 'cut_info.csv'
        origin_file_name = os.path.join(file_path, file_name)
        new_file_name = os.path.join(file_path, mp4_name + '.csv')
        print(new_file_name)
        os.rename(origin_file_name, new_file_name)
    except Exception as e:
        pass


def send_starttime(filename):
    #===========CHANGE=========#
    print("SEND STARTTIME")
    ip = 'http://localhost:8888'
    starttime = int(time.time())
    data = {"source":"recording","status":"start", "starttime": starttime, "appname":filename, "count":5}
    res = requests.post(ip, data=data)
    print(res)


def get_curdate():
    cur_date = datetime.datetime.today().strftime('%Y-%m-%d')
    return cur_date


def send_endtime(filename):
    print("SEND ENDTIME");
    ip = 'http://localhost:8888'
    endtime = int(time.time())
    data = {"source":"recording", "status":"end",'endtime':endtime}
    print(data)
    res = requests.post(ip, data=data)
    write_csv(json.loads(res.text), filename)

def write_csv(json_list, filename):
    appname = '_'.join(filename.split('_')[1:])
    device = filename.split('_')[0]
    cur_date = get_curdate()
    path = f'/home/kimsoohyun/00-Research/02-Graph/05-data/cut_point/{cur_date}/{device}/{appname}.csv'
    df = pd.DataFrame(json_list)
    #df.loc[-1] = [0,0,5,0]#TODO
    #df = df.sort_values(['curtime'])
    df.to_csv(path, index=False)

@app.route('/record_status', methods=['POST'])
def start_record():
    print("start record")
    global record_proc
    json = request.get_json()
    print("GET JSON")
    status = json['status']
    filename = json['filename']
    print("status:", status," filename: ",  filename)
    fullpath = get_path(filename)

    print("FULL PATH",fullpath)
    if status == "true":
        time.sleep(10)
        #send_starttime(filename)
        record_proc = subprocess.Popen(["python3", "record.py", "--filename",f"{fullpath}"],\
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,\
                                      preexec_fn=os.setsid)#, universal_newlines=True)
        print("rescord start")
        return jsonify(result="started")
    elif status == "false":
        #os.killpg(os.getpgid(record_proc.pid), signal.SIGINT)
        record_proc.send_signal(signal.SIGINT)
        #signal.signal(signal.SIGINT, record_proc)
        send_endtime(filename)
        del record_proc
        recording_camera = None
        return jsonify(result="stopped")


if __name__ == "__main__":
    app.run(host='localhost', debug=True,port=8090, threaded=True)

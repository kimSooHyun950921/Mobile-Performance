import camera
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify            
import camera                                                                   
import cv2     
import subprocess
from execjs import get
import os 
import time
import requests
app = Flask(__name__)      
video_camera = None
                                                                            
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
        ret ,frame = video_camera.get_frame()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        vis = frame.copy()

        #regions, _ = mser.detectRegions(gray)
        #hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        #cv2.polylines(vis, hulls, 1, (0, 255, 0))
        width = vis.shape[0]
        height = vis.shape[1]
        #start = (0, int(width/2))
        #end = (height, int(width/2))

        #start_width = (int(height/2),0)
        #end_width = (int(height/2), width)

        #cv2.line(vis, start, end, (0, 148, 82) ,2)
        #cv2.line(vis, start_width, end_width, (0, 148, 82), 2)
        cv2.circle(vis, (695, 1080 ), 1,(0, 0, 255), 10)
        ret, jpg = cv2.imencode('.JPEG', vis)
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
    default_path = '/home/kimsoohyun/00-Research/02-Graph/05-data/mp4'   
    path = os.path.join(default_path, device,'{}.mp4'.format(file_name))
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
       

def send_starttime():
    #===========CHANGE=========#
    print("SEND STARTTIME")
    ip = 'http://localhost:8888'
    starttime = int(time.time())
    data = {"starttime": starttime}
    res = requests.post(ip, data=data)
    print(res)


@app.route('/record_status', methods=['POST'])
def start_record():
    global video_camera
    if video_camera == None:
        video_camera = camera.VideoStreaming()
    json = request.get_json()
    status = json['status']
    filename = json['filename']
    print("status:", status," filename: ",  filename)

    fullpath = get_path(filename)
    print(fullpath)
    if status == "true":
        send_starttime()
        video_camera.start_record(fullpath)
        return jsonify(result="started") 
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")


if __name__ == "__main__":
    app.run(host='localhost', debug=True,port=8090, threaded=True)

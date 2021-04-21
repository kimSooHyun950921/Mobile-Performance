import time
import requests
import random

class RequestManager():
    def __init__(self, device, path):
        self.defaultpath = path
        self.device = device


    def ready_experiment(self, packagename, starttime):
        robot_req = requests.post("http://localhost:8888",
                                  data = {"source":"recording-passive",\
                                  "status":"start",\
                                  "starttime":starttime,\
                                  "appname":packagename},\
                                  headers={'Content-Type': \
                                  'application/x-www-form-urlencoded'})


    def start_recording(self, packagename):
        x = requests.post('http://localhost:8090/record_status', \
                          json={"status":"true", 
                                "filename":f"{self.device}_{packagename}"},
                                headers={'Content-Type': 'application/json'})       
        return time.time()


    def stop_recording(self, packagename):
        x = requests.post('http://localhost:8090/record_status',
                          json={"filename":f"{self.device}_{packagename}",
                                "status":"false"},
                          headers={'Content-Type': 'application/json'}
                          )


    def __predict(self):
        predict_req = requests.get('http://localhost:8889/predict')
        return self.__parsing(predict_req)


    def __parsing(self, predict_req):
        obj = predict_req.json()
        if len(obj["box"]) == 0:
            return None, None
        axis = random.choice(obj["box"])
        rx = round((int(axis[0]) + int(axis[2]))/2, 2)
        ry = round((int(axis[1]) + int(axis[3]))/2, 2)
        return rx, ry


    def robot_touch(self, packagename):
        rx, ry = self.__predict()
        if rx != None and ry != None:
            robot_req = requests.post("http://localhost:8888",
                                      data = {"source":"recording-passive",
                                      "status":"on-going",
                                      "appname":packagename,
                                      "xy-axisx":rx,
                                      "xy-axisy":ry,
                                      "xy-axisz":-1})


    def robot_app_execute(self, packagename, starttime):
        robot_req = requests.post("http://localhost:8888",
                                  data = {"source":"recording-passive",
                                  "status":"appexecute",
                                  "execute":starttime,
                                  "appname":packagename})


    def start_analyze(self, avipath, csvpath, outpath,
                            poutpath, pcappath, count, packagename):
        requests.post("http://localhost:1111",
                      json={"device":self.device,
                            "avipath":avipath,
                            "csvpath":csvpath,
                            "outpath":outpath,
                            "pcappath":pcappath,
                            "pcapoutputpath":poutpath,
                            "appname":packagename,
                            "excount":count},
                      headers={'Content-Type': 'application/json'})


if __name__ == "__main__":
   import time
   import argparse
   parser = argparse.ArgumentParser(description='Process Manager')
   parser.add_argument('--path', '-p',
                        type=str,
                        default='/home/kimsoohyun/00-Research/02-Graph/05-data/',
                        help='input default path')
   parser.add_argument('--device', '-d',
                        type=str,
                        required=True,
                        help='input device')
   args = parser.parse_args()

   packagename = 'kr.co.company.hwahae'
   rm = RequestManager(args.device, args.path)
   for index in range(0, 5):
    rm.start_recording(packagename)
    time.sleep(3)
    rm.ready_experiment(packagename, time.time())
    rm.robot_app_execute(packagename,time.time())
    for jndex in range(0, 5):
        rm.robot_touch(packagename)
        time.sleep(3)
    rm.stop_recording(packagename)
    time.sleep(3)



import os
import requests
import csv
import json
from change_axis import ChangeAxis as C2
from change_axis_qhd import ChangeAxis as C1
from time import sleep

def read_csv(filename):
    with open(filename,  newline='') as f:
        reader = csv.reader(f, delimiter=',')
        coord_list = list()
        for row in  reader:
            if row[0] == 'x' and row[1] == 'y':
                continue
            coord_list.append(row)
    return coord_list


def json_template(x, y, appname):
    json_inner  = {"appname":appname, "x": x, "y": y}
    json_dumps = json.dumps(json_inner)
    json_result = {"xy-axis": json_dumps}
    return json_result
    

def main(args):
    """ 1. file_list:  모든 파일을 읽어옴
        2. coordin_list: 하나의 파일에서 좌표값을 읽어옴
        3. post request를 보냄"""

    c1 = C1(1440, 2960, 530, 1080, 695)
    c2 = C2(530, 1080, 40, 100, 695)
    filename = '{}.csv'.format(args.appname)
    appname = args.appname.split('/')[-1]
    start_res = send_req(args.ip, 100, 100, appname)
    print("[DEBUG-1]", start_res)
    sleep(2)
    for x, y in read_csv(filename):
        c_x = c2.r_x(c1.x_bias(c1.c_x(float(x))))
        c_y = c2.r_y(c1.y_bias(c1.c_y(float(y))))
        print("[DEBUG-1]", "old-x:"+str(x), ", old-y:"+ str(y), ", mid-x:"+ str(c1.x_bias(c1.c_x(float(x)))), ", mid-y:"+ str(c1.y_bias(c1.c_y(float(y)))))
        print("[DEBUG-2]",  json_template(c_x, c_y, appname))
        print("[DEBUG-3]", "old-x:"+str(x), ", old-y:"+ str(y), ", new-x:"+ str(c_x), ", new-y:"+ str(c_y))
        if args.method.lower() == 'post':
            response = send_req(args.ip, c_x, c_y, appname)
            print("[DEBUG-4]", response.status_code, response.reason)
            sleep(2)

    end_res = send_req(args.ip, -101, -101, appname)


def send_req(ip, x, y, appname):
    res = requests.post(ip, data=json_template(x, y, appname))
    return res 


if __name__ == "__main__":
    """필요한 Argument: file 이름 method 방법"""
    import argparse
    parser = argparse.ArgumentParser(description= 'send post msg')
    parser.add_argument('--appname', '-a',
                        type=str,
                        help='input coordinate-list file WITH *PATH*')
    parser.add_argument('--method','-m',
                        type=str,
                        help='input send method \nex)put, get, post...')
    parser.add_argument('--ip', '-i',
                        type=str,
                        help='input send ip and port')
    args = parser.parse_args()
    main(args)

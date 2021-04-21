import os                                                                       
import sys
import shutil                                                                   
import csv                                                                      
import subprocess                                                               
import xml.etree.ElementTree as ET                                              
import random                                                                   
import re                                                                       
import time
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/01-tapsterbot/dataSendTest')
import req
from change_axis_qhd import ChangeAxis as C1

FLAGS = None
def get_point(index, package_name):
    activity_list = list()

    # waiting for rendering end
    while True:
        if len(activity_list) > 5:
            activity_list.pop(0)
        if len(activity_list) ==5 and len(set(activity_list)) == 1:
            break

        #export XML log
        command = 'adb shell uiautomator dump /sdcard/{0}.xml'.format(index)
        dump_output = None
        try:
            dump_output = command_output(command)
        except subprocess.CalledProcessError:
            print("uiautomator dump error")

        if dump_output is not None and \
           not dump_output.startswith('UI hierchary dumped to:'):
            activity_list.append(0)
            point = (random.randrange(0, 1080),
                     random.randrange(0, 1920))
            continue

        #pull XML log
        command = 'adb pull /sdcard/{0}.xml ./dataset/00-xml/{1}/{0}.xml'.format(index, package_name)
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        xml = './dataset/00-xml/{0}/{1}.xml'.format(package_name, index)
        size, point = parse_xml_log(xml)
        activity_list.append(size)
    return point


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def check_dirs(dirs):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def terminate_env(pss):
    for ps in pss:
        command = 'adb shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError as e:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb shell kill -2 {0}'.format(psnum)
        command_check(command)


def command_popen(command):
    return subprocess.Popen(command, shell=True)


def command_check(command):
    return subprocess.check_call(command, shell=True)


def command_output(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
        if item.get('clickable') == 'true':
            bounds.append(item.get('bounds'))
    try:
        choose = random.choice(bounds)
        axes = re.findall('\d+', choose)
        point = (int(axes[0])+int(axes[2])/2, int(axes[1])+int(axes[3])/2)
    except ValueError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    except IndexError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    return size, point


def main(args):
    '''input: app_package_name
      output: csvfile 
             (appname, send-axis,expect-bot-axis, 
             clicked-axis, clicked-bot-axis, is success)
      1. 앱 패키지리스트를 읽어옴
      2. adb를 실행시켜 앱 패키지 이름으로 앱을 실행시킴
      3. 횟수가 0이될때까지 다음을 반복
         3-1. xml의 clickble bound 중앙값을 찾음
         3-2. 값 저장: clicked-axis, clicked_bot-axis
         3-3. 데이터 robot에 전송 함
         3-4. clicked-bot-axis 전송받음 --> 데이터 저장
         3-5. adb로부터 실제클릭리스트 받음 --> 데이터 저장
              getevent -l /dev/input/event0 | grep "ABS_MT_POSITION"
              displayX = x * 1440 / 4096
              displayY = y * 2960 / 4096            
         3-6. 수동으로 클릭되었는지 확인(is success)
         3-7. csv 저장
         '''
    binaries = ['adb']                                                          
    check_binary(binaries)
    change_point = C1(1440, 2960, 40, 100, 695)
                                                                                
    dirs = ['./dataset/01-coordinate-csv',
            './dataset/00-xml']                                                 
    check_dirs(dirs)                                                            
    print('checked all binaries dirs')                                          
    
    #앱 패키지 리스트를 읽어옴
    app_package_list = args.input                                               
    event = args.event                                                          
    if not os.path.exists(app_package_list):                                    
        raise Exception(' Need app_list.csv')                                   
                                                                                
    app_list = list()                                                           
                                                                                
    with open(app_package_list, 'r') as f:                                      
        reader = csv.DictReader(f)                                              
        for row in reader:                                                      
            print(row['package_name'])                                          
            app_list.append(row['package_name'])

    # 앱순회                                                  
    for package_name in app_list: 
        dirs = ['./dataset/00-xml/'+package_name]
        check_dirs(dirs)
        command = 'adb shell rm /sdcard/*.xml'                                  
        try:                                                                    
            command_check(command)                                              
        except subprocess.CalledProcessError:                                   
            pass                                                                
                                                                                
                                                                                
        #adb를 실행시켜 앱실행                                                              
        command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)  
        try:                                                                    
            command_check(command)                                              
        except subprocess.CalledProcessError:                                   
            pass                                                                
                                                                                
        for index in range(0, event):
            #xml의 point ckwdma
            send_axis = get_point(index, package_name)
            send_bot_axis = (change_point.c_x(send_axis[0]), \
                             change_point.c_y(send_axis[1]))
            res = req.send_req(args.ip, \
                               send_bot_axis[0], \
                               send_bot_axis[1], \
                               package_name)


            command = 'adb shell getevent -l /dev/input/event0 | grep "ABS_MT_POSTION"'
            try:
                result = command_output(command)
            except subprocess.CalledProcessError:
                result = None
            print(result)
            

                                                                                
                                                                                
        #stop app
        for index in range(0, 5):
            command = 'adb shell input keyevent KEYCODE_BACK'
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass
        command = 'adb shell am force-stop {0}'.format(package_name)
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Mobile xml extractor')
    parser.add_argument('-i', '--input', type=str,
                        required=True,
                        help=('list of app package names to test'))
    parser.add_argument('-e', '--event', type=int,
                        default=10,
                        help=('the number of generated user event(default: 10)'))
    parser.add_argument('-p', '--ip', type=str,
                        required=True,
                        help=('input send ip address'))
    FLAGS, _ = parser.parse_known_args()

    main(FLAGS)

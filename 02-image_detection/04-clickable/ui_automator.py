import os
import sys
import shutil
import csv
import subprocess
import xml.etree.ElementTree as ET
import random
import re
import time

FLAGS = None


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def check_dirs(dirs):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def terminate_env(pss):
    for ps in pss:
        command = 'adb -s 230943b313057ece shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError as e:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb -s 230943b313057ece shell kill -2 {0}'.format(psnum)
        command_check(command)


def command_popen(command):
    return subprocess.Popen(command, shell=True)


def command_check(command):
    return subprocess.check_call(command, shell=True)


def command_output(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def parse_xml_log(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print("Error", e)
        return None, None
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
        point = (random.randrange(int(axes[0]), int(axes[2])),                  
                 random.randrange(int(axes[1]), int(axes[3])))                  
    except ValueError:                                                          
        point = (random.randrange(0, 1080),                                     
                 random.randrange(0, 1920))                                     
    except IndexError:                                                          
        point = (random.randrange(0, 1080),                                     
                 random.randrange(0, 1920))                                     
    return size, point 


def main(args):
    """input: app_package_name
       output: app_screenshot, app_xml
       1. 앱 패키지리스트를 읽어온다.
       2. adb를 실행시켜 앱 패키지이름으로 앱을 실행시킨다.
       3. 횟수가 0이 될때까지 다음을 반복한다.
          3-1. 00-xml/appname/num.xml로 앱을 저장한다.
          3-2. 00-screenshot/appname/num.png로 앱 스크린을 저장한다.
          3-3. clickable을 찾아 임의 클릭을 한다 (혹은 수동으로 엔터쳐서)
          """
    binaries = ['adb']
    check_binary(binaries)

    dirs = ['/home/kimsoohyun/00-Research/02-Graph/02-image_detection/04-clickable/dataset/00-xml/2020-11-12',
            '/home/kimsoohyun/00-Research/02-Graph/02-image_detection/04-clickable/dataset/00-img/2020-11-12']
    check_dirs(dirs)
    print('checked all binaries dirs')

    app_package_list = args.input
    event = args.event
    if not os.path.exists(app_package_list):
        raise Exception(' Need app_list.csv')

    app_list = list()

    with open(app_package_list, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['PackageName'])
            app_list.append(row['PackageName'])

    for package_name in app_list:
        pss = ['screencap']
        
        command = 'adb -s 230943b313057ece shell rm /sdcard/*.xml'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb -s 230943b313057ece shell rm /sdcard/*.png'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        
        #create XML dir
        os.makedirs('./dataset/00-xml/2020-11-12/{0}'.format(package_name),
                    exist_ok=True)
        os.makedirs('./dataset/00-screenshot/2020-11-12/{0}'.format(package_name),
                    exist_ok=True)

        #lauch app
        command = 'adb -s 230943b313057ece shell monkey -p {0}\
                   -c android.intent.category.LAUNCHER 1'.format(package_name)
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass

        #insert click
        for index in range(0, event):
            time.sleep(10)
            activity_list = list()

            # waiting for rendering end
                #export XML log
            command = 'adb -s 230943b313057ece shell uiautomator dump /sdcard/{0}.xml'.format(index)
            dump_output = None
            try:
                dump_output = command_output(command)
            except subprocess.CalledProcessError:
                pass
            if dump_output is not None and \
               not dump_output.startswith('UI hierchary dumped to:'):
                activity_list.append(0)
                point = (random.randrange(0, 1080),
                         random.randrange(0, 1920))
                continue

            #pull XML log
            command = 'adb -s 230943b313057ece pull /sdcard/{0}.xml ./dataset/00-xml/2020-11-12/{1}/'.format(index, package_name)
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass
            xml = './dataset/00-xml/2020-11-12/{0}/{1}.xml'.format(package_name, index)
            size, point = parse_xml_log(xml)
            if size != None:
                activity_list.append(size)
            
            #get screen shot
            command = 'adb -s 230943b313057ece shell screencap -p /sdcard/{0}.png'.format(index)
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass
            command = 'adb -s 230943b313057ece pull /sdcard/{0}.png ./dataset/00-screenshot/2020-11-12/{1}/'.format(index, package_name)
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass

            # click point
            if point == None:
                continue
            if point[0] != point[1]:
                command = 'adb -s 230943b313057ece shell input tap {0} {1}'.format(point[0], point[1])
            else:
                command = 'adb -s 230943b313057ece shell input keyevent KEYCODE_BACK'
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass

        #stop app
        for index in range(0, 5):
            command = 'adb -s 230943b313057ece shell input keyevent KEYCODE_BACK'
            try:
                command_check(command)
            except subprocess.CalledProcessError:
                pass
        command = 'adb -s 230943b313057ece shell am force-stop {0}'.format(package_name)
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
    FLAGS, _ = parser.parse_known_args()
    
    main(FLAGS)

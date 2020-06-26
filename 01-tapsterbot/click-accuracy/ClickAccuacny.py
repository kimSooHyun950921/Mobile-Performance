import sys
import csv
import time
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/01-tapsterbot/dataSendTest')
import req 
import subprocess

FLAGS = None

def readPixelList(path):
    path_list = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            path_list.append((row[0],row[1]))
    return path_list


def execute_adb_command(command):
    try:
        process = subprocess.Popen(command, shell=True)
        result = process.communticate(timeout=3)
        print(result)
    except subprocess.CalledProcessError as e:
        print(e)
        return None
    except TimeoutExpired:
        process.kill()
    return result
    

def main(_):
    '''
    1. 파일을 읽음
    2. 데이터 전송함
    3. 클릭되었음을 알리면 
    '''
    pixel_list = readPixelList(FLAGS.path)
    for w,h in pixel_list:
        while True:
            time.sleep(5)
            res = req.send_req(FLAGS.ip, w, h, "TEST")
            print(res, w, h)
            if res.status_code == 200:
                adb_command_x = 'adb shell getevent -l /dev/input/event0 | grep "ABS_MT_POSITION_X"'
                adb_command_y = 'adb shell getevent -l /dev/input/event0 | grep "ABS_MT_POSITION_Y"'
                result_x = execute_adb_command(adb_command_x)
                result_y = execute_adb_command(adb_command_y)
                print(result_x, result_y)
                break
            else:
                continue


if __name__=="__main__":
    import argparse                                                             
                                                                                
    parser = argparse.ArgumentParser(description='Mobile xml extractor')                                     
    parser.add_argument('-p', '--path', type=str,    
                        default='./dataset/test.csv',
                        help=('list of app package names to test'))             
    parser.add_argument('-i', '--ip', type=str,                                 
                        default='http://localhost:8888',
                        help=('input send ip address'))                         
    FLAGS, _ = parser.parse_known_args()                                        
                                                                                
    main(_)                                                                
                  

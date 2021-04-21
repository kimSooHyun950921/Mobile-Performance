import sys
import csv
import time
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/01-tapsterbot/dataSendTest')
from change_axis import ChangeAxis as C2                                        
from change_axis_qhd import ChangeAxis as C1    
import req 
import subprocess

FLAGS = None

def readPixelList(path):
    path_list = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            path_list.append((row[0],row[1], row[2]))
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
    c1 = C1(1440, 2960, 56, 120, 695)                                         
    c2 = C2(530, 1080, 40, 100, 695)   
    print('curtime,'+'qhd-x,'+'qhd-y,'+'robot-x,'+'robot-y')
    for w,h, z in pixel_list:
        for i in range(0,100):
            while True:
                time.sleep(0.2)
            #c_x = c2.r_x(c1.x_bias(c1.c_x(float(w))))                               
            #c_y = c2.r_y(c1.y_bias(c1.c_y(float(h))))
                res = req.send_req(FLAGS.ip, w, h, z,"TEST")
                if res.status_code == 200:
                    print(str(time.time())+','+ str(w)+','+str(h))
                    break
                else:
                    continue
        time.sleep(13)

if __name__=="__main__":
    import argparse                                                             
                                                                                
    parser = argparse.ArgumentParser(description='Mobile xml extractor')                                     
    parser.add_argument('-p', '--path', type=str,    
                        default='./dataset/robot-test-on-going.csv',
                        help=('list of app package names to test'))             
    parser.add_argument('-i', '--ip', type=str,                                 
                        default='http://localhost:8888',
                        help=('input send ip address'))                         
    FLAGS, _ = parser.parse_known_args()                                        
                                                                                
    main(_)                                                                
                  

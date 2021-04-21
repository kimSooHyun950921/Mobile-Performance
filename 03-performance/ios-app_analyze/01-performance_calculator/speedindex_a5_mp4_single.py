from PIL import Image, ImageChops                                               
from skimage import io                                                          
from skimage.measure import compare_ssim as ssim        
from skimage.metrics import structural_similarity as ssim
#from m_c2d import sim as ssim
import cv2                                                                                
import csv                                                                      
import os                                                                       
import subprocess                                                               
from math import sqrt                                                           
import scipy.integrate as integrate                                             
import sys                                                                      
import logging                                                                  
import logging.config                                                           
import xml.etree.ElementTree as ET                                              
from operator import itemgetter                                                 
import configparser                                                                                
import time
#TODO ini file to args
class SpeedIndexCalculator():                                                            
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('/home/kimsoohyun/00-Research/02-Graph/03-performance/ios-app_analyze/01-performance_calculator/config.ini')

        self.MP4DIR = config.get('path', 'MP4DIR')
        self.CUTFILE = config.get('path', 'CUTFILE')
        self.IMGDIR = config.get('path', 'IMGDIR')
        self.OUTPUTDIR = config.get('path', 'OUTPUTDIR')
        self.OUTPUTFILE = config.get('path', 'OUTPUTFILE')
        
        self.FPS = int(config.get('analysis-info', 'FPS'))
        self.DEBUG = True #config.get('analysis-info', 'DEBUG')


    def get_event_time(self, get_event_list):                                             
        for index in range(to_index, from_index -1):
            if index - 1 == from_index:                                
                list_split_point.append((from_index, index))
                break                                                     
            try: 
                image1 = cv2.imread(files_list[index], cv2.COLOR_BGR2GRAY)
                image2 = cv2.imread(files_list[index-1], cv2.COLOR_BGR2GRAY)
                #image1 = io.imread(files_list[index]) 
                #image2 = io.imread(files_list[index-1])                                 
            except IndexError as e:                                                   
                print(e)                                                                
            similarity = ssim(image1, image2, multichannel=True)                      
            if similarity < 0.90:                                                      
                list_split_point.append((from_index, index))                            
                break                                                                   
        return list_split_point                                                   
                                                                                
                                                                                
    def sync(self, jpg_list, cut_list):                                                   
        sync_cut_point = list()
        cut_list.insert(0,0.0)
        for index in range(0, len(cut_list)):
            try:
                cut_index = int(int(cut_list[index])*self.FPS)
            except ValueError  as e:
                cut_index = int(float(cut_list[index])*self.FPS)
                                                                                
            for index in range(cut_index,len(jpg_list)):                              
                sync_index = index                                                      
                image1 = io.imread(jpg_list[cut_index])                                 
                image2 = io.imread(jpg_list[sync_index])                                
                similarity = ssim(image1, image2, multichannel=True)                    
                if self.DEBUG: print("SYNC() - cut_index: {0} sync index {1} sim:".format(cut_index, sync_index), similarity)                                             
                if similarity < 0.99:                                                    
                    sync_cut_point.append(sync_index)                                     
                    break                                                                 
        return sync_cut_point

                                                                                
    def get_split_point(self, files_list, cut_point):                                     
        list_split_point = list()
        if self.DEBUG: print("CUTPOINT: ", cut_point )
        experiment_time = len(cut_point)
        if experiment_time == 1:
            experiment_time = experiment_time + 1
        for index in range(0, experiment_time):                                      
            from_index = 0                                                          
            if index > 0:
                if len(cut_point) == 1:
                    from_imdex = cut_point[index-1]
                    to_index = len(files_list)-1
                else:
                    from_index = cut_point[index-1] ## 10                           
                    to_index = cut_point[index] ## 10                                   
                
                if self.DEBUG: print("INDEX",from_index, to_index)                                                       
                for index in range(to_index, from_index, -1):                           
                    if index-1 == from_index:                                           
                        list_split_point.append((from_index, index))                    
                        break
                    if self.DEBUG: print("GET SPLIT POINT()-index:", index)
                    image1 = io.imread(files_list[index])                               
                    image2 = io.imread(files_list[index-1])                             
                    similarity = ssim(image1, image2, multichannel=True)             
                    if self.DEBUG: print("GET SPLIT POINT()-ssim:", similarity)
                    if similarity < 0.999999:                                                
                        list_split_point.append((from_index, index))                    
                        break                                                           
        return list_split_point                                                     
                                                                                
                                                                                
    def get_speed_index(self, files_list, list_split_point):                              
        speed_index = list()                                                        
        for from_index, to_index in list_split_point:                               
            speed = 0                                                               
            sim_list = list()                                                       
            for index, snaps in enumerate(files_list[from_index:to_index]):
                image1 = io.imread(snaps)                                           
                image2 = io.imread(files_list[to_index])                            
                similarity = (1-ssim(image1, image2, multichannel=True))*(1000/self.FPS) 
                if self.DEBUG: print(f"GET SPEED INDEX()-speedindex {snaps}:", similarity)
                sim_list.append(similarity)                                         
                speed = speed + similarity                                          
            speed_index.append((speed, sim_list))  
        return speed_index                                                          
                                                                                
                                                                                
    def run_ffmpeg(self, device,video_name, ext):   
        video_file = '{}.{}'.format(video_name, ext)
        if self.DEBUG: print(video_file)
        time.sleep(5)
        temp_path = os.path.join(self.IMGDIR, device, video_name)
        if self.DEBUG: print("FFPEG temp_path", temp_path)
        mp4_file= os.path.join(self.MP4DIR, video_file)#, device, video_file)
        if self.DEBUG: print("FFPEG temp_path", mp4_file)
        os.makedirs(temp_path, exist_ok = True)  
        jpg_name = os.path.join(temp_path, 'out%04d.jpg')
        if self.DEBUG: print("FFMPEG jpg_name", jpg_name)
    # ffmpeg 실행                                                               
    # LuHa: fps=2 로 변경                                                       
    # command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR + str(video_name) + '/out%04d.jpg'
        command = 'ffmpeg -i ' + mp4_file + ' -vf fps={0} '.format(self.FPS) + jpg_name
        try:                                                                        
            ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
        except Exception as e:                                                      
            print(e)                                                                
            raise e                                                                 
        return True                                                                 
                                                                                
                                                                                
    def list_mp4(self, path):
        path = path.split('/')[-1]
        movie_ex_list = ['mp4', 'mkv', 'avi']
        result = []
        if self.DEBUG: print("MP4 PATH", path)
        ext = path.split('.')[-1]
        filename = path.replace('.avi','')
        package_name = '_'.join(path.split('_')[1:]).replace('.avi','')
        if ext in movie_ex_list:
            return filename, package_name, ext 
                                                                                
                                                                                
    def list_jpg(self, dirname, device):    
        print("LIST_JPG")
        result = []
        if self.DEBUG: print("DIRNAME", dirname)
        path = os.path.join(self.IMGDIR, device, dirname)
        for f in os.listdir(path):                                                  
            if f.endswith('.jpg'):                                                  
                
                result.append('{}/{}'.format(path, f))                                             
        return result                                                      
                    

    def get_similarity_list(self, files_list):
        list_similarity = []

        for index in range(len(files_list)):
            try:
                image1 = io.imread(files_list[index])
                image2 = io.imread(files_list[index+1])
            except OSError as e:
                continue
            except IndexError as e:
                continue
            similarity = ssim(image1, image2, multichannel = True)
            list_similarity.append((files_list[index], files_list[index+1], similarity))
        return list_similarity


    def write2csv(self, video_name, list_split_point, speed_list):
        csv_name = '{}.csv'.format(video_name)
        output_path = os.path.join(self.OUTPUTDIR, csv_name)
        if self.DEBUG: print(output_path)
        with open(output_path, 'a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            for index in range(0, len(speed_list)):
                writer.writerow([video_name, list_split_point[index], speed_list[index][0], speed_list[index][1]])


    def get_num_of_touch_event(self, cut_file_path):
        return len(list(csv.reader(open(cut_file_path))))


    def get_cut_point(self, filename):
        cuts_t = list()
        filename = '{}.csv'.format(filename)
        cut_file_path = os.path.join(self.CUTFILE, filename)
        if not os.path.isfile(cut_file_path):
            return None
        with open(cut_file_path,'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                cuts_t.append(row['time'])
        if self.DEBUG: print("get_cut_point(): ", cuts_t)
        return cuts_t


    def main(self, args):
        os.makedirs(self.OUTPUTDIR, exist_ok = True)
        cut_point = list()
        video_name, package_name, ext = self.list_mp4(args.path)
        if self.DEBUG: print("VIDEO NAME:", video_name, "EXT:", ext, "package_name:", package_name)
        cut_point = self.get_cut_point(package_name)
        if cut_point == None:
            print("NONE cutpoint")
            return
        try:
            self.run_ffmpeg(args.device, video_name, ext)
        except Exception as e:
            print("error occured")
            print(e)
        print("LISTJPG")
        jpg_files_list = self.list_jpg(video_name, args.device)
        jpg_files_list.sort()
        if self.DEBUG: print("FILE LIST:", jpg_files_list)

        sync_point = self.sync(jpg_files_list, cut_point)
        if self.DEBUG: print("GET SYNC POINT:", sync_point)

        list_split_point = self.get_split_point(jpg_files_list,sync_point)
        if self.DEBUG: print("LIST SPLIT POINT: ", list_split_point)

        speed_list = self.get_speed_index(jpg_files_list, list_split_point)
        if self.DEBUG: print("SPEED LIST: ", speed_list)
            
        self.write2csv(video_name, list_split_point, speed_list)
        if self.DEBUG: print("WRITE CSV")
                                                                               
                                                                                
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='calculate speedindex')
    parser.add_argument('--device', '-d',
                        type=str,
                        required=True,
                        help='input ios or android')
    parser.add_argument('--path', '-p',
                        type=str,
                        help='path')
    args = parser.parse_args()
    speed_index = SpeedIndexCalculator()
    speed_index.main(args)                                                                      
                                                                                                   

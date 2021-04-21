from PIL import Image, ImageChops                                               
from skimage import io                                                          
#from skimage.measure import compare_ssim as ssim                               
from skimage.metrics import structural_similarity as ssim                       
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
import pandas as pd
FPS = 1

def run_ffmpeg(video_path, img_path):
    os.makedirs(img_path, exist_ok = True)
    jpg_name = os.path.join(img_path, 'out%04d.jpg')

    command = 'ffmpeg -i ' + video_path + ' -vf fps={0} '.format(FPS) + jpg_name
    try:
        ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print(e)
        raise e
    return True


def get_ssim_list(jpg_file_list):
    list_similarity = []
    for index in range(1, len(jpg_file_list)):
        image1 = io.imread(jpg_file_list[index-1])
        image2 = io.imread(jpg_file_list[index])
        similarity = ssim(image1, image2, multichannel = True)
        print(similarity)
        list_similarity.append({'img1':jpg_file_list[index-1], \
                                'img2':jpg_file_list[index], \
                                'sim':similarity})
    return list_similarity


def list_jpg(imgpath):
    result = []
    for f in os.listdir(imgpath):
        if f.endswith('.jpg'):
            result.append('{}/{}'.format(imgpath, f))
    return result
    

def list_mp4_dir(mp4path, imgpath):
    with os.scandir(mp4path) as it:
        for entry in it:
            if entry.name.endswith('.mp4'):
                img_path = os.path.join(imgpath, entry.name.replace('.mp4',''))
                yield entry.path, img_path
        

    
def main(args):
    for mp4path, imgpath in list_mp4_dir(args.mp4path, args.imgpath):
        run_ffmpeg(mp4path, imgpath)
        jpg_files_list = list_jpg(imgpath)
        jpg_files_list.sort()
        ssim_list = get_ssim_list(jpg_files_list)
        df = pd.DataFrame(ssim_list)
        df_name = mp4path.split('/')[-1].replace('.mp4','.csv')
        df.to_csv('./ssim_data/'+df_name,index=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='calculate speedindex')
    parser.add_argument('--mp4path', '-m',
                        type=str,
                        required=True,
                        help='input mp4 path')
    parser.add_argument('--imgpath', '-i',
                        type=str,
                        required=True,
                        help='input img path')
    args = parser.parse_args()
    main(args)


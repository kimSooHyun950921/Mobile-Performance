import cv2
import os
import csv
import sys
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/02-image_detection/00-cv_mser')
from change_axis_qhd import ChangeAxis

LABEL_CLICKABLE = 'clickable'
LABEL_NON_CLICKABLE = 'non-clickable'
DEBUG = False

CLICKABLE_LIST = ['clickable', 'focusable', 'focused',\
                  'scrollable', 'selected']

#RAW파일을 읽기보다는 TAR안에 파일을 저장하면서 파일을 쓰는방법, 읽는 방법
#1. 수동으로 확인할것
#2. 디버깅이 쉽게 네이밍을 바꿈
#3. x,y 바꿈
def is_clickable_file(row):
    if len(row) >= 6:
        return True
    else:
        return  False


def parse_csv(csv_name):
    firstline = True
    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if firstline:
                firstline = False
                continue
            if is_clickable_file(row):
                yield row[0], row[1:5], row[5:]
            else:
                yield row[0], row[1:5], None


def read_csv(csv_path):
    clickable_path = os.path.join(csv_path, LABEL_CLICKABLE)
    non_clickable_path = os.path.join(csv_path, LABEL_NON_CLICKABLE)
    path_list = [clickable_path, non_clickable_path]
    for path in path_list:
        for csv in os.scandir(path):
            if csv.is_file() and csv.path.endswith('.csv'):
                if path == clickable_path:
                    yield csv.path, LABEL_CLICKABLE
                if path == non_clickable_path:
                    yield csv.path, LABEL_NON_CLICKABLE


def check_correct_point(p):
    print("POINT", p)
    if p[0] + p[1] + p[2] + p[3] == 0:
        return False
    return True


def get_package_name(axis_csv):
    return axis_csv.split('/')[-1].replace('.csv', '')


def get_img_path(p_name, img_path, screen_num):
    #get package name from csv name
    return os.path.join(img_path, p_name, '{}.png'.format(screen_num))


def check_dir(dir_name):
    os.makedirs(dir_name, exist_ok=True)


def main(arg):
    """
    Input: csv파일
    Output: crop img
    csv파일을 모두 읽어온다.(clickable, non-clickable따로 저장)
    csv를 한줄씩 읽으면서 앱에 해당하는 이미지를 불러온다
    opencv를 이용하여 좌표를 crop한다 clickable이면 clickable 폴더에
                                   non-clickable이면 non-clickable폴더에
    저장한다.
    """
    #앱이름-scene숫자-에서 몇번째 .png
    for axis_csv, label  in read_csv(arg.csv_path):
        crop_save_img = 0
        tmp_screen_num = 0
        for screen_num, point_list, clicklist in parse_csv(axis_csv):
            if DEBUG:
                print("label:", label, " screen_num:", screen_num, \
                      " point_list: ", point_list, " clicklist: ", clicklist)
            if tmp_screen_num != screen_num:
               crop_save_img = 0
            # 잘못된 값의 좌표가 들어간경우 확인(0,0,0,0)
            point = list()
            for p in point_list:
                point.append(int(p))
            is_correct_point = check_correct_point(point)
            
            if not is_correct_point:
                continue
        
            #image Read & Crop
            package_name = get_package_name(axis_csv)
            img_path = get_img_path(package_name, arg.img_path, screen_num)
            img = cv2.imread(img_path)
            #img_resize = cv2.resize(img, (540, 960))
            
            x = point[0]
            y = point[1]
            w = point[2] - point[0]
            h = point[3] - point[1]
            try:
                crop_img = img[y:y+h, x:x+w]
            except TypeError as e:
                print("TYPE ERROR", e)

            if DEBUG:
                #ch = ChangeAxis(1440, 2960, 540,960)

                #cv2.rectangle(img_resize, (ch.x_bias(ch.c_x(point[0])), ch.y_bias(ch.c_y(point[1]))),\
                #                          (ch.x_bias(ch.c_x(point[2])), ch.y_bias(ch.c_y(point[3]))),\
                #                   (0, 255, 0), 10)
                cv2.imshow('cropped', crop_img)
                
                cv2.waitKey(0)
           
            #clickable_dir, 과 non_clickable_dir이 있는지 확인
            for LABEL_CLICK in CLICKABLE_LIST:
                c_img = os.path.join(arg.output_img_path, LABEL_CLICK)
                check_dir(c_img)
            non_c_img = os.path.join(arg.output_img_path, LABEL_NON_CLICKABLE)
            check_dir(non_c_img)

            #write crop img
            crop_path = ''
            package_name = axis_csv.split('/')[-1].replace('.csv', '')
            if label == LABEL_CLICKABLE:
                for clickable_dir in clicklist[0].split(','):
                    img_name = '{}_{}_{}.png'.format(package_name, \
                                                     screen_num, \
                                                     crop_save_img)
                    crop_path = os.path.join(arg.output_img_path, \
                                             clickable_dir, img_name)
                    try:
                        cv2.imwrite(crop_path, crop_img) 
                    except: pass
            elif label == LABEL_NON_CLICKABLE:
                img_name = '{}_{}_{}.png'.format(package_name, \
                                                 screen_num, crop_save_img)
                crop_path = os.path.join(arg.output_img_path, label, img_name)
                try:
                    cv2.imwrite(crop_path, crop_img) 
                except: pass
            else:
                print("WRONG LABEL")

            crop_save_img += 1
            tmp_screen_num = screen_num


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Crop Data Img')
    parser.add_argument('-i', '--img_path', type=str,
                        default='./dataset/00-screenshot/',
                        help=('input img screenshot path'))
    parser.add_argument('-c', '--csv_path', type=str,
                        default='./dataset/01-csv',
                        help=('input axis csv path'))

    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)
 

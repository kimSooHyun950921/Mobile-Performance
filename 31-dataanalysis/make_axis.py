import os
import sys
import shutil
import csv
import subprocess
import xml.etree.ElementTree as ET
import random
import re
import time


def read_xml(path):
    file_list = list()
    for entry in os.scandir(path):
        if entry.is_dir():
            for xml in os.scandir(entry):
                if xml.is_file():
                    print(xml.path)
                    yield xml.path


def traverse(node):
    node_list = list()
    for sub_node in list(node):
        node_list.append(sub_node)
        new_node_list = traverse(sub_node)
        node_list += new_node_list
    return node_list


def parse_node(str_point):
    print(str_point)
    p = re.compile('[0-9]+')
    point_list = p.findall(str_point)
    return point_list


def get_axises(node_list):
    click_axies = list()
    for node in node_list:
        point_list = parse_node(node.get('bounds'))
        attr = node.attrib
        clickable, clickable_list = is_clickable(attr)
        if clickable:
            click_axies.append((point_list, clickable_list))
    return click_axies


def is_clickable(attrib):
    clickable = 'clickable'
    scrollable = 'scrollable'
    is_clickable = False
    clickable_list = list()

    if attrib[clickable] == 'true':
        if attrib[scrollable] == 'true':
            return is_clickable, None
        clickable_list.append(clickable)
        is_clickable = True
    return is_clickable, clickable_list


def check_clickable_path(c_list):
    #print("CLIST", c_list)
    if len(c_list[0][1]) == 0:
        return 'non-clickable'
    else:
        return 'clickable'


def write_csv(c_list, xml, path):
    # get full path
    xml_num = xml.split('/')[-1].split('.')[0]
    csv_name = '{}.csv'.format(xml.split('/')[-2])
    clickable_path = check_clickable_path(c_list)
    full_path = os.path.join(path, clickable_path, csv_name)
    #print(full_path)

    #check file exist
    mode = 'w'
    if os.path.isfile(full_path):
        mode = 'a'
    else:
        mode = 'w'

    #write csv
    with open(full_path, mode, newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        if mode == 'w':
            writer.writerow(['screen_num', 'x1', 'y1', \
                             'x2', 'y2', 'clicklist'])
        for elem in c_list:
            clicklist = ''
            if len(elem[1]) != 0:
                clicklist = ','.join(elem[1])
            print([xml_num, elem[0][0], elem[0][1], \
                   elem[0][2], elem[0][3], clicklist])
            writer.writerow([xml_num, elem[0][0], elem[0][1], elem[0][2], \
                            elem[0][3],clicklist])


def check_dir(args):
    clickable_dir = os.path.join(args.csvpath, 'clickable')
    non_clickable_dir = os.path.join(args.csvpath, 'non-clickable')
    dirs = [args.path, args.csvpath, clickable_dir, non_clickable_dir]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def main(args):
    """
    1. 모든 xml file 을 읽기
    2. xml순회 하면서 xml의 모든 노드들의 상태(clickable)등을 파악
    3. 그 노드의 bound와 clickable을 읽어
        3-1. clickable, scrollable, long-clickable 이 True이면
             01-csv/clickable/appname.csv에
             app_screenshot_num, x, y, [clickable...]형식으로 write
        3-2. 그렇지 않으면
             01-csv/non-clickable/appname.csv에
             app_screenshot_num, x, y로 적음
    Input: xml, app screenshot (starbucks_1.xml)
    output: csv: (app_screenshot_num, x, y, [clickable, ...])"""
    check_dir(args)

    for xml in read_xml(args.path):
        tree = ET.parse(xml)
        root = tree.getroot()
        node_list = traverse(root)
        click_list = get_axises(node_list)
        if len(click_list) != 0:
            write_csv(click_list, xml, args.csvpath)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='axis extractor')
    parser.add_argument('-p', '--path', type=str,
                        default='./dataset/00-xml/',
                        help=('input xml & screenshot path'))
    parser.add_argument('-c', '--csvpath', type=str,
                        default='./dataset/01-csv/',
                        help=('input output csv path'))
    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)

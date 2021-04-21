#!/usr/bin/env python3

import sys
import os
import statistics
import subprocess
import re
import pandas as pd
import time
def get_files(path, ext = '', recursive = False):
    path_list = [path]
    result = list()
    while len(path_list) > 0:
        cpath = path_list.pop()
        with os.scandir(cpath) as it:
            for entry in it:
                print("entryname",entry.name)
                if entry.name.endswith(ext):
                        yield entry.path
                else:
                    if recursive == True:
                        path_list.append(entry.path)

    return path_list


def filter_ip(path, newpath):
    print(path)
    print(os.path.join(newpath,path.split('/')[-1]))
    cp = subprocess.run(["tcpdump", "-r", path, "host", "not", 
                         "192.168.1.186", "-w", 
                         os.path.join(newpath,path.split('/')[-1])])
    print(cp)
    print("1")
                         
def get_subprocess_stdout(path, protocol):
    if protocol == 'total':
        options = '-lruZ'
    elif protocol == 'tcp':
        options = '-lrZ'
    elif protocol == 'udp':
        options = '-luZ'
    else:
        return None
        
    cp = subprocess.run(['tcptrace', '--output_dir=./tmp', options, path], 
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL,
            universal_newlines = True)
    return cp.stdout


def get_thrput_avg(string):
    try:
        mean = statistics.mean(
                    map(int,
                    re.findall('throughput:(?:\s)+(\d+) Bps', string)))
        return mean
    except:
        return -1


def get_rttavg_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('RTT avg:(?:\s)+(\d+.\d+) ms', string)))
        return mean
    except:
        return -1


def get_rttmax_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('RTT max:(?:\s)+(\d+.\d+) ms', string)))
        return mean
    except:
        return -1


def get_idletime_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('idletime max:(?:\s)+(\d+.\d+) ms', 
                    string)))
        return mean
    except:
        return -1


def get_dataxmittime_avg(string):
    try:
        mean = statistics.mean(
                    map(float, 
                    re.findall('data xmit time:(?:\s)+(\d+.\d+) secs', 
                    string)))
        return mean
    except:
        return -1


def get_tcp_len(string):
    try:
        length= len(re.findall('TCP connection', 
                    string))
        return length
    except:
        return -1


def get_http_len(string):
    try:
        length= len(re.findall(':80', 
                    string))
        return length
    except:
        return -1


def get_https_len(string):
    try:
        length = len(re.findall(':443', 
                    string))
        return length
    except:
        return -1


def get_elapsed_avg(string):
    try:
        m = re.search('elapsed time: \s+(\d+):(\d+):(\d+).(\d+)', string)
        mean = statistics.mean(
                  map(int,
                      int(m.group(1))*1000*pow(60, 2)+ 
                      int(m.group(2))*1000*pow(60, 1)+ 
                      int(m.group(3))*1000+  
                      int(m.group(4))))                 


        return mean
    except:
        return -1


def get_retrans_sum(string):
    try:
        sumation = sum(map(int,
                       re.findall('rexmt data pkts:(?:\s)+(\d+)', 
                       string)))
        return sumation
    except:
        return -1


def get_trafficvolume_sum_udp(string):
    try:

        sumation_udp = sum(map(int,
                       re.findall('data bytes sent:(?:\s)+(\d+)', 
                       string)))
        return sumation_udp
    except:
        return -1


def get_trafficvolume_sum_tcp(string):
    try:
        sumation_tcp = sum(map(int,
                       re.findall('unique bytes sent:(?:\s)+(\d+)', 
                       string)))
        return sumation_tcp
    except:
        return -1


def get_udp_len(string):
    try:
        length = len(re.findall('UDP connection',
                                        string))
        return length
    except:
        return -1


def get_ttfb_avg(string):
    try:
        result = list()
        for path in get_files('./tmp', '.dat'):
            cp = subprocess.run(['cat', path],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.DEVNULL,
                                universal_newlines = True)
            for line in cp.stdout.splitlines():
                ttfb = int(line.split(' ')[1])
                if ttfb == 0:
                    continue
                result.append(ttfb)
        mean = statistics.mean(result)
        return mean
    except:
        return 0


def get_keep_rate(string):
    try:
        target_list = re.findall('complete conn: \w*', string)
        keep_cnt = 0
        for conn in target_list:
            if conn == 'complete conn: no':
                keep_cnt = keep_cnt + 1
        return keep_cnt/len(target_list)
    except:
        return -1


def main(path, outputpath):

    #subprocess.run('rm ./tmp/*', shell = True)
    data = dict()
    alldf = pd.DataFrame()
    filename = path.split('./')[-1][:-5]
    if path.split('/')[-1] == 'android':
        device = 'android'
    elif path.split('/')[-1] == 'ios':
        device = 'ios'

    if device == 'ios':
        if not os.path.exists(os.path.join(path, 'new')):
            os.mkdir(os.path.join(path, 'new'))
        newpath = os.path.join(path, 'new')

        for filename in get_files(path, '.pcap'):
            print("PATH", path)
            filter_ip(filename, newpath)

    if device == 'ios':
        pcappath = newpath
    elif device == 'android':
        pcappath = path

    for path in get_files(pcappath, '.pcap'):
        string_all = get_subprocess_stdout(path, 'total')

        filename = path.split('/')[-1][:-5]
        if  path.split('/')[-2] == 'new':
            device = 'ios'
        elif  path.split('/')[-1] == 'android':
            device = 'android'
        print(device)
        data['device'] = device
        data['index'] = filename.split('_')[1]
        data['package'] = filename.split('_')[0]
        data['rtt'] = get_rttavg_avg(string_all)
        data['rttm'] = get_rttmax_avg(string_all)
        data['idletime'] = get_idletime_avg(string_all)
        data['xmittime'] = get_dataxmittime_avg(string_all)
        data['tcp'] = get_tcp_len(string_all)
        data['http'] = get_http_len(string_all)
        data['https'] = get_https_len(string_all)
        data['retrans'] = get_retrans_sum(string_all)
        data['trafficvolume'] = get_trafficvolume_sum_tcp(string_all) +\
                                get_trafficvolume_sum_udp(string_all)
        data['ttfb'] = get_ttfb_avg(string_all)
        data['keep'] = get_keep_rate(string_all)
        data['throughput'] = get_thrput_avg(string_all)
        subprocess.run('rm ./tmp/*', shell = True)

        string_tcp = get_subprocess_stdout(path, 'tcp')
        data['http_tcp'] = get_http_len(string_tcp)
        data['https_tcp'] = get_https_len(string_tcp)
        data['throughput_tcp'] = get_thrput_avg(string_tcp)
        data['ttfb_tcp'] = get_ttfb_avg(string_tcp)
        subprocess.run('rm ./tmp/*', shell = True)

        string_udp = get_subprocess_stdout(path, 'udp')
        #print(string_udp)
        
        #data['udp']
        udp = get_udp_len(string_udp)
        data['udp'] = udp
        if data['rtt'] > 0:
            df = pd.DataFrame.from_dict([data], orient='columns')
            df = df.sort_values(['package','index'])
            alldf = alldf.append(df)

    alldf.index = alldf.index.astype(int)
    alldf = alldf.sort_values(['package'])
    alldf = alldf.sort_index()
    alldf.to_csv('./result/analysis_{0}_{1}.csv'.format(device, time.time()), index=False)
if __name__ == '__main__':
    sys.exit(main(sys.argv))

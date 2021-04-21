import os
import sys
import time
import signal
import datetime
import subprocess
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/06-appexecute/')
from ios_execute import Call_APP

PCAP = "pcap/"
IOS = "ios"
ANDROID = "android"
ANDROID_DEVICE = "230943b313057ece"
IOS_IP = '192.168.1.168'
ANDROID_IP = '192.168.1.201'
class ProcessManager():
    def __init__(self, device, path):
        self.device = device
        self.defaultpath = path
        curtime = datetime.datetime.today().strftime("%Y-%m-%d")
        self.cur_pcappath = os.path.join(self.defaultpath,
                                     PCAP,
                                     curtime,
                                     device)


    def write_pcap(self, packagename, index):
        if self.device == 'ios':
            ip = IOS_IP
        elif self.device == 'android':
            ip = ANDROID_IP
        pcap_cmd = f"ssh root@192.168.1.1 \
                    tcpdump -i br-lan -s 0 -U -w - \
                    host {ip} > \
                    {self.cur_pcappath}/{packagename}_{index}.pcap"
        pcap_proc = subprocess.Popen(pcap_cmd, shell=True,
                                     preexec_fn=os.setsid)
        return pcap_proc


    def stop_pcap(self, proc):
        os.killpg(os.getpgid(proc.pid), signal.SIGINT)
        proc.send_signal(signal.SIGINT)
        cmd = 'ssh root@192.168.1.1 "killall -s 9 tcpdump"'
        proc = subprocess.Popen(cmd, shell=True,preexec_fn=os.setsid)


    def execute_app(self, appname, packagename):
        if self.device == IOS:
            input("Nonw App Start")
            #call_app = Call_APP()
            #call_app.main('start', appname)
            return time.time()
        elif self.device == ANDROID:
            curtime = time.time()
            subprocess.Popen(["adb", "-s", ANDROID_DEVICE, "shell", 
                              "monkey", "-p", packagename, \
                              "-c", "android.intent.category.LAUNCHER" ,"1"])
            return curtime


    def remove_data(self, packagename, device):
        if self.device == ANDROID:
            subprocess.Popen(["adb", "-s", ANDROID_DEVICE, "shell",
                              "pm","clear", packagename])


    def stop_app(self, packagename):
        if self.device == IOS:
            input("Now App Stop")
            #call_app = Call_APP()
            #call_app.main('end', packagename)
        elif self.device == ANDROID:
            app_cmd = f'adb -s {ANDROID_DEVICE} shell \
                        am force-stop {packagename}'
            app_proc = subprocess.Popen(app_cmd, shell=True, 
                                        preexec_fn=os.setsid)


if __name__ == "__main__":
    import time
    import argparse
    parser = argparse.ArgumentParser(description='Process Manager')
    parser.add_argument('--path', '-p',
                        type=str,
                        default='/home/kimsoohyun/00-Research/02-Graph/05-data/',
                        help='input default path')
    parser.add_argument('--device', '-d',
                        type=str,
                        required=True,
                        help='input device')
    args = parser.parse_args()
    pm = ProcessManager(args.device, args.path)

    pm.execute_app("화해", "kr.co.company.hwahae")
    #for index in range(0, 5):
    #    proc = pm.write_pcap("kr.co.company.hwahae", index)
    time.sleep(3)
    #    pm.stop_pcap(proc)
    pm.stop_app("kr.co.company.hwahae")


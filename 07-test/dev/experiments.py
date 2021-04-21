import os
import csv
import time
from utils.make_dir import DirManager as DM
from utils.request_manager import RequestManager as RM
from utils.process_manager import ProcessManager as PM

AVI = '.avi'
CSV = '.csv'

class EXP():
    def __init__(self, path, csvpath, device, count):
        self.dm = DM(path)
        self.rm = RM(device, path)
        self.pm = PM(device, path)
        self.csvpath = csvpath
        self.device = device
        self.count = count

    def start(self):
        self.dm.make_dir()

        for appname, packagename in self.read_csv(self.csvpath):
            starttime = self.rm.start_recording(packagename)
            self.rm.ready_experiment(packagename, starttime)
            for i in range(0, self.count):
                pcapproc = self.pm.write_pcap(packagename, i)
                if i == 0:
                    appexectime = self.pm.execute_app(appname, packagename)
                    self.rm.robot_app_execute(packagename, appexectime)
                else:
                    self.rm.robot_touch(packagename)
                time.sleep(15)
                self.pm.stop_pcap(pcapproc)
                print("Sleep 30 sec")
                time.sleep(3)
            self.rm.stop_recording(packagename)
            self.rm.start_analyze(os.path.join(self.dm.get_avipath(),
                                               self.device,
                                               packagename+AVI),
                                  os.path.join(self.dm.get_cutpath(),
                                               self.device,
                                               packagename+CSV),
                                  os.path.join(self.dm.get_outpath(),
                                               self.device,
                                               packagename+CSV),
                                  os.path.join(self.dm.get_pcapresultpath(),
                                               self.device),
                                  os.path.join(self.dm.get_pcappath(),
                                                self.device),
                                  self.count,
                                  packagename)

            self.pm.stop_app(packagename)
            time.sleep(2)


    def read_csv(self, csvfile_path):
        with open(csvfile_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row['AppName'], row['PackageName']



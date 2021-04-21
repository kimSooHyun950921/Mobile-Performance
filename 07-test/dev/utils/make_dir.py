import os
import datetime

PCAP = 'pcap/'
PCAPCALC='pcap_output/'
CUTPATH = 'cut_point/'
AVIPATH = 'avi/'
IMGPATH = 'cut_img/'
SIPATH = 'output/'
IOS = 'ios/'
ANDROID = 'android/'

class DirManager():
    def __init__(self, defaultpath):
        self.cur_date = datetime.datetime.today().strftime("%Y-%m-%d")
        self.path = defaultpath
        self.make_filepath()
        self.cur_pcappath = os.path.join(self.path, PCAP, self.cur_date)
        self.cur_cutpath = os.path.join(self.path, CUTPATH, self.cur_date)
        self.cur_avi = os.path.join(self.path, AVIPATH, self.cur_date)
        self.cur_si = os.path.join(self.path, SIPATH, self.cur_date)
        self.cur_img = os.path.join(self.path, IMGPATH, self.cur_date)
        self.cur_pcapcal = os.path.join(self.path, PCAPCALC, self.cur_date)

    def get_outpath(self):
        return self.cur_si


    def get_avipath(self):
        return self.cur_avi


    def get_cutpath(self):
        return self.cur_cutpath

    def get_pcapresultpath(self):
        return self.cur_pcapcal


    def get_pcappath(self):
        return self.cur_pcappath


    def make_filepath(self):
        if not os.path.isdir(os.path.join(self.path, PCAP)):
            os.mkdir(os.path.join(self.path, PCAP))
        if not os.path.isdir(os.path.join(self.path, CUTPATH)):
            os.mkdir(os.path.join(self.path, CUTPATH))
        if not os.path.isdir(os.path.join(self.path, AVIPATH)):
            os.mkdir(os.path.join(self.path, AVIPATH))
        if not os.path.isdir(os.path.join(self.path, IMGPATH)):
            os.mkdir(os.path.join(self.path, IMGPATH))
        if not os.path.isdir(os.path.join(self.path, IMGPATH)):
            os.mkdir(os.path.join(self.path, SIPATH))
        if not os.path.isdir(os.path.join(self.path, PCAPCALC)):
            os.mkdir(os.path.join(self.path, PCAPCALC))


    def make_dir(self):
        if not os.path.isdir(self.cur_pcappath):
            os.mkdir(self.cur_pcappath)
        if not os.path.isdir(self.cur_cutpath):
            os.mkdir(self.cur_cutpath)
        if not os.path.isdir(self.cur_avi):
            os.mkdir(self.cur_avi)
        if not os.path.isdir(self.cur_img):
            os.mkdir(self.cur_img)
        if not os.path.isdir(self.cur_si):
            os.mkdir(self.cur_si)
        if not os.path.isdir(self.cur_pcapcal):
            os.mkdir(self.cur_pcapcal)
        self.make_device_dir()


    def make_device_dir(self):
        if not os.path.isdir(os.path.join(self.cur_pcappath, IOS)):
            os.mkdir(os.path.join(self.cur_pcappath, IOS))
        if not os.path.isdir(os.path.join(self.cur_pcappath, ANDROID)):
            os.mkdir(os.path.join(self.cur_pcappath, ANDROID))

        if not os.path.isdir(os.path.join(self.cur_cutpath, IOS)):
            os.mkdir(os.path.join(self.cur_cutpath, IOS))
        if not os.path.isdir(os.path.join(self.cur_cutpath, ANDROID)):
            os.mkdir(os.path.join(self.cur_cutpath, ANDROID))

        if not os.path.isdir(os.path.join(self.cur_avi, IOS)):
            os.mkdir(os.path.join(self.cur_avi, IOS))
        if not os.path.isdir(os.path.join(self.cur_avi, ANDROID)):
            os.mkdir(os.path.join(self.cur_avi, ANDROID))

        if not os.path.isdir(os.path.join(self.cur_img, IOS)):
            os.mkdir(os.path.join(self.cur_img, IOS))
        if not os.path.isdir(os.path.join(self.cur_img, ANDROID)):
            os.mkdir(os.path.join(self.cur_img, ANDROID))


        if not os.path.isdir(os.path.join(self.cur_si, IOS)):
            os.mkdir(os.path.join(self.cur_si, IOS))
        if not os.path.isdir(os.path.join(self.cur_si, ANDROID)):
            os.mkdir(os.path.join(self.cur_si, ANDROID))


        if not os.path.isdir(os.path.join(self.cur_pcapcal, IOS)):
            os.mkdir(os.path.join(self.cur_pcapcal, IOS))
        if not os.path.isdir(os.path.join(self.cur_pcapcal, ANDROID)):
            os.mkdir(os.path.join(self.cur_pcapcal, ANDROID))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Directory Manager')
    parser.add_argument('--defaultpath', '-d',
                        type=str,
                        default='/home/kimsoohyun/00-Research/02-Graph/05-data/',
                        help='input default path')
    args = parser.parse_args()
    dm = DirManager(args.defaultpath)
    dm.make_dir()


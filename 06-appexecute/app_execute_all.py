import time
import pyaudio
import wave
import sys
import os
from google_speech import Speech

class Call_APP():
    def __init__(self, package_name):
        self.chunk = 1024
        result = self.find_name(package_name)
        print(package_name, result)
        if result == None:
            sys.exit(0)
        self.call_name = result[1]
        self.file_name = result[0]
        self.f = wave.open(self.file_name,"rb")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format =self.p.get_format_from_width(self.f.getsampwidth()),
                             channels = self.f.getnchannels(),
                             rate = self.f.getframerate(),
                             output = True)
        self.lang = 'ko'
        self.sox_effects = ("speed", "1.1")


    def find_name(self, package_name):
        path = '/home/kimsoohyun/00-Research/02-Graph/06-appexecute/wav_file/'
        bixby = f'{package_name}_bixby.wav'
        google = f'{package_name}_google.wav'
        if os.path.isfile(os.path.join(path,bixby)):
            return os.path.join(path,bixby), os.path.join(path,'hibixby.wav')
        elif os.path.isfile(os.path.join(path, google)):
            return os.path.join(path,google), os.path.join(path,'okgoogle.wav')
        else:
            return None


    def call_bixby(self):
        f = wave.open(self.call_name,"rb")
        p = pyaudio.PyAudio()
        stream = self.p.open(format =p.get_format_from_width(f.getsampwidth()),
                             channels = f.getnchannels(),
                             rate = f.getframerate(),
                             output = True)
        data = f.readframes(self.chunk)
        while data:
            stream.write(data)
            data = f.readframes(self.chunk)
        stream.stop_stream()
        p.terminate()

    def call_appname(self):
        f = wave.open(self.file_name,"rb")
        p = pyaudio.PyAudio()
        stream = self.p.open(format =p.get_format_from_width(f.getsampwidth()),
                             channels = f.getnchannels(),
                             rate = f.getframerate(),
                             output = True)
        data = f.readframes(self.chunk)
        while data:
            stream.write(data)
            data = f.readframes(self.chunk)
        stream.stop_stream()
        p.terminate()


    def exit_appname(self):
        f = wave.open(file_name,"rb")
        p = pyaudio.PyAudio()
        stream = self.p.open(format =p.get_format_from_width(f.getsampwidth()),
                             channels = f.getnchannels(),
                             rate = f.getframerate(),
                             output = True)
        data = f.readframes(self.chunk)
        while data:
            stream.write(data)
            data = f.readframes(self.chunk)
        stream.stop_stream()
        p.terminate()


    def start_main(self):
        self.call_bixby()
        time.sleep(0.5)
        self.call_appname()

    def end_main(self):
        self.call_bixby()
        time.sleep(0.5)
        self.exit_appname()

    def main(self, startend):
        if startend == 'start':
            self.start_main()
        elif startend == "end":
            self.end_main()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--packagename','-p', 
                        type=str, 
                        required=True,
                        help='input appname')
    parser.add_argument('--startend','-s',
                        type=str,
                        required=True,
                        help='input start or end message')
    args = parser.parse_args()
    c = Call_APP(args.packagename)
    c.main(args.startend)
            

    

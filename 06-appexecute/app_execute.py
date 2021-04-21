import time
import pyaudio
import wave
from google_speech import Speech

class Call_APP():
    def __init__(self, appname):
        self.chunk = 1024
        self.appname = appname
        self.f = wave.open(r"/home/kimsoohyun/00-Research/02-Graph/06-appexecute/하이빅스비_2.wav","rb")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format =self.p.get_format_from_width(self.f.getsampwidth()),
                             channels = self.f.getnchannels(),
                             rate = self.f.getframerate(),
                             output = True)
        self.lang = 'ko'
        self.sox_effects = ("speed", "1.1")

    
    def call_bixby(self):
        data = self.f.readframes(self.chunk)
        while data:
            self.stream.write(data)
            data = self.f.readframes(self.chunk)
        self.stream.stop_stream()
        self.p.terminate()

    def call_appname(self):
        text = f'{self.appname}실행'
        speech = Speech(text, self.lang)
        speech.play(self.sox_effects)

    def exit_appname(self):
        text = f'{self.appname}종료'
        speech = Speech(text, self.lang)
        speech.play(self.sox_effects)

    def start_main(self):
        #self.call_bixby()
        #time.sleep(0.5)
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
    parser.add_argument('--appname','-a', 
                        type=str, 
                        required=True,
                        help='input appname')
    parser.add_argument('--startend','-s',
                        type=str,
                        required=True,
                        help='input start or end message')
    args = parser.parse_args()
    c = Call_APP(args.appname)
    c.main(args.startend)
            

    

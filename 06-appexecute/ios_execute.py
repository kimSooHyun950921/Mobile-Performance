import os
import subprocess
import time
import pyaudio
import wave
from google_speech import Speech

class Call_APP():
    def __init__(self):
        self.chunk = 1024
        self.lang = 'ko'
        self.sox_effects = ("speed", "1.1")


    def call_siri(self):
        os.system('/home/kimsoohyun/00-Research/02-Graph/06-appexecute/call_siri.sh')
        #subprocess.run(["/home/kimsoohyun/00-Research/02-Graph/06-appexecute/call_siri.sh"])


    def call_appname(self, appname):
        text = f'{appname} 앱 실행'
        speech = Speech(text, self.lang)
        speech.play(self.sox_effects)


    def exit_appname(self):
        text = f'홈화면'
        speech = Speech(text, self.lang)
        speech.play(self.sox_effects)


    def start_main(self, appname):
        self.call_siri()
        time.sleep(0.65)
        self.call_appname(appname)


    def end_main(self):
        self.call_siri()
        time.sleep(0.65)
        self.exit_appname()


    def main(self, startend, appname):
        if startend == 'start':
            self.start_main(appname)
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
    c = Call_APP()
    c.main(args.startend, args.appname)
            

    

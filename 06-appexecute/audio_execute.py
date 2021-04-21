import pyaudio  
import wave 
from google_speech import Speech

#define stream chunk   
chunk = 1024  

#open a wav format music  
f = wave.open(r"/home/kimsoohyun/00-Research/02-Graph/06-appexecute/하이빅스비_2.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)  

#play stream  
while data:  
    stream.write(data)  
    data = f.readframes(chunk)  

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  

text2 = "밀리의 서재 실행해줘"
ko = 'ko'
sox_effects = ("speed", "1.1")
speech2 = Speech(text2, ko)
speech2.play(sox_effects)

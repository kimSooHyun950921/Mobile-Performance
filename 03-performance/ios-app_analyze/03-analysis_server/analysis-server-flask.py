import sys
import time
import json
import asyncio
from queue import Queue
from multiprocessing import Process, Value, Array, Manager
from flask import Flask, url_for, request
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/03-performance/ios-app_analyze/01-performance_calculator')
sys.path.append('/home/kimsoohyun/00-Research/02-Graph/03-performance/ios-app_analyze/04-packet_calculator')
from speedindex_a5_mp4_single_c2d import SpeedIndexCalculator
from main import pcap_main_single

app = Flask(__name__)
manager = Manager()
queue = manager.Queue()
count = 0


@app.route('/',methods=['GET', 'POST'])
def post():
    global queue
    data = request.data
    json_data = json.loads(data)
    
    print(json_data['device'], json_data['avipath'], json_data['csvpath'])
    queue.put((json_data['device'], \
               json_data['avipath'],\
               json_data['csvpath'],\
               json_data['outpath'],\
               json_data['pcappath'],
               json_data['pcapoutputpath'],\
               json_data['appname'],\
               json_data['excount']
               ))
    return 'hello word'


def processing():
    global queue
    speedindex_calculator = SpeedIndexCalculator()
    count = 0
    while True:
        while True:
            time.sleep(3)
            if queue.qsize() <= 0:
                break
            device, mp4path, csvpath, outpath, pcappath, pcapoutputpath, appname, count = queue.get()
            pcap_main_single(pcappath, pcapoutputpath, appname, count)
            speedindex_calculator.main(device, mp4path, csvpath, outpath)
            
            queue.task_done()
            print("size:", queue.qsize(), "count:", count)


if __name__ == "__main__":
    process = None
    try:
        process = Process(target=processing)
        process.start()
        app.run(port=1111, debug=True)
    except KeyboardInterrupt as e:
        print("Bye")
        process.join()

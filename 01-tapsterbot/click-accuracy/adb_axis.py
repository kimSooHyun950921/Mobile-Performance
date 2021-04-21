import re
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
def main():
    command = "adb shell getevent -lt /dev/input/event0 | grep 'ABS_MT_POSITION'"
    regex = r'ABS_MT_POSITION_(\w)\s+(\d+\w+)'
    process = Popen(command, shell=True,
                    stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    s = time.time()
    while True:
        result = process.stdout.readline().decode().replace('\n','')
        matches = re.findall(regex, result)
        for axis, value in matches:
            deci_value = int(value, 16)
            if axis == 'X':
                displayX = deci_value * 1440 / 4096
                print(axis, displayX)
            if axis == 'Y':
                displayY = deci_value * 2960 / 4096
                print(axis, displayY)
        e = time.time()
        if e - s > 10:
            print("=======================[ TERM ]==========================")
            s = time.time()

if __name__ == "__main__":
    main()

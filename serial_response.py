import serial
import time
# open serial
ser = serial.Serial("/dev/ttyAMA0",115200)

def getInfo(recv):
    
    if(recv[0]==35 and recv[-3]==38):
        return str.encode('useful data~')
    return str.encode('useless data!')


def main():
    while True:
        count = ser.inWaiting()
        if count != 0:
            print("got it...")
            recv = ser.read(count)
            msg = getInfo(recv)
            ser.write(msg)
            print(recv)
            print(msg)
        ser.flushInput()
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exit...")
        if ser != None:
            ser.close

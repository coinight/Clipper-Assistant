import socket
import Wifi,time
from machine import SPI,Pin,PWM
import st7735
import time,random
from bmpdecoder import bmpFileData

def initDisplay(rotate = True):
    global display,tftVdd
    tftVdd = PWM(Pin(11),freq =1000,duty = 500)
    display = st7735.TFT(
        SPI(1,baudrate=60000000, polarity=0, phase=0,
            sck=Pin(2),mosi=Pin(3),miso=Pin(10)),
        6,10,7)#spi, aDC, aReset, aCS,ScreenSize = (160, 160)
    display.initr()
    display.invertcolor(False)
    if rotate:
        display.rotation(2)
        #display._offset = (26,1)#(26,1)
    else:
        display.rotation(1)
        #display._offset = (1,26)#(26,1)
    display.fill(0)
    
initDisplay(False)
Wifi.ConnectWifi(hostname='Socket_test')
print(Wifi.wlan.ifconfig()[0])
print('等待连接中')
while True:
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect(('192.168.1.162',8080))
    except OSError as e:
        print('重新连接中',e)
        s.close()
        time.sleep(5)
        continue 
    print('连接成功')
    s.send(b'code')
    while True:
        try:
            data = s.recv(5)
            print(data)
        except OSError as e:
            print('等待数据',e)
            try:
                s.send(b'code')
                continue 
            except OSError as e:
                break             
        display.fill(0)
        size = int.from_bytes(data[1:3], 'little'),int.from_bytes(data[3:5], 'little')
        # print(size)
        try:
            s.send(b'\x00')
        except OSError as e:
            break             
        display._setwindowloc((0,0),(size[0]-1,size[1]-1))
        img_size = size[0]*size[1]*2
        i = 0
        while i<img_size:
            data = s.recv(2048)
            display._writedata(data)
            i += len(data)
            # print('next')
            # s.send(b'\x00')
    # 
    # 

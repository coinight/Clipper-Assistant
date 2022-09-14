from utime import sleep_ms
from ujson import loads
import network

wlan = network.WLAN(network.STA_IF)

def ConnectWifi(isFull = False,hostname = "WebClock3"):
    global wlan
    wlan.active(True)
    wlan.config(dhcp_hostname = "WebClock3")
    def do_connect(ssid,pword):
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(ssid, pword)
            timeout = 0
            while not wlan.isconnected():
                sleep_ms(20)
                timeout += 1
                if(timeout > 50 * 15):
                    print("WiFi Connected Error")
                    break
        print('network config:', wlan.ifconfig())

    
    f = open("wificonfig.json","a+")
    d = f.read()
    try:
        d = loads(d)
        temp = {}
        if not isFull:
            do_connect(list(d)[0],d[list(d)[0]])
            return 
        for i in wlan.scan():
            for j in d:
                if i[0].decode() == j:
                    temp[i[3]] = j
        print("Finded:",temp)
        print("Best:",temp[max(temp.keys())],d[temp[max(temp.keys())]])
        do_connect(temp[max(temp.keys())],d[temp[max(temp.keys())]])
    except ValueError:
        print("ValueError"+ d)
    
    f.close()
    del f,d
    print("###Wifi Connected###")
    return 

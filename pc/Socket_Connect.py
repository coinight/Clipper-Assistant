import _thread
import socket
import socket, time
import _thread
from typing import List, Any

import PIL.Image
import numpy as np
import pyautogui

s = socket.socket()
ip = socket.gethostbyname(socket.gethostname())
print(ip)

cil_list: list[socket.socket] = []


def rgb8882565(bgr):
    return (bgr[0] & 0xf8 | (bgr[1] & 0xfc) >> 5), \
           ((bgr[1] & 0x1C) << 3 | bgr[2] >> 3)


def send_screen_data(s: socket.socket, size, img):
    print(size)
    s.send(b'\xec' + size[0].to_bytes(2, byteorder='little') +
           size[1].to_bytes(2, byteorder='little'))
    print(s.recv(1))
    data = np.array(img)
    buf = bytearray()
    l: list[Any] = []
    for x in np.nditer(data, order='C'):
        if len(l) < 3:
            l.append(x)
        else:
            buf += bytearray(rgb8882565(l))
            l.clear()
            l.append(x)
    buf += bytearray(rgb8882565(l))
    s.send(buf)


def shack_hand(cil: socket.socket, cli_addr):
    print('连接地址：', cli_addr)
    get = cil.recv(1024).decode()
    if get != 'code':
        print(get)
        cil.close()
        return
    cil_list.append(cil)


def main_loop():
    s.bind((ip, 8080))
    s.listen(10)
    while True:
        new_cil, addr = s.accept()  # 建立客户端连接。
        _thread.start_new_thread(shack_hand, (new_cil, addr))


if __name__ == '__main__':
    main_loop()

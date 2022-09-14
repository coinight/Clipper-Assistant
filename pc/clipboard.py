import _thread
import numpy as np
import win32api
import win32clipboard as win32cb
import win32con
import time, math
from PIL import Image, ImageGrab, ImageDraw, ImageFont, ImageColor
import Socket_Connect
import Create_Text_img

Key_Code_C = 67
Key_Code_F = 70
flag_delta = 0
flag_delta_time = 0.2
screen_size = (160, 128)
screen_size_delta = screen_size[0] / screen_size[1]


def creatData(s):
    img = np.zeros((16 * len(s), 16))
    # img.fill(0)
    img_pil = Image.fromarray(img)
    fontText = ImageFont.truetype("./msyh.ttc", 16, encoding="utf-8")

    draw = ImageDraw.Draw(img_pil)

    draw.text((0, 0), s, font=fontText,
              fill=0xff)
    data = img_pil.load()
    return data


def get_clipboard(font_size=26,dy = -5):
    time.sleep(0.07)
    win32cb.OpenClipboard()
    format_cb = win32cb.EnumClipboardFormats(0)
    win32cb.CloseClipboard()
    print(format_cb)
    if format_cb == 8:
        print('pic')
        win32cb.OpenClipboard()
        img = ImageGrab.grabclipboard()
        try:
            win32cb.CloseClipboard()
        except Exception as e:
            print(e)
        size_delta = img.size[0] / img.size[1]
        if size_delta > screen_size_delta:
            size = (screen_size[0], math.floor(screen_size[0] / size_delta))
        else:
            size = (math.floor(screen_size[1] * size_delta), screen_size[1])
        img = img.resize(size)
        if len(Socket_Connect.cil_list) > 0:
            Socket_Connect.send_screen_data(Socket_Connect.cil_list[-1], size, img)
    elif format_cb >= 49000:
        win32cb.OpenClipboard()
        data:bytes = win32cb.GetClipboardData(win32con.CF_TEXT)
        win32cb.CloseClipboard()
        print(data)
        img, size = Create_Text_img.creatData(data.decode('gbk'),size=font_size,dy = dy)
        if len(Socket_Connect.cil_list) > 0:
            Socket_Connect.send_screen_data(Socket_Connect.cil_list[-1], size, img)

if __name__ == '__main__':

    _thread.start_new_thread(Socket_Connect.main_loop, ())
    while True:
        t = time.time()
        if t - flag_delta > flag_delta_time and win32api.GetKeyState(win32con.VK_CONTROL) < 0 and win32api.GetKeyState(
                Key_Code_F) < 0:
            flag_delta = t
            print("copy")
            get_clipboard()

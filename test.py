#-*-coding:utf-8-*-

import win32api
import win32gui
import win32con
from PIL import ImageGrab, Image
import time
import pytesseract
import re


def mouse_move(new_x, new_y):
    if new_y is not None and new_x is not None:
        point = (new_x, new_y)
        win32api.SetCursorPos(point)


def mouse_left_click(new_x=None, new_y=None, times=1):
    """
    鼠标左击事件
    :param new_x: 新移动的坐标x轴坐标
    :param new_y: 新移动的坐标y轴坐标
    :param times: 点击次数
    """
    mouse_move(new_x, new_y)
    time.sleep(0.05)
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        times -= 1


while True:
    wow_window = win32gui.FindWindow(0, '魔兽世界')
    win32gui.SetForegroundWindow(wow_window)
    points = win32gui.GetWindowRect(wow_window)

    time.sleep(1)
    image = ImageGrab.grab(points)
    image.save('./wow.jpg')

    # 查询厚皮价格
    mouse_left_click(1100, 45)
    time.sleep(10)

    # 获取第一行 的竞拍价截图
    img = Image.open('./wow.jpg')
    crop_area = [810, 194, 896, 217]
    price_screenshot = img.crop(crop_area)
    price_screenshot.save('./price_screenshot.jpg')

    image = Image.open('./price_screenshot.jpg')

    # 图片放大处理
    scale = 4
    width = int(image.size[0] * scale)
    height = int(image.size[1] * scale)
    image = image.resize((width, height), Image.ANTIALIAS)

    # 图片转灰度处理
    image = image.convert('L')
    # # 阈值 控制二值化程度，不能超过256
    threshold = 200
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化，convert('1')
    image = image.point(table, '1')

    text = pytesseract.image_to_string(image, lang='chi_sim')

    # 根据图片识别内容得出竞价
    res = re.findall(r'\d+', text)

    try:
        if len(res) < 2:
            price = 0.1
        else:
            price = int(res[0]) + int(res[1]) / 100
    except:
        continue
    print(price)

    # 如果 竞价 <= 6.3 , 选中 竞价
    if price < 6.3:
        mouse_left_click(100, 200)
        time.sleep(3)
        mouse_left_click(500, 670)
    # 否则，重新扫描拍卖行
    else:
        continue

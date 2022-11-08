import os
import time

import psutil
import win32api
import win32clipboard as clipboard
import win32con
import win32gui
from PIL import Image, ImageGrab
from numpy import average, dot, linalg


class DengLuQi():
    def __init__(self, app_path, username, password):
        self.app_path = app_path
        self.username = username
        self.password = password
        # 启动应用
        win32api.ShellExecute(0, 'open', self.app_path, '', '', 1)
        # 等待应用启动
        while True:
            self.wow_window = win32gui.FindWindow(0, '魔兽世界')
            if self.wow_window:
                break
            else:
                continue
            time.sleep(1)
        # 窗口置顶
        win32gui.SetForegroundWindow(self.wow_window)

    def wait_window_loading(self, crop_area, image_flag):
        # 等待窗口内控件加载完毕
        while True:
            self.get_screenshot(self.wow_window, './images/check.bmp')

            # 图片裁剪 (888, 707, 999, 734)
            self.image_crop('check.bmp', crop_area, 'new_check.bmp')

            # 核对检查点 检查点出现则窗口加载完毕
            if self.image_similarity_vectors_via_numpy(
                    './images/new_check.bmp', './images/%s' % image_flag):
                print('加载好了')
                time.sleep(2)
                break
            print('加载中')
            time.sleep(2)

    def get_screenshot(self, window_name, screenshot_name):
        points = win32gui.GetWindowRect(window_name)
        image = ImageGrab.grab(points)
        image.save(screenshot_name)

    def image_crop(self, image_name, points, new_image_name):
        img = Image.open('./images/%s' % image_name)
        crop_area = points
        crop = img.crop(crop_area)
        crop.save('./images/%s' % new_image_name)

    def get_thum(self, image, size=(64, 64), greyscale=False):
        # 对图片进行统一化处理
        # 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
        image = image.resize(size, Image.ANTIALIAS)
        if greyscale:
            # 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
            image = image.convert('L')
        return image

    def image_similarity_vectors_via_numpy(self, image1, image2):
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        # 计算图片的余弦距离 (是否为同一张图片)
        image1 = self.get_thum(image1)
        image2 = self.get_thum(image2)
        images = [image1, image2]
        vectors = []
        norms = []
        for image in images:
            vector = []
            for pixel_tuple in image.getdata():
                vector.append(average(pixel_tuple))
            vectors.append(vector)
            # linalg=linear（线性）+algebra（代数），norm则表示范数
            # 求图片的范数？？
            norms.append(linalg.norm(vector, 2))
        a, b = vectors
        a_norm, b_norm = norms
        # dot返回的是点积，对二维数组（矩阵）进行计算
        res = dot(a / a_norm, b / b_norm)
        if res >= 0.99:
            return True
        return False

    def login(self):
        self.wait_window_loading([898, 709, 997, 733], 'loginbtn.bmp')

        self.mouse_left_click(950, 550)
        time.sleep(0.5)
        self.send_msg(self.username)
        time.sleep(0.5)

        self.mouse_left_click(950, 650)
        time.sleep(0.5)
        self.send_msg(self.password)
        time.sleep(0.5)

        win32api.SendMessage(self.wow_window, win32con.WM_KEYDOWN,
                             win32con.VK_RETURN, 0)
        win32api.SendMessage(self.wow_window, win32con.WM_KEYUP,
                             win32con.VK_RETURN, 0)
        # 等待角色列表加载完毕 （可改进）
        self.wait_window_loading([863, 916, 1000, 950], 'getinbtn.bmp')

        self.mouse_left_click(900, 930)

    def process_exists(self, processname):
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == processname:
                return True
            return False

    def send_msg(self, msg):
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(win32con.CF_UNICODETEXT, msg)
        clipboard.CloseClipboard()
        win32api.keybd_event(17, 0, 0, 0)
        time.sleep(0.5)
        win32api.keybd_event(86, 0, 0, 0)
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    def mouse_move(self, new_x, new_y):
        if new_y is not None and new_x is not None:
            point = (new_x, new_y)
            win32api.SetCursorPos(point)

    def mouse_left_click(self, new_x=None, new_y=None, times=1):
        """
        鼠标左击事件
        :param new_x: 新移动的坐标x轴坐标
        :param new_y: 新移动的坐标y轴坐标
        :param times: 点击次数
        """
        self.mouse_move(new_x, new_y)
        time.sleep(0.05)
        while times:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            times -= 1

    def get_child_windows(self, parent):
        '''     
        获得parent的所有子窗口句柄
        返回子窗口句柄列表
        '''
        if not parent:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(parent,
                                  lambda hwnd, param: param.append(hwnd),
                                  hwndChildList)
        return hwndChildList

    def process_kill(self, pname):
        # 杀死进程
        os.system("taskkill /F /IM %s" % pname)


if __name__ == "__main__":
    app_path = 'E:/game/oldwow/World of Warcraft/_classic_/Wow.exe'
    username = ''
    password = ''
    dlq = DengLuQi(app_path, username, password)
    dlq.login()

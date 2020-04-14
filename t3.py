import win32api
import win32gui
import win32con
import time
import win32clipboard as clipboard


def send_msg(msg):
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    clipboard.CloseClipboard()

    # win32api.SendMessage(wow_window, win32con.WM_PASTE, 0, 0)
    # win32api.SendMessage(wow_window, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32api.keybd_event(17, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(86, 0, 0, 0)

    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


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


def get_child_windows(parent):
    '''     
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),
                              hwndChildList)
    return hwndChildList


# #获取某个句柄的类名和标题
# title = win32gui.GetWindowText(hwnd)
# clsname = win32gui.GetClassName(hwnd)

# #获取父句柄hwnd类名为clsname的子句柄
# hwnd1= win32gui.FindWindowEx(hwnd, None, clsname, None)

win32api.ShellExecute(0, 'open', r'E:\\game\\oldwow\\World of Warcraft\\_classic_\\Wow.exe', '','',1)
time.sleep(10)

wow_window = win32gui.FindWindow(0, '魔兽世界')
win32gui.SetForegroundWindow(wow_window)
time.sleep(0.5)
# points = win32gui.GetWindowRect(wow_window)
# print(points)

# child_windows = get_child_windows(wow_window)
# print(child_windows)

# title = win32gui.GetWindowText(cw[0])
# clsname = win32gui.GetClassName(child_windows[0])

# 获取子容器,识别结果输入框
# edtextHwnd = win32gui.FindWindowEx(wow_window, None, 'Edit', '')

# buf_size = win32gui.SendMessage(edtextHwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1  # 要加上截尾的字节
# str_buffer = win32gui.PyMakeBuffer(buf_size)  # 生成buffer对象
# win32api.SendMessage(edtextHwnd, win32con.WM_GETTEXT, buf_size, str_buffer)  # 获取buffer
# print(str_buffer[:-1])
# str = str(str_buffer[:-1])  # 转为字符串
# result = str
# print(result)

# # 获取识别结果中输入框文本
# length = win32gui.SendMessage(edtextHwnd, win32con.WM_GETTEXTLENGTH)+1
# buf = win32gui.PyMakeBuffer(length)
# #发送获取文本请求
# win32api.SendMessage(edtextHwnd, win32con.WM_GETTEXT, length, buf)
# #下面应该是将内存读取文本
# address, length = win32gui.PyGetBufferAddressAndLen(buf[:-1])
# text = win32gui.PyGetString(address, length)

# print(text)

mouse_left_click(950, 550)
time.sleep(0.5)
send_msg('cyjmmy@sohu.com')
time.sleep(0.5)




mouse_left_click(950, 650)
time.sleep(0.5)
send_msg('zxl19890518')
time.sleep(0.5)

win32api.SendMessage(wow_window, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
win32api.SendMessage(wow_window, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

time.sleep(10)
mouse_left_click(900, 930)
# win32api.SendMessage(wow_window, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
# win32api.SendMessage(wow_window, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
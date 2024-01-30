import win32gui
import win32con
import win32api

if __name__ == '__main__':
    # 获取鼠标位置
    win32api.GetCursorPos()
    win32api.SetThreadLocale(win32con.SUBLANG_CHINESE_SIMPLIFIED)
    # # 鼠标左键按下
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    #
    # # 鼠标左键放开
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    #
    # # 鼠标右键按下
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    #
    # # 鼠标右键放开
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    # 设置鼠标位置
    # win32api.SetCursorPos((x, y))
    #
    # # 键盘输入事件
    # win32api.keybd_event(VK_CODE[word], 0, 0, 0)
    # win32api.keybd_event(VK_CODE[word], 0, win32con.KEYEVENTF_KEYUP, 0)

    # # 获取窗口句柄
    # hwnd = win32gui.FindWindow(None, "飞书")
    # print(hwnd)
    #
    # # 将窗口移动到(100, 100)的位置
    # win32gui.MoveWindow(hwnd, 100, 100, 500, 400, True)
    #
    # # 关闭窗口
    # win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    #
    # # 打开窗口
    # win32gui.ShowWindow(0, hwnd)

    # 弹窗
    # win32api.MessageBox(0, "HELLO BAOZI!", 'pywin32', win32con.MB_OK)


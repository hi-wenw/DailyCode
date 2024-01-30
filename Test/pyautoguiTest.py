import time

import pyautogui

if __name__ == '__main__':
    # pyautogui.moveTo(157, 1067, duration=0.1)
    # pyautogui.click()
    # pyautogui.moveTo(311, 315, duration=0.1)
    # pyautogui.click()
    # pyautogui.moveTo(534, 870, duration=0.1)
    # pyautogui.click()
    # pyautogui.typewrite('Hello world!\n', interval=0.01)
    # pyautogui.hotkey('enter')
    while True:
        time.sleep(1)
        print(pyautogui.position())
        pyautogui.screenshot(r'my_screenshot.png')
        print(pyautogui.screenshot().getpixel((220, 200)))

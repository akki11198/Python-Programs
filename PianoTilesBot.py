from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while keyboard.is_pressed('q') == False:
    
    if pyautogui.pixel(779, 700)[0] == 0:
        click(779, 700)
    if pyautogui.pixel(898, 700)[0] == 0:
        click(898, 700)
    if pyautogui.pixel(1039, 700)[0] == 0:
        click(1039, 700)
    if pyautogui.pixel(1113, 700)[0] == 0:
        click(1113, 700)
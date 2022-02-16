from tempfile import TemporaryFile
from cefpython3 import cefpython as cef #web browsing
import os
import platform
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    print("PIL is not installed,")
    print('Install using: pip install Pillow')
    sys.exit(1)

def main(url, w, h):
    global VIEWPORT_SIZE, URL, SCREENSHOT_PATH
    URL = url
    VIEWPORT_SIZE = (w, h)
    SCREENSHOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'SCREENSHOT.png')
    


import tkinter as tk

root = tk.Tk()
root.geometry('400x200')

class Widget:
    def __init__(self, labtext, set_variable):
        self.lab = tk.Label(root, text=labtext)
        self.lab.pack()
        self.v = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.v)
        self.entry.pack()
        self.v.set(set_variable)


obj1 = Widget('Enter Website Name: ', 'https://www.google.com')
obj2 = Widget('Enter Width : ', '1024')
obj3 = Widget('Enter Height : ', '2048')
root.bind('<Return>', lambda x: main(obj1.v.get()), int(obj2.v.get()), int(obj3.v.get()))
lab4 = tk.Label(root, text='          ')
lab4.pack()

lab5 = tk.Label(root, text='Press the Enter Key to Create Screenshot')
lab5.pack()

root.mainloop()


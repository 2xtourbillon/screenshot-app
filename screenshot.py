from calendar import LocaleHTMLCalendar
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

    check_version()
    sys.excepthook = cef.ExceptHook() #all cef processes are shut down on error

    if os.path.exists(SCREENSHOT_PATH):
        print('Remove Old Screenshot')
        os.remove(SCREENSHOT_PATH)

    command_line_arguments()

    settings = {
        'windowless_rendering_enabled': True, #take screenshot of browser but don't open browser
    }

    switches = {
        'disable-gpu': "",
        'disable-pgu-compositing': "",
        'enable-begin-frame-scehduling': "",
        'disable-surfaces': "",
    }

    browser_settings = {
        'windowless_frame_rate': 30,
    }

    cef.Initialize(settings=settings, switches=switches)
    create_browser(browser_settings)
    cef.MessageLoop() #programming contruct for dispatching events/messages
    cef.Shutdown()
    print('Opening your screenshot with the default Application')
    open_with_default_application(SCREENSHOT_PATH)


def check_versions():
    ver = cef.GetVersion()
    print('CEF Python {ver} '.format(ver=ver['version']))
    print('Chromium {ver} '.format(ver=ver['chrome_version']))
    print('CEF {ver} '.format(ver=ver['cef_version']))
    print('Python {ver} {arch}'.format(ver=platform.python_version(), arch=platform.architecture()[0]))

    assert cef.__version__ >= '57.0', 'CEF Python v57.0+ required to run this.'


def command_line_arguments():
    if len(sys.argv) == 4:
        url = sys.argv[1]
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        #checking url
        if url.startswith('http://') or url.startswith('https://'):
            global URL
            URL = url
        else:
            print('Error: Invalid URL Entered')
            sys.exit(1)
        #checking w and h
        if width > 0 and height > 0:
            global VIEWPORT_SIZE
            VIEWPORT_SIZE = (width, height)
        else:
            print('Error: Invalid Width and Height!')
            sys.exit(1)
    elif len(sys.argv) < 1:
        print('Error: Expected Arguments Not Received!'
              'Expected Args are URL, Width and Height')

# creating browser in off-screen mode
def create_browser(settings):
    global VIEWPORT_SIZE, URL
    parent_window_handle = 0
    window_info = cef.WindowInfo()
    window_info.SetAsOffscreen(parent_window_handle)
    print('Viewport size: {size}'.format(size=str(VIEWPORT_SIZE)))
    print('Loading URL: {url}'.format(url=URL))
    
    browser = cef.CreateBrowserSync(window_info=window_info, settings=settings, url=URL)
    browser.SetClientHandler(LoadHandler())
    browser.SetClientHandler(RenderHandler())
    browser.SendFocusEvent(True)
    browser.WasResized()
    


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


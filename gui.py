import PySimpleGUI as sg
from service import startService
import threading
from time import sleep

from utils import get_service_on, set_service_on


def main():
    lock = threading.Lock()
    sg.theme('SystemDefault')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Button('开启服务', size=(20, 5), visible=True), sg.Button('关闭服务', size=(20, 5), visible=False)],
                [sg.Text('开启服务后，您的电脑将立即进入锁屏状态。')],
                [sg.Text('开启服务后，如果有人拔下电源，程序将会以最大音量发出报警。')] ]


    # Create the Window
    window = sg.Window('笔记本防盗报警', layout, margins=(20, 30))
    start_btn = window.FindElement('开启服务')
    terminate_btn = window.FindElement('关闭服务')

    service_task = threading.Thread(target=startService, args=(lock, ))

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == '开启服务': 
            print('Service On')
            start_btn.Update(visible=False)
            terminate_btn.Update(visible=True)
            set_service_on(True)
            service_task.start()
        if event == '关闭服务':
            print('Service Off')
            start_btn.Update(visible=True)
            terminate_btn.Update(visible=False)
            set_service_on(False)
            service_task = threading.Thread(target=startService, args=(lock, ))
        if event == sg.WIN_CLOSED:
            set_service_on(False)
            break
        # startService()


    window.close()
    exit(0)

if __name__ == '__main__':
    main()
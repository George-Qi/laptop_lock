import psutil
from playsound import playsound
from time import sleep
import multiprocessing

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from ctypes import *
from utils import set_service_on, get_service_on

print(psutil.sensors_battery().power_plugged)

def playAlarmSound():
    playsound('alarm_bell.mp3')


def setSoundMax():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(0, None)
    volume.SetMasterVolumeLevel(-20, None)

def lockScreen():
    user32 = windll.LoadLibrary('user32.dll')
    user32.LockWorkStation()

def startService(lock: multiprocessing.Lock):
    # lockScreen()
    while True:
        lock.acquire()
        flag_on = get_service_on()
        print(flag_on)
        lock.release()
        if (flag_on == False):
            break
        print('run...')
        power_plugged = psutil.sensors_battery().power_plugged
        if not power_plugged:
            print("Warning!!!")
            setSoundMax()
            playAlarmSound()
        sleep(1)
    print('over')
    sleep(10)
    return

if __name__ == '__main__':
    lock = multiprocessing.Lock()
    startService(lock)
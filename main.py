# -*- coding: utf-8 -*-
""" A Driver GUI PROGRAM

A MQTT driven simulator program to update car telemetrics

@author: Christy J Finny
@Organization University


"""
import argparse
import base64
from cProfile import run
import threading
import time
import os
import sys
import subprocess

import PySimpleGUI as Pg
import numpy as np
import paho.mqtt.client as pm

from constants import * 

# Key's for the GUI:
KEY_EXIT = '-EXIT-'
KEY_START = '-START-'
KEY_STOP = '-STOP-'
KEY_BATTERY = '-BATTERY-'
# KEY_BRAKE = '-BrakeL-'+ '-BrakeR-' # ----> if this is possible it can replace KEY_BRAKEL & KEY_BRAKER below
KEY_BRAKEL = '-BrakeL-'
KEY_BRAKER = '-BrakeR-'
KEY_SPEED = '-SPEED-'
KEY_ACCEL = '-ACCEL-'
KEY_MQTT = '-MQTT-'


# Colour template for the window, can be customized per component but much more compact and tidy with theme.
Pg.theme('LightBrown1')

# Columns for the layout; useful code for sizing images: subsample=
Battery_level = Pg.Column(
    [
        [
            Pg.Text('', pad=(0, 0), key='-LEFT-PLACEHOLDER-', size=(5, 0)),
            Pg.Image(key=KEY_BATTERY, enable_events=True, expand_x=True),
        ]
    ], size=(310, 300), justification='center')


Speed_level = Pg.Column(
    [
            [Pg.Text('', expand_x=True,expand_y=True)],
            [Pg.Text('', key=KEY_ACCEL, font='_ 10', size=(25, 1), background_color='white')],
            [Pg.Text('', key=KEY_SPEED, font='_ 80', expand_x=True, expand_y=True, background_color='white')],
            [
                Pg.Text('', size=(15, 1)),
                Pg.Text('km/h', font='_ 50')
            ]

            # Usable Base64 images:
            # Pg.Image(data=Speedometer_needle, key='-Speed-', visible=True),
            # Pg.Image(data=Speedometer_dial)

        ], size=(310, 300), justification='center')

# The layout for the GUI window
The_layout = [[
    Pg.Column([[Pg.Text('', key='-BrakeL-', size=(40, 28), background_color='red')]], size=(40, 480)),
    Pg.VSeparator(),
    Pg.Column([
        [Pg.Text('Welcome to the Driver UI Demo', expand_x=True, justification='center')],
        [
            Pg.Button('Start', key=KEY_START, expand_x=True, metadata=False),
            Pg.Button('Stop', key=KEY_STOP, expand_x=True, metadata=False),
            Pg.Button(' T E L E M E T R Y ', key=KEY_MQTT, expand_x=True, metadata=False),
            Pg.Button('Exit Program', key=KEY_EXIT, expand_x=True)
        ],
        [Battery_level, Speed_level],
        [Pg.HSeparator()],
        [
            Pg.Text('', pad=(0, 0), key='-LEFT-PLACEHOLDER-', expand_x=True),
            Pg.Image(data=Radio_Warning, enable_events=True, key='-Radio-Warning-'),
            Pg.Image(data=Hydro_Warning, enable_events=True, key='-Hydro-Warning-'),
            Pg.Image(data=Battery_Warning, enable_events=True, key='-Battery-Warning-'),
            Pg.Image(data=Signal_Warning, enable_events=True, key='-Signal-Warning-'),
            Pg.Image(data=Steering_Warning, enable_events=True, key='-Steering-Warning-'),
            Pg.Text('', pad=(0, 0), key='-RIGHT-PLACEHOLDER-', expand_x=True)
        ],
    ]),
    Pg.VSeparator(),
    Pg.Column([[Pg.Text('', key='-BrakeR-', size=(40, 28), background_color='red')]], size=(40, 480))
]]

# The Setup for the window itself, must go after layout, so it can refer to the The_layout label
window_main = Pg.Window('', The_layout, grab_anywhere=True, no_titlebar=True,
                        size=(800, 480), location=(400,240), finalize=True)

# Removes the cursor from the GUI, requires the finalize option in the window setup code to be True, set to 'None' or ''
window_main.set_cursor(cursor='')


# Variables and Arrays for loops below:

StateList = (
    Battery_0, Battery_14, Battery_29, Battery_43, Battery_57, Battery_71, Battery_86, Battery_100, Battery_Charging,
    Battery_Setup
)
WarningList = (
    '-Radio-Warning-', '-Hydro-Warning-', '-Battery-Warning-', '-Signal-Warning-', '-Steering-Warning-'
)
WarningList_Default = (
    Radio_Warning, Hydro_Warning, Battery_Warning, Signal_Warning, Steering_Warning
)
WarningList_True = (
    Radio_Warning_True, Hydro_Warning_True, Battery_Warning_True, Signal_Warning_True, Steering_Warning_True
)
WarningList_False = (
    Radio_Warning_False, Hydro_Warning_False, Battery_Warning_False, Signal_Warning_False, Steering_Warning_False
)


# All the functions needed:
class BaseThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
        self._stop_event = threading.Event()
        self._interval = 0

    def run(self):
        raise NotImplementedError

    def terminate(self):
        self._running = False

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class GUIUpdateThread(BaseThread):

    def __init__(self, wait=1):
        super(GUIUpdateThread, self).__init__()
        self._wait = wait
        self.name = "gui_update"

    def run(self):
        toggle = False
        while self._running:
            for i, _ in enumerate(StateList):
                time.sleep(self._wait)
                data = StateList[i]
                window_main[KEY_BATTERY].update(data=data)
                window_main[KEY_BRAKEL].update(visible=toggle)
                window_main[KEY_BRAKER].update(visible=toggle)
                toggle = not toggle
                is_killed = self._stop_event.wait(self._interval)
                if is_killed:
                    break


class SpeedAdjustorThread(BaseThread):

    def __init__(self, wait=0.2):
        super(SpeedAdjustorThread, self).__init__()
        self._wait = wait 
        self.name = "speed_adjuster"

    def run(self):
        toggle = False
        while self._running:
            for i in range(30):
                time.sleep(self._wait)
                window_main[KEY_SPEED].update(i)
                toggle = not toggle
                is_killed = self._stop_event.wait(self._interval)
                if is_killed:
                    break


class AccelAdjustorThread(BaseThread):

    def __init__(self, wait=0.1):
        super(AccelAdjustorThread, self).__init__()
        self._wait = wait
        self.name = "accel_adjustor"

    def run(self):
        toggle = False
        while self._running:
            for i in range(100):
                time.sleep(self._wait)
                window_main[KEY_ACCEL].update('Current Acceleration torque: '+str(i)+'%')
                toggle = not toggle
                is_killed = self._stop_event.wait(self._interval)
                if is_killed:
                    break


class WarningThread(BaseThread):

    def __init__(self, wait=1):
        super(WarningThread, self).__init__()
        self._wait = wait
        self.name = "warning"

    def run(self):
        yl = 0
        while self._running:
            for a, _ in enumerate(WarningList):
                if yl == 3:
                    yl = 0
                time.sleep(self._wait)
                order = (WarningList_True[a], WarningList_False[a], WarningList_Default[a])
                data = order[yl]
                window_main[WarningList[a]].update(data=data)
                if a == len(WarningList) - 1:
                    yl = yl + 1
                is_killed = self._stop_event.wait(self._interval)
                if is_killed:
                    break


def init():
    window_main[KEY_BATTERY].update(data=StateList[9])
    window_main[KEY_STOP].update(disabled=True)
    window_main[KEY_START].update(disabled=False)
# window_main.write_event_value('-THREAD-', 'DONE')  # put a message into queue for GUI


# For windows:
#subprocess.call('start cmd.exe @cmd /k python Speed_readings.py', shell=True)
#subprocess.call('start cmd.exe @cmd /k python Battery_readings.py', shell=True)
#subprocess.call('start cmd.exe @cmd /k python Accel_readings.py', shell=True)
#time.sleep(1)
#subprocess.call('start cmd.exe @cmd /k python Raspberry_data_collector.py', shell=True)
# For Raspberry pi:
# subprocess.call('lxterminal -e python3.10 Speed_readings.py', shell=True)
# subprocess.call('lxterminal -e python3.10 Battery_readings.py', shell=True)
# subprocess.call('lxterminal -e python3.10 Accel_readings.py', shell=True)
# time.sleep(1)
# subprocess.call('lxterminal -e python3.10 Raspberry_data_collector.py', shell=True)
    
# Main Loop:
def main():
    init()
    while True:

        gui_update = GUIUpdateThread()
        speed_adjustor = SpeedAdjustorThread()
        warning = WarningThread()
        accel_adjustor = AccelAdjustorThread()
        threads = []
        threads.extend([gui_update, speed_adjustor, warning, accel_adjustor])

        event, values = window_main.read()
        
        if event == Pg.WIN_CLOSED or event == KEY_EXIT:
            print('Closed from exit button')
            window_main.close()
            sys.exit(0)

        elif event == KEY_START:
            window_main[KEY_STOP].update(disabled=False)
            window_main[KEY_START].update(disabled=True)

            for t in threads:
                t.setDaemon(True)
                t.start()

        elif event == KEY_STOP:
            window_main[KEY_START].update(disabled=False)
            window_main[KEY_STOP].update(disabled=True)

            for t in threads:
                t.stop()
               # t.join()
            


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        window_main.close()

  



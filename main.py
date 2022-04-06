# Welcome to the script ^^

# GitHub test

# This code uses PySimpleGUI, it could end up using PySimpleGUIQt for overlap on speed

# Cause overlaps, animate, function for battery image change and brake alert, next organise MQTT, next organise USB

# All the modules you will need to run the GUI:
from concurrent.futures import thread
import PySimpleGUI as Pg
# import PySimpleGUIQt
# import PySimpleGUIQt as PgQ
# import PyQt5.QtGui as PqG
# import PyQt5.QtWidgets as PqW
# import PySide2.QtGui as PsG
import paho.mqtt.client as pm
# Other essential  modules:
import base64
import threading
import time
import os
import sys
import subprocess

from constants import *

# Key's for the GUI
KEY_EXIT = '-EXIT-'
KEY_TEST = '-TEST-'
KEY_BATTERY = '-BATTERY-'
# KEY_BRAKE = '-BrakeL-', '-BrakeR-' ----> if this is possible it can replace KEYS below
KEY_BRAKEL = '-BrakeL-'
KEY_BRAKER = '-BrakeR-'

# Colour template for the window, can be customized per component but much more compact and tidy with theme.
Pg.theme('LightBrown1')

# Columns that contains two levels and images; useful code for sizing images: subsample=
# Brake = Pg.Column([[Pg.Text('', key='-Brake-', size=(3, 30), background_color='red')]])
Battery_level = Pg.Column(
    [
        [
            Pg.Text('', pad=(0, 0), key='-LEFT-PLACEHOLDER-', size=(5, 0)),
            Pg.Image(key=KEY_BATTERY, enable_events=True, expand_x=True),
        ]
    ], size=(310, 300), justification='center')

########################################################################################################################################################################
# ---------------------Warning! Test Zone--------------------- #

# gig = PsG.QPixmap()
# gig.loadFromData(base64.b64decode(Speedometer_dial))


# app = PgQ.QApplication([])
# Without ^ the program returns exit code -1073740791 (0xC0000409)

# w = PgQ.QWidget()
# pic = PgQ.QLabel(w)
# pm = PgQ.QPixmap()
# pm.loadFromData(base64.b64decode(Speedometer_needle))
# pic.setPixmap(pm)
# w.show()
# app.exec_()


# ---------------------Warning! Test Zone--------------------- #
########################################################################################################################################################################

########################################################################################################################################################################
# ---------------------Warning! Test Zone--------------------- #
# Speedometer = PgQ.Tree ([
#     PgQ.QPainter(data=Speedometer_needle)
#     # error: must be an iterable, not NoneType
#     # Column is not a parent type container, need to use one to host childern elements
#     ])
# ---------------------Warning! Test Zone--------------------- #
########################################################################################################################################################################

Speed_level = Pg.Column(
    [
        [
            Pg.Text('', pad=(0, 0), key='-LEFT-PLACEHOLDER-', size=(2, 19)),

            ########################################################################################################################################################################
            # ---------------------Warning! Test Zone--------------------- #

            # w.show(),
            # [Speedometer],
            # print(dir(Speedometer)),
            # ---------------------Warning! Test Zone--------------------- #
            ########################################################################################################################################################################

            Pg.Image(data=Speedometer_needle, key='-Speed-', visible=True),
            Pg.Image(data=Speedometer_dial)
        ]
    ], size=(310, 300), justification='center')

# The layout for the GUI window
The_layout = [[
    Pg.Column([[Pg.Text('', key='-BrakeL-', size=(40, 28), background_color='red')]], size=(40, 480)),
    Pg.VSeparator(),
    Pg.Column([
        [Pg.Text('Welcome to the Driver UI Demo', expand_x=True, justification='center')],
        [
            Pg.Button('Run Program', key=KEY_TEST, expand_x=True, metadata=False),
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
                        size=(800, 480), location=(0, 0), finalize=True)

## The placeholders to centralize the warning buttons
## The_Main_Window['-LEFT-PLACEHOLDER-'].expand(True, True, True)
## The_Main_Window['-RIGHT-PLACEHOLDER-'].expand(True, False, True)

# Removes the cursor from the GUI, requires the finalize option in the window setup code to be True, set to 'None' or ''
window_main.set_cursor(cursor='')

# Variables and Arrays for loops below
# toggle = False
Test_Variable = 0
stop_threads = False

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



def guiupdater(wait=1):
    toggle = False
    while stop_threads == False:
        for i, _ in enumerate(StateList):
            time.sleep(wait)
            data = StateList[i]
            window_main[KEY_BATTERY].update(data=data)
            window_main[KEY_BRAKEL].update(visible=toggle)
            window_main[KEY_BRAKER].update(visible=toggle)
            toggle = not toggle
        if stop_threads:
            break

class Warning(threading.Thread):
    def __init__(self):
        threading.Thread.__init__()
        self.name = "Warning"
        self.stop_threads = True

    def run(self):
        y1 = 0
        while self.stop_threads:
            for a, _ in enumerate(WarningList):
                if yl == 3:
                    yl = 0
            time.sleep(self.wait)
            order = (WarningList_True[a], WarningList_False[a], WarningList_Default[a])
            data = order[yl]
            window_main[WarningList[a]].update(data=data)
            if a == len(WarningList) - 1:
                yl = yl + 1

    


    # ---------------------Incomplete Step warning function--------------------- #
    # while True:
    #     for a, _ in enumerate(WarningList):
    #         print('Max should be', len(WarningList))
    #         print('a is ', a)
    #         print(WarningList[a])
    #         time.sleep(wait)
    #         default_data = WarningList_Default[a]
    #         true_data = WarningList_True[a]
    #         false_data = WarningList_False[a]
    #         print('data is ', default_data)
    #         print('data is ', true_data)
    #         print('data is ', false_data)
    #         if True:
    #             window_main[WarningList[a]].update(data=default_data)
    #             print('test')
    #         if a >= 1:
    #             window_main[WarningList[a]].update(data=true_data)
    #             print('test1')
    #         if a >= 2:
    #             window_main[WarningList[a]].update(data=false_data)
    #             print('test2')
    #         else:
    #             print('passed')
    #             continue


def init():
    window_main[KEY_BATTERY].update(data=StateList[9])
    stop_threads = False


# window.write_event_value('-THREAD-', 'DONE')  # put a message into queue for GUI

# All the loops needed:
# For windows:
# subprocess.call('start cmd.exe @cmd /k python3 Speed_readings.py', shell=True)
# subprocess.call('start cmd.exe @cmd /k python3 Battery_readings.py', shell=True)
# subprocess.call('start cmd.exe @cmd /k python3 Raspberry_data_collector.py', shell=True)
# For Raspberry pi:
subprocess.call(['gnome-terminal', '-X', 'python3 Speed_readings.py'], shell=True)
subprocess.call(['gnome-terminal', '-X', 'python3 Battery_readings.py'], shell=True)
subprocess.call(['gnome-terminal', '-X', 'python3 Raspberry_data_collector.py'], shell=True)

init()
while True:

    event, values = window_main.read()
    # ---------------------Maintenance loop and exit function--------------------- #
    if event == KEY_EXIT:
        print('Closed from exit button')
        window_main.close()
        sys.exit(0)
    # ---------------------Multithreading testing Protocol--------------------- #
    elif event == KEY_TEST:
        if window_main[KEY_TEST].metadata == False:
            print('Test Button Pressed, starting demo')
            threading.Thread(target=guiupdater, daemon=True).start()
            threading.Thread(target=warning, daemon=True).start()
            window_main[KEY_TEST].metadata = not window_main[KEY_TEST].metadata
        elif window_main[KEY_TEST].metadata == True:
            print('Test Button Pressed, stopping demo')
            stop_threads = True
            threading.Thread(target=guiupdater, daemon=True).join()
            threading.Thread(target=warning, daemon=True).join()
            window_main[KEY_TEST].metadata = not window_main[KEY_TEST].metadata
    # ---------------------Single step testing Protocol--------------------- #
    # if event == 'Test':
    #     print('LEN is ', len(StateList))
    #     print('RANGE is ', range(len(StateList)))
    #     print('State BASE64 code is ', StateList[Test_Variable])
    #     print('Unit is currently ', Test_Variable)
    #     if Test_Variable < len(StateList):
    #         print('Unit is currently ', Test_Variable)
    #
    #         window_main[KEY_BATTERY].update(data=StateList[Test_Variable])
    #
    #         window_main['-BrakeL-'].update(visible=toggle)
    #         window_main['-BrakeR-'].update(visible=toggle)
    #         toggle = not toggle
    #
    #         # The_Main_Window['-Speed-'].update(data=StateList[Test_Variable])
    #
    #         # The_Main_Window[ the warning lights ]
    #
    #         print('GUI should now be updated')
    #         Test_Variable = Test_Variable + 1
    #         print('Unit is now ', Test_Variable)
    #     if Test_Variable == len(StateList):
    #         print('This Array has run out, will reset the function now')
    #         Test_Variable = 0
    #         print('Unit is now ', Test_Variable)
    #         continue

window_main.close()
#
#
#
# ---------------------|End of GUI|--------------------- #

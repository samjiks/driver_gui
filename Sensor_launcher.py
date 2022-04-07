import subprocess

subprocess.call('start cmd.exe @cmd /k python3 Speed_readings.py', shell=True)
subprocess.call('start cmd.exe @cmd /k python3 Battery_readings.py', shell=True)
subprocess.call('start cmd.exe @cmd /k python3 Accel_readings.py', shell=True)

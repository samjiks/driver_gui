import paho.mqtt.client as pm
import time

try:
    Broker = "localhost"
    client = pm.Client('BATTERY_LEVEL',0)
    client.connect(Broker)

    while True:

        for Current_Battery_Level in range(0, 113):
            client.publish('BatteryLevel', 'battery Percentage is  ' + str(Current_Battery_Level))
            print('Just published the battery level as', str(Current_Battery_Level), 'to the topic BATTERY_LEVEL')
            time.sleep(1)

except KeyboardInterrupt:
    print('KeyPress detected, closing')
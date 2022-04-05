import paho.mqtt.client as pm
import time

try:
    Broker = "192.168.0.33"
    client = pm.Client('BATTERY_LEVEL', 0)
    client.connect(Broker)

    while True:
        for Current_Battery_Level in range(0, 113):
            # client.publish('$SYS/broker/clients/connected/BatteryLevel', str(Current_Battery_Level))
            # client.publish('BatteryLevel', str(Current_Battery_Level))
            client.publish('BatteryLevel', str(Current_Battery_Level))
            print('Just published the battery level as', str(Current_Battery_Level), 'to the topic BATTERY_LEVEL')
            time.sleep(1)

except KeyboardInterrupt:
    print('KeyPress detected, closing')
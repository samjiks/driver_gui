import paho.mqtt.client as pm
import time

try:
    Broker = "localhost"
    client = pm.Client('ACCEL_LEVEL', 2)
    client.connect(Broker)

    while True:
        for Current_Accel_Level in range(0, 100):
            # client.publish('$SYS/broker/clients/connected/BatteryLevel', str(Current_accel_Level))
            # client.publish('AccelLevel', str(Current_Battery_Level))
            client.publish('BatteryLevel', str(Current_Battery_Level))
            print('Just published the battery level as', str(Current_Accel_Level), 'to the topic accel_LEVEL')
            time.sleep(1)

except KeyboardInterrupt:
    print('KeyPress detected, closing')
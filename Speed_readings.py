import paho.mqtt.client as pm
import time

try:
    Broker = "localhost"
    client = pm.Client('SPEED_LEVEL', 1)
    client.connect(Broker)

    # [('BatteryLevel',0), ('SpeedLevel', 1)]

    while True:
        for Current_Speed in range(0, 30):
            client.publish('$SYS/broker/clients/connected/SpeedLevel', str(Current_Speed))
            print('Just published the speed level as', str(Current_Speed), 'to the topic SPEED_LEVEL')
            time.sleep(1)

except KeyboardInterrupt:
    print('KeyPress detected, closing')
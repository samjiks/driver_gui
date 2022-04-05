import paho.mqtt.client as pm
import time

try:
    Broker = "192.168.0.33"
    client = pm.Client('ACCEL_LEVEL', 2)
    client.connect(Broker)

    while True:
        for Current_Accel_Level in range(0, 100):
            # client.publish('$SYS/broker/clients/connected/AccelLevel', str(Current_Accel_Level))
            # client.publish('AccelLevel', str(Current_Accel_Level))
            client.publish('AccelLevel', str(Current_Accel_Level))
            print('Just published the accel level as', str(Current_Accel_Level), 'to the topic ACCEL_LEVEL')
            time.sleep(1)

except KeyboardInterrupt:
    print('KeyPress detected, closing')
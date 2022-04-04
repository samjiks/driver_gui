import paho.mqtt.client as pm
import time

Broker = "localhost"
client = pm.Client('BATTERY_LEVEL')
client.connect(Broker)

while True:
    for Current_Battery_Level in range(2, 113):
        client.publish('BatteryLevel', Current_Battery_Level)
        print('Just published the battery level as', str(Current_Battery_Level), 'to the topic BATTERY_LEVEL')

        time.sleep(5)



#client.on_message =
# client.on_connect = connection_test()
# client.on_log = data_logger()


# client.loop_start()
# time.sleep(50)
# client.loop_stop()
# client.disconnect()
import paho.mqtt.client as pm
import time



# ---------------------|Start of MQTT Subscription|--------------------- #
#
#
#
def connection_test(client, userdata, flags, rc):
    if rc==0:
        print('Connected successfully')
    else:
        print('Unable to connect, Returned code was =', rc)

# def data_logger(client, userdata, level, buf):
#     print('Log: '+buf)

def on_message(client, userdata, message):
    print('Apparently the battery level is ', str(message.payload.decode("utf-8")))

# def simple(client, userdata, flags, rc):
#     print('connection achieved')

Broker = 'localhost'
client = pm.Client('RaspberryPi')
client.connect(Broker)

client.loop_start()

client.subscribe('BatteryLevel')

client.on_message = on_message
# client.on_connect = simple
client.on_connect = connection_test
# client.on_log = data_logger

time.sleep(80)
client.loop_stop()
#
#
#
# ---------------------|End of MQTT Subscription|--------------------- #

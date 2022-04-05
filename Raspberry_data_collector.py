import paho.mqtt.client as pm
import time
import sys


try:
    # ---------------------|Start of MQTT Subscription|--------------------- #
    #
    #
    #

    # Packet ID:
    # Battery = 0
    # Speed = 1

    def connection_test(client, userdata, flags, rc):
        if rc == 0:
            ConnectionFlag = True
            print('Connected successfully')
        else:
            print('Unable to connect to Broker, Returned code was =', rc)
            ConnectionFlag = False
            sys.exit(1)

    def data_logger(client, userdata, level, buf):
        print('Log: ' + buf)

    def the_message(client, userdata, message):
        print('The value of the', print(client), 'is ', str(message.payload.decode("utf-8")))

    ConnectionFlag = False
    Broker = 'localhost'
    RPSubscriber = pm.Client('RaspberryPi')
    RPSubscriber.connect(Broker)

    print('connecting to the Broker')

    # RPSubscriber.subscribe([('$SYS/broker/clients/connected/BatteryLevel', 0), ('$SYS/broker/clients/connected/SpeedLevel', 1)])
    # RPSubscriber.subscribe([('BatteryLevel', 0), ('SpeedLevel', 1)])
    RPSubscriber.subscribe([('BatteryLevel', 0), ('SpeedLevel', 1)])

    RPSubscriber.on_connect = connection_test
    RPSubscriber.on_log = data_logger
    RPSubscriber.on_message = the_message

    if RPSubscriber.is_connected() == False:
        RPSubscriber.loop_forever()
    else:
        RPSubscriber.disconnect()
        sys.exit(1)
    print('wat..')
    #
    #
    #
    # ---------------------|End of MQTT Subscription|--------------------- #

except KeyboardInterrupt:
    print('KeyPress detected, closing')
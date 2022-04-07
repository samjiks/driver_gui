import paho.mqtt.client as pm
import pandas as pd
import time
import sys

global TheValues

Shared_Battery = 0
Shared_Speed = 0
Shared_Accel = 0
TheValues = [Shared_Battery, Shared_Speed, Shared_Accel]


try:
    # ---------------------|Start of MQTT Subscription|--------------------- #
    #
    #
    #

    # Packet ID:
    # Battery = 0
    # Speed = 1
    # Accel = 2


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
        value = str(message.payload.decode("utf-8"))
        print('The value of the', print(client), 'is ', value)
        if message.topic == "BatteryLevel":
            global Shared_Battery
            Shared_Battery = value
        elif message.topic == "SpeedLevel":
            global Shared_Speed
            Shared_Speed = value
        elif message.topic == "AccelLevel":
            global Shared_Accel
            Shared_Accel = value
        global TheValues
        TheValues = [Shared_Battery, Shared_Speed, Shared_Accel]
        print(value)
        print(TheValues)


    ConnectionFlag = False
    Broker = 'localhost'
    RPSubscriber = pm.Client('RaspberryPi')
    try:
        RPSubscriber.connect(Broker)
    except:
        print('Unable to find the Broker, please check address')
        sys.exit()

    print('connecting to the Broker')

    # RPSubscriber.subscribe([('$SYS/broker/clients/connected/BatteryLevel', 0), ('$SYS/broker/clients/connected/SpeedLevel', 1)])
    # RPSubscriber.subscribe([('BatteryLevel', 0), ('SpeedLevel', 1)])
    RPSubscriber.subscribe([('BatteryLevel', 0), ('SpeedLevel', 1), ('AccelLevel', 2)])

    RPSubscriber.on_connect = connection_test

    # RPSubscriber.on_log = data_logger
    RPSubscriber.on_message = the_message
    print(TheValues)
    print(TheValues[1])

    col1 = "Battery"
    col2 = "Speed"
    col3 = "Acceleration"

    my_dict= {'Battery': TheValues[0], 'Speed': TheValues[1], 'Acceleration': TheValues[2]}
    data = pd.DataFrame([my_dict])
    data.to_excel('Book1.xlsx', sheet_name='Sheet1')

    # open('ArraySheet.txt','w').write(TheValues)
    if not RPSubscriber.is_connected():
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
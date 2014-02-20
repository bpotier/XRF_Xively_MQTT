#!/usr/bin/python
import mosquitto
import os
import time
import serial
import datetime
import re
import eeml

broker = "127.0.0.1"
tcpport = 1883
baud = 9600
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)

#XIVELY details
#Change values according to your XIVELY config
######################################################################
XIVELYMQTTServer = "api.xively.com" 
XIVELYAPIKey ="IvUMMwND4OsBfXhO0WmIq1XwbOpGs1HGHTEkLw9KTTqpdc18"
XIVELYFeed = 41913791
XIVELYUrl = '/v2/feeds/{feednum}.xml' .format(feednum = XIVELYFeed)
######################################################################

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#Connect to broker
mqttc.connect(broker, tcpport, 60, True)

#Remain connected and publish
while mqttc.loop() == 0:
        llapMsg = ser.read(12)
        mqttc.publish("TempSensors", llapMsg)
        devID = llapMsg[1:3]

        if re.search("a01TMPA", llapMsg):
                temp = llapMsg[7:12]
                xively = eeml.Pachube(XIVELYUrl, XIVELYAPIKey)
                xively.update([eeml.Data(devID + "_Exterieur", temp, unit=eeml.Celsius())])

        if re.search("a02TMPA", llapMsg):
                temp = llapMsg[7:12]
                xively = eeml.Pachube(XIVELYUrl, XIVELYAPIKey)
                xively.update([eeml.Data(devID + "_Chambre", temp, unit=eeml.Celsius())])

        #Push data to XIVELY
        try:
                xively.put()

        except:
                print("ERROR : Failed to Send...")

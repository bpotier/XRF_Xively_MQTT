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

#cosm details
XIVELYMQTTServer = "api.xively.com"
XIVELYAPIKey ="IvUMMwND4OsBfXhO0WmIq1XwbOpGs1HGHTEkLw9KTTqpdc18"
XIVELYFeed = 41913791
XIVELYUrl = '/v2/feeds/{feednum}.xml' .format(feednum = XIVELYFeed)

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#connect to broker
#print "Connect to MQTT Broker..."
mqttc.connect(broker, tcpport, 60, True)

#remain connected and publish
while mqttc.loop() == 0:
        llapMsg = ser.read(12)
        mqttc.publish("TempSensors", llapMsg)
        devID = llapMsg[1:3]
#       xively = eeml.Pachube(XIVELYUrl, XIVELYAPIKey)
#       temp = llapMsg[7:12]

        if re.search("a01TMPA", llapMsg):
                temp = llapMsg[7:12]
                xively = eeml.Pachube(XIVELYUrl, XIVELYAPIKey)
                #send data to XIVELY
                xively.update([eeml.Data(devID + "_Exterieur", temp, unit=eeml.Celsius())])
#                print("XIVELY updated "+devID+"_Exterieur with value: "+temp)

        if re.search("a02TMPA", llapMsg):
                temp = llapMsg[7:12]
                xively = eeml.Pachube(XIVELYUrl, XIVELYAPIKey)
                #send data to XIVELY
                xively.update([eeml.Data(devID + "_Chambre", temp, unit=eeml.Celsius())])
#                print("XIVELY updated "+devID+"_Chambre with value: "+temp)

        #Push data to cosm
        try:
                xively.put()

        except:
                print("ERROR : Failed to Send...")

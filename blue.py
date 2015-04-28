import os 
import time
import RPi.GPIO as GPIO
import requests
import serial
import pickle
#AC/Heater range [18,45]

def toBool(inpBool):
	if (inpBool == "true"):
		return True
	return False

# BCM for GPIO pins (read nos in rectangles)
GPIO.setmode(GPIO.BCM)

# Set pins for usage
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

#serialData = serial.Serial('/dev/ttyUSB0',9600)							# BEWARE use lsusb to see bus number (USB0/ USB1....)

countRoomEmpty = 0 		# Number of seconds for which nobody in room
roomIsEmpty = 0 		# If room empty: 1, else: 0
# nosPeople = 0 			# Number of people in the room

applianceGPIO = [18, 23, 24, 25] 											#Assuming 4 appliances on 18,23,24,25 respectively
applianceName = {18:'Fridge', 23:'Garage Opener', 24:'Charger', 25:'Oven'}
applianceOn = [True, True, True, True] 										#Tells whether appliance is ON or OFF
requests.post("http://1.1.1.4:3000/postApp",params={'0':applianceOn[0], '1':applianceOn[1], '2':applianceOn[2], '3':applianceOn[3]})	# Get Appliance State

set_temp = 25 #Temperature required
ac_temp = 25 #Operating temperature of AC at any given time
ac_incriment = 0 #REquired change in ac_temp to achieve desired temperature
previously = 0 #Number of people in the room before scanning the file

while(1):
	try:
		#tempSensor = int(serialData.readline().split(" ")[0][:-3])
		#humSensor = int(serialData.readline().split(" ")[1][:-4])
		# requests.post("http://1.1.1.4:3000/temp",params={'temp':tempSensor, 'humidity':humSensor})			# Post Temp, Hum
		# print tempSensor	
		# print humSensor

		set_temp = int(requests.get("http://1.1.1.4:3000/atb")._content) 									#The temperature user wants

		applianceOn = requests.get("http://1.1.1.4:3000/data")._content.split(",")							# Get Appliance State
		print "Appliance On: " + str(applianceOn)

		nosPeople = int(requests.get("http://1.1.1.4:3000/nosPeople2")._content)
		print "Nos of People: " + str(nosPeople)

		for i in range(4):
			if (applianceOn[i] == 'false'):
				GPIO.output(applianceGPIO[i], GPIO.LOW)
			else:
				GPIO.output(applianceGPIO[i], GPIO.HIGH)	

		if(nosPeople == 0):
			if(not roomIsEmpty):
				countRoomEmpty = countRoomEmpty + 1
			else:
				countRoomEmpty = 0
		else:
			if(roomIsEmpty==1):
				print "Powering up"

		print countRoomEmpty
		# Power Down if no people for >= 4sec
		if(countRoomEmpty == 4):
			print "Powering Down"
			for i in range(4):
				GPIO.output(applianceGPIO[i],GPIO.LOW)
				applianceGPIO[i] = 'false'
			countRoomEmpty = 0	
			roomIsEmpty = 1

		# # If fire, Sound Alarm, Power all devices down
		# if(tempSensor > 60.0):
		# 	print "Fire! Run!"
		# 	for i in range(4):
		# 		GPIO.output(applianceGPIO[i],GPIO.LOW)
		# 	break

		# if(roomIsEmpty != 1):
		# 	if (tempSensor < set_temp):
		# 		ac_incriment = 1

		# 	elif (tempSensor > set_temp):
		# 		ac_incriment = -1

		# 	if (nosPeople > previously+7): 		#More than 7 people entering should cause a sufficient change in room temperature because of body heat
		# 		ac_incriment = ac_incriment - 1
			
		# 	if (ac_temp > 17 and ac_temp < 46):
		# 		ac_temp = ac_temp + ac_incriment
		# 		tempSensor = tempSensor + ac_incriment

		# 	nosPeople = nosPeople
		requests.post("http://1.1.1.4:3000/actempblue",params={'actemp':ac_temp}) #Current temperature the AC is set at.
		time.sleep(0.5)
		previously=nosPeople
	except:
		pass
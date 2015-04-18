import bluetooth
import os 
import time
import RPi.GPIO as GPIO
import requests
import serial
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
roomIsEmpty = 1 		# If room empty: 1, else: 0
nosPeople = 0 			# Number of people in the room

applianceGPIO = [18, 23, 24, 25] 											#Assuming 4 appliances on 18,23,24,25 respectively
applianceName = {18:'Fridge', 23:'Garage Opener', 24:'Charger', 25:'Oven'}
applianceOn = [True, True, True, True] 										#Tells whether appliance is ON or OFF
requests.post("http://1.1.1.4:3000/postApp",params={'0':applianceOn[0], '1':applianceOn[1], '2':applianceOn[2], '3':applianceOn[3]})	# Get Appliance State


set_temp = 25 #Temperature required
ac_temp = 25 #Operating temperature of AC at any given time
ac_incriment=0 #REquired change in ac_temp to achieve desired temperature
user_perm=0 #Defines permission of user


while(1):
	try:
		user_perm=0 #0 by default
		# Get data from Arduino DHT11
		#tempSensor = int(serialData.readline().split(" ")[0][:-3])
		#humSensor = int(serialData.readline().split(" ")[1][:-4])
		# requests.post("http://1.1.1.4:3000/temp",params={'temp':tempSensor, 'humidity':humSensor})			# Post Temp, Hum
		# print tempSensor
		# print humSensor

		set_temp=int(requests.get("http://localhost:3000/atb")._content) #The temperature user wants
		arrMAC = bluetooth.discover_devices()																# add parameter duration = secToScan if needed
		
		requests.post("http://1.1.1.4:3000/",params={'bmac':arrMAC})										# Post bluetooth																															
		print arrMAC
		
		arrName = namerequests.get("http://1.1.1.4:3000/data")._content.split(",")							# Get Names of people

		applianceOn = requests.get("http://1.1.1.4:3000/data")._content.split(",")							# Get Appliance State
		print applianceOn
		if (applianceOn[0] == False):
			GPIO.output(applianceGPIO[0], GPIO.LOW)
			print "0 Off"
		else:
			GPIO.output(applianceGPIO[0], GPIO.HIGH)
			print "0 On"

		if (applianceOn[1] == False):
			GPIO.output(applianceGPIO[1], GPIO.LOW)
		else:
			GPIO.output(applianceGPIO[1], GPIO.HIGH)

		if (applianceOn[2] == False):
			GPIO.output(applianceGPIO[2], GPIO.LOW)
		else:
			GPIO.output(applianceGPIO[2], GPIO.HIGH)

		if (applianceOn[3] == False):
			GPIO.output(applianceGPIO[0], GPIO.LOW)
		else:
			GPIO.output(applianceGPIO[0], GPIO.HIGH)

		

		# if(len(arrMAC) == 0):
		# 	if(not roomIsEmpty):
		# 		# print " * Nobody Home"
		# 		countRoomEmpty+=1
		# 	else:
		# 		countRoomEmpty=0
		# else:
		# 	if(roomIsEmpty==1):
		# 		print "Powering up"

		# 		# print "Power up A/C & lights"
		# 		for i in range(4):
		# 			GPIO.output(applianceGPIO[i],GPIO.HIGH)
		# 		#Update data on server

		# 	roomIsEmpty=0

		# # Power Down if no people for >= 4sec
		# if(countRoomEmpty == 4):
		# 	print "Powering Down"
		# 	for i in range(4):
		# 		GPIO.output(applianceGPIO[i],GPIO.LOW)

		# 	countRoomEmpty = 0	
		# 	roomIsEmpty = 1

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

		# 	if (nosPeople > len(arrMAC)+7): 		#More than 7 people entering should cause a sufficient change in room temperature because of body heat
		# 		ac_incriment = ac_incriment - 1
			
		# 	if (ac_temp > 17 and ac_temp < 46):
		# 		ac_temp = ac_temp + ac_incriment
		# 		tempSensor = tempSensor + ac_incriment

		# 	nosPeople = len(arrMAC)
		requests.post("http://localhost:3000/actempblue",params={'actemp':ac_temp}) #Current temperature the AC is set at.
		time.sleep(0.5)
		
	except:
		pass

import bluetooth
import os 
import time
import RPi.GPIO as GPIO
#import requests
import serial
#AC/Heater range [18,45]


# BCM for GPIO pins (read nos in rectangles)
GPIO.setmode(GPIO.BCM)

# Set pins for usage
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)



countRoomEmpty = 0 		# Number of seconds for which nobody in room
roomIsEmpty = 1 		# If room empty: 1, else: 0
nosPeople = 0 			# Number of people in the room

applianceGPIO = [18, 23, 24, 25] 										#Assuming 4 appliances on 18,23,24,25 respectively
applianceName = {18:'Fridge', 23:'Music System', 24:'Laptop Charger', 25:'Oven'}
applianceOn = [0, 0, 0, 0] 												#Tells whether appliance is ON or OFF

signal = 5 																# 1-indexing : + means ON,-ve means OFF ??
																		# Value 5 means no change to be done
																		# Used 1-indexing as +/-ve 0 make no sense

set_temp = 25
ac_temp = 25

ac_incriment=0

# send_to_server={'temp':inside_temp,'appliances[]':applianceOn } #Server Part
# r=requests.get('http://localhost:3000',params=...) #:-?
# s=requests.post("http://localhost:3000",data=send_to_server)

while(1):
	try:
		# Get data from Arduino DHT11
		serialData = serial.Serial('/dev/ttyUSB0',9600)							# BEWARE use lsusb to see bus number (USB0/ USB1....)
		tempSensor = int(serialData.readline().split(" ")[0][:-3])
		humSensor = int(serialData.readline().split(" ")[1][:-4])

		arrMAC = bluetooth.discover_devices()								# add parameter duration = secToScan if needed	
		print arrMAC

		#Get signal from server () 
		if(signal!=5):
			if(signal<0):
				signal*=(-1)
				GPIO.output(applianceGPIO[signal-1],GPIO.LOW)
				print applianceName [ applianceGPIO[signal-1]]," was switched off"
				#Update data at server
			else:
				GPIO.output(applianceGPIO[signal-1],GPIO.HIGH)
				print applianceName [ [signal-1]]," was switched on"
				#Update data at server
			signal=5 #Reset	

		if(len(arrMAC)==0):
			if(not roomIsEmpty):
				# print " * Nobody Home"
				countRoomEmpty+=1
			else:
				countRoomEmpty=0
		else:
			if(roomIsEmpty==1):
				print "Powering up"

				# print "Power up A/C & lights"
				for i in range(4):
					GPIO.output(applianceGPIO[i],GPIO.HIGH)
				#Update data on server

			roomIsEmpty=0

		# Power Down if no people for >= 4sec
		if(countRoomEmpty == 4):
			print "Powering Down"
			for i in range(4):
				GPIO.output(applianceGPIO[i],GPIO.LOW)

			countRoomEmpty = 0	
			roomIsEmpty = 1

		# If fire, stop to all devices and stop home automation MAYBE trigger siren
		if(tempSensor > 60.0):
			print "Fire! Run!"
			for i in range(4):
				GPIO.output(applianceGPIO[i],GPIO.LOW)
			break

		if(roomIsEmpty != 1):
			if (tempSensor < set_temp):
				ac_incriment = 1

			elif (tempSensor > set_temp):
				ac_incriment = -1

			if (nosPeople > len(arrMAC)+7): 		#More than 7 people entering should cause a sufficient change in room temperature because of body heat
				ac_incriment = ac_incriment - 1
			
			if (ac_temp > 17 and ac_temp < 46):
				ac_temp = ac_temp + ac_incriment
				tempSensor = tempSensor + ac_incriment

			print "Current Temp is: " + str(tempSensor)

			nosPeople = len(arrMAC)

		time.sleep(0.5)
		
	except:
		pass
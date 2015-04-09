import bluetooth
import os 
import time
import RPi.GPIO as GPIO
import requests
import serial

#AC/Heater range [18,45]

# BCM for GPIO pins
GPIO.setmode(GPIO.BCM)

# Set pins for usage
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

count=0 #Number of seconds for which room's empty
empty=0 #If room empty : 1,else :0
nppl=0 #Number of people in the room

appl=[18,23,24,25] #Assuming 4 appliances on 18,23,24,25 respectively
names={18:'Fridge',23:'Music Player',24:'Oven',25:'Laptop Charger'}
is_set=[0,0,0,0] #Tells whether appliance is ON or OFF

inside_temp=26
set_temp=25
ac_temp=25

ac_incriment=0

print "MAC Address                 Name"
while(1):
	try:
		ser = serial.Serial('/dev/ttyUSB0',  9600, timeout = 0.1) #timeout ?
		inside_temp=ser.readline() # :-?

		r=requests.get('http://localhost:3000/getdata')
		get_states# =?
		# os.system('clear')
		bluelist=bluetooth.discover_devices(duration=1,lookup_names=True)
		# print bluelist
		# print "count is ",count
		# for p in range(len(bluelist)):
			# print bluelist[p][0]+"           "+bluelist[p][1]

		#Get signal from server () 
		if(get_states!=is_set):
			for i in range(4):
				if(get_states[i]!=is_set):
					if(get_states[i]==0):
						GPIO.output(appl[i],GPIO.LOW)
					else:
						GPIO.output(appl[i],GPIO.HIGH)	


		if(len(bluelist)==0):
			if(not empty):
				# print " * Nobody Home"
				count+=1
			else:
				count=0
		else:
			if(empty==1):
				print "Powering up"

				# print "Power up A/C & lights"
				for i in range(4):
					GPIO.output(appl[i],GPIO.HIGH)
				#Update data on server
				empty=0

		if(count==10):
			print "Powering down"

			# print "Power down all appliances"
			for i in range(4):
				GPIO.output(appl[i],GPIO.LOW)

			#Update data on server
			count=0	
			empty=1

		if(inside_temp>60):
			print "Fire! Run!"

			# print "Emergency stop to all devices and stop home automation"
			for i in range(4):
				GPIO.output(appl[i],GPIO.LOW)
			#Send a distress signal to 101 ? 
			break

		if(empty!=1):
			if(inside_temp < set_temp):
				ac_incriment=1

			elif(inside_temp > set_temp):
				ac_incriment=-1

			if(nppl>len(bluelist)+7): #More than 7 people entering should cause a sufficient change in room temperature because of body-heat
				ac_incriment+=-1

			print ac_temp," changed by ",ac_incriment
			if(ac_temp>17 and ac_temp<46):
				ac_temp+=ac_incriment
				inside_temp+=ac_incriment
			print inside_temp," RT "
			nppl=len(bluelist)

		requests.post("http://localhost:3000/data",params={'tempInt':inside_temp)
		time.sleep(0.5)
	except:
		pass
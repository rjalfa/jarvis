import bluetooth
import os 
import time
import RPi.GPIO as GPIO

#For Arduino
import serial 
ser = serial.Serial('/dev/ttyACM0',  115200, timeout = 0.1) 

#Not too sure about this:

# def send(x):
#   ser.write(x)
#   while True:
#     try:
#       time.sleep(0.01)
#       break
#     except:
#       pass
#   time.sleep(0.1)

# reading=ser.readline()
# ser.write('3')

# Using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

# Set relay pins as output
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

count=0
empty=0
nppl=0

appl=[18,23,24,25] #Assuming 4 appliances on 18,23,24,25 respectively
names={'Fridge':18,'Television':23,'Laptop Charger':24,'Music System':25}

signal=5 #Contains the index of the appliance to be switched on/off (+ve means 'ON',-ve means 'OFF')
#Value 5 means no change to be done

inside_temp=26
set_temp=25
ac_temp=25

ac_incriment=0

print "MAC Address                 Name"
while(1):

	# os.system('clear')
	lol=bluetooth.discover_devices(duration=1,lookup_names=True)
	# print lol
	# print "count is ",count
	# for p in range(len(lol)):
		# print lol[p][0]+"           "+lol[p][1]

	#Get signal from server ()
	if(signal!=5):
		if(signal<0):
			signal*=(-1)
			GPIO.output(appl[signal],GPIO.LOW)
			print names[signal]," was switched off"
			#Send confirmation,maybe?
		else:
			GPIO.output(appl[signal],GPIO.HIGH)
			print names[signal]," was switched on"
			#Send confirmation,maybe?
		signal=5 #Reset	

	if(len(lol)==0):
		if(not empty):
			# print " * Nobody Home"
			count+=1
		else:
			count=0
	else:
		if(empty==1):
			print "Powering up"
			# print "Power up A/C & lights"
		empty=0

	if(count==10):
		print "Powering down"
		# print "Power down all appliances"
		count=0	
		empty=1

	if(inside_temp>60):
		print "Fire! Run!"
		# print "Emergency stop to all devices"
		break

	if(empty!=1):
		if(inside_temp < set_temp):
			ac_incriment=1

		elif(inside_temp > set_temp):
			ac_incriment=-1

		if(nppl>len(lol)+5): #More than 5 people entering should cause a sufficient change in room temperature because of body-heat
			ac_incriment+=-1

		print ac_temp," changed by ",ac_incriment
		if(ac_temp>18 and ac_temp<35):
			ac_temp+=ac_incriment
			inside_temp+=ac_incriment
		print inside_temp," RT "
		nppl=len(lol)


	time.sleep(0.5)
import time
import bluetooth
import requests
import subprocess

prevMac = set()
newMac = []
newName = []
while(1):
	try:
		# Get all registered MACs from server
		macServer = requests.get("http://1.1.1.4:3000/userData")._content.split(",")
		macServer = macServer[:len(macServer)-1]
		macServerSet = set(macServer)

		# Get all registered UserNames from server
		namesServer =  requests.get("http://1.1.1.4:3000/userName")._content.split(",")
		namesServer = namesServer[:len(namesServer)-1]

		# Scan bluetooth for available MACs
		macScan = bluetooth.discover_devices(lookup_names = False)
		# macScan = bluetooth.discover_devices(lookup_names = False, duration = 1)
		macScanSet = set(macScan)

		filteredPeople = macScanSet.intersection(macServerSet)

		for x in range(len(list(filteredPeople))):
			if (list(filteredPeople)[x] not in prevMac):
				newMac.append(list(filteredPeople)[x])

		for y in newMac:
			index = macServer.index(y)
			newName.append(namesServer[index])

		newName = list(set(newName))
		print "yoyoyoyoyoyoyooyoyoy"
		if (len(newName) == 1):
			subprocess.Popen(["pico2wave", "--lang=en-US", "--wave=/home/pi/Desktop/ied/jarvis/names.wav", "Hello" + str(newName[0])])
			subprocess.Popen(["mplayer", "names.wav"])
		elif (len(newName) > 1):
			subprocess.Popen(["pico2wave", "--lang=en-US", "--wave=/home/pi/Desktop/ied/jarvis/names.wav", "Hello People"])
			subprocess.Popen(["mplayer", "names.wav"])


		print "Total Registered: " + str(macServer)
		print "Total Registered: " + str(namesServer)
		print "Total Scanned   : " + str(macScan)
		print "Intersection    : " + str(filteredPeople)
		print "New Entries MAC : " + str(newMac)
		print "New Entries     : " + str(newName)
		print len(filteredPeople)

		requests.post("http://1.1.1.4:3000/nosPeople",params={'nosPeople':len(filteredPeople)})

		prevMac = filteredPeople
		newMac = []
		newName = []

	except:
		pass

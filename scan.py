import time
import bluetooth
import requests

while(1):
	try:
		macServer = requests.get("http://1.1.1.4:3000/userData")._content.split(",")
		macServer = macServer[:len(macServer)-1]
		macServer = set(macServer)

		namesServer =  requests.get("http://1.1.1.4:3000/userName")._content.split(",")
		namesServer = namesServer[:len(namesServer)-1]

		macScan = bluetooth.discover_devices(lookup_names = False, duration = 1)
		macScan = set(macScan)
		filteredPeople = macScan.intersection(macServer)

		print macServer
		print namesServer
		print filteredPeople
		print len(filteredPeople)
		requests.post("http://1.1.1.4:3000/nosPeople",params={'nosPeople':len(filteredPeople)})

	except:
		pass

import time
import bluetooth
import requests

temp=open('workspace.txt','w')
r = 0
while(1):
	try:
		rmac = requests.get("http://localhost:3000/userData")._content.split(",")
		rmac = rmac[:len(rmac)-1]
		rmac=set(rmac)
		arrMac = bluetooth.discover_devices(duration=1,lookup_names=False)
		arrMac=set(arrMac)
		valid_people=arrMac.intersection(rmac)
		r = len(valid_people)
		print "people: ",r
	except:
		pass
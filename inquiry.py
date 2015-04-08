# file: inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: performs a simple device inquiry followed by a remote name request of
#       each discovered device
# $Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
#

import bluetooth 
import requests
while True:
	print("performing inquiry...")

	nearby_devices = bluetooth.discover_devices(duration=1,lookup_names=True)
	s = ""
	print("found %d devices" % len(nearby_devices))

	for addr, name in nearby_devices:
    		s+=addr+","+name+"\n"

	requests.post("http://localhost:3000/", params= {'bmac':s})


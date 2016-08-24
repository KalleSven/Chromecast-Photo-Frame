from __future__ import print_function
import time
import pychromecast
import os
from glob import glob
import random
import shutil
import sys
import threading
import logging
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

PHOTOSBASEDIR = "/path/to/photos" #Root path where photos will be found.
PORT = 8088 #Port used to serve photos to the chromecast
IP = "192.168.X.X" #IP of server where photos are stored, likewise the server the script is running on
CASTDEVICE = "Livingroom" #The name of the cast device to serve.
TIMEDELAY = 10 #Number of seconds to display each photo


logging.basicConfig(level=logging.CRITICAL)
server = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
thread = threading.Thread(target = server.serve_forever)
thread.daemon = True

try:
    thread.start()
    print("BaseHTTPserver running")
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)


result = []
exclude = "@eaDir"
filetype = ".jpg"
for root, dirs, files in os.walk(PHOTOSBASEDIR):
	dirs[:] = [d for d in dirs if d not in exclude]
	for name in files:
		if filetype in name:
			result.append(os.path.join(root,name))

while True:
	print("Picking photo to cast")
	next = random.choice(result)  #Picks a photo at random
	synoPath = os.path.dirname(next)+"/@eaDir/"+os.path.basename(next)+"/SYNOPHOTO_THUMB_XL.jpg" #Findes the corresponding Photo Station generated thumbnail
	if os.path.isfile(synoPath):
		src = synoPath
	else: 
		src = next #If no Photo Station thumbnail is found, fall back on the original photo picked
	
	if not os.path.exists("media"):
	    os.makedirs("media")
	shutil.copy(src,"media/media.jpg")

	try:
		print("Trying to connect to Chromecast")
		cast = pychromecast.get_chromecast(friendly_name=CASTDEVICE) #Connecting to Chromecast device
		cast.wait() 		# Wait for cast device to be ready
		print("Connected to Chromecast")
	
		if cast.status.display_name=="Backdrop" or cast.status.display_name=="Default Media Receiver" or cast.status.display_name==None: #Only try to cast photo if no other media playing
			print("Casting photo")
			mc = cast.media_controller
			mc.play_media("http://"+IP+":"+str(PORT)+"/media/media.jpg?time="+str(time.time()), "image/jpg")
		time.sleep(TIMEDELAY) #Number of seconds to delay before casting next photo
		cast.disconnect()	
	except:
		print("Could not play photo")
	


import RPi.GPIO as gp
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread

# Author Jordan May
# x15515673
# Code used to activate the pump -> https://www.youtube.com/watch?v=My1BDB1ei0E&t=239s
# For hooking up the wiring, i used this -> https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc
# # Firebase code : https://firebase.google.com/docs/reference/admin/python/firebase_admin
# Class for controlling the pump


# Set up Firebase
def set_up_firebase():
	try:
		fb_credentials = credentials.Certificate('smartplant-2fc4c-firebase-adminsdk-gjnsf-78fd7405b8.json')
		firebase_admin.initialize_app(fb_credentials, {'databaseURL' : 'https://smartplant-2fc4c.firebaseio.com/'})
		print("Success")
	except IOError as e:
		print("Something went wrong" + e)

# start listener
def listener():
	firebase_admin.db.reference('/').listen(listener_fb)

# listener inner
def listener_fb(event):
	# Make a reference to our state node
	pump_value_state = db.reference('Pump/Information/state')
	pump_timer = db.reference('Pump/Information/rateLimit')

	pump_timer = int(pump_timer.get())
	# now if it is on then we turn the pump on
	if pump_timer > 1:
		# If the pump timer is more than one we know we have a value. Check if it is on
		if pump_value_state.get() == "on":
			print("yes")
			activatePump(pump_timer)
		else:
			print("no")
	else:
		print("no")

# Activate Pump
def activatePump(rateLimit):
	time_integer = int(rateLimit)

	print("Turning on the pump at rate limit ", rateLimit)
	time.sleep(rateLimit)

	print("Turning off pump now!")

	print("Turning state to off")

	root_node = db.reference()
	state_pump = root_node.child("Pump/Information/").update({'state' : "off"})
	# Turn the relay on, allowing flow
	gp.setmode(gp.BOARD)
	gp.setup(7, gp.OUT)
	gp.output(7, gp.LOW)
	# # Allow flow until rateLimit
	time.sleep(rateLimit)
	# # Turn relay off
	gp.output(7, gp.HIGH)

	# # cleanup
	gp.cleanup()

set_up_firebase()
listen_for_config_details = Thread(target = listener())
listen_for_config_details.start()

# import RPi.GPIO as gp
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread

# Author Jordan May
# x15515673
# Class for controlling the pump

# Variables set up
# gp.setmode(gp.BOARD)
# gp.setup(7, gp.OUT)

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
	# now if it is on then we turn the pump on
	if pump_timer.get() > 1:
		# If the pump timer is more than one we know we have a value. Check if it is on
		if pump_value_state.get() == "on":
			print("yes")
			activatePump(pump_timer.get())
		else:
			print("no")
	else:
		print("no")


# Activate Pump
def activatePump(rateLimit):

	print("Turning on the pump at rate limit ", rateLimit)
	time.sleep(rateLimit)

	print("Turning off pump now!")

	print("Turning state to off")
	
	root_node = db.reference()
	state_pump = root_node.child("Pump/Information/").update({'state' : "off"})
	# Turn the relay on, allowing flow
	# gp.output(7, gp.LOW)
	# # Allow flow until rateLimit
	# time.sleep(rateLimit)
	# # Turn relay off
	# gp.output(7, gp.HIGH)
	# # Log timestamp into Firebase

	# # cleanup 
	# gp.cleanup()

set_up_firebase()
listen_for_config_details = Thread(target = listener())
listen_for_config_details.start()



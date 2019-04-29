# import grovepi
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread
import random
import time
import datetime


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
	firebase_admin.db.reference('LCD/Information/message').listen(listener_fb)

# management
def listener_fb(event):
	# Check if the user has pressed a button for which state they want
	lcd_state_which = db.reference('LCD/Information/message')
	lcd_date = db.reference('LCD/Information/date')
	
	lcd_date_converted = float(lcd_date.get())
	last_watered_time = datetime.datetime.fromtimestamp(lcd_date_converted/1000.0)

	if(lcd_state_which.get() == "last watered"):
		# if the message says "Last Watered" trigger the method
		lcd_change_time_last_watered(last_watered_time)

	elif(lcd_state_which.get() == "temperature"):
		# if they want the current temperature
		current_temperature = db.reference('Temperature/Information/message')
		current_temperature_converted = int(current_temperature.get())

		current_temperature_method(current_temperature_converted)


# This changes the text on the lcd screen to the time of last watered
def lcd_change_time_last_watered(last_watered):
	print("Last Watered")

# This changes the text on the lcd screen to the current temperature
def current_temperature_method():
	print("Current temperature")

set_up_firebase()
listen_for_config_details = Thread(target = listener())
listen_for_config_details.start()
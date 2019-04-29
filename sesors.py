# import grovepi
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread
import random
import time

humidityState = False
temperatureState = False
# Set up Firebase
try:
	fb_credentials = credentials.Certificate('smartplant-2fc4c-firebase-adminsdk-gjnsf-78fd7405b8.json')
	firebase_admin.initialize_app(fb_credentials, {'databaseURL' : 'https://smartplant-2fc4c.firebaseio.com/'})
	print("Success")
	global node 
	# root 
	node = db.reference()
except IOError as e:
	print("Something went wrong" + e)

# start listener
def listener():
	firebase_admin.db.reference('/').listen(listener_fb)


# listener for firebase events
def listener_fb(event):
	
	# Make a reference to our state 
	# Temperature 
	temperature_state = db.reference('Temperature/Information/state')
	temperature_value = db.reference('Temperature/Information/message')
	temperature_timer = db.reference('Temperature/Information/rateLimit')

	# Humidity
	humidity_state = db.reference('Humidity/Information/state')
	humidity_value = db.reference('Humidity/Information/message')
	humidity_timer = db.reference('Humidity/Information/rateLimit')

	# Soil
	soil_state = db.reference('Soil/Information/state')
	soil_value = db.reference('Soil/Information/message')
	soil_timer = db.reference('Soil/Information/rateLimit')

	# Light
	light_state = db.reference('Light/Information/state')
	light_value = db.reference('Light/Information/message')
	light_timer = db.reference('Light/Information/rateLimit')

	# Check for our temperature
	if temperature_state.get() == "ON":
		print("Temperature is on")
		# Define global state
		# Turn this on]
		global temperatureState
		temperatureState = True
		try:
			# Start publish thread for temperature
			temperature_publishing = Thread(target = temperature_publish_firebase)
			# if the thread hasnt being started then start
			if not temperature_publishing.isAlive():
				temperature_publishing.start()
				print("Startinng temperature thread")
		except Exception as e:
			pass

	else:
		print("Temperature is off")
		temperatureState = False

	# Check for our humidity 
	if humidity_state.get() == "ON":
		print("Humidity is on")
		# global state
		global humidityState
		humidityState = True
		try:
			# start thread for humidity
			humidity_publishing = Thread(target = humidity_publish_firebase)
			# if not started already
			if not humidity_publishing.isAlive():
				print("Starting humidity thread")
				humidity_publishing.start()
		except Exception as e:
			pass
	else:
		humidityState = False
		print("Humidity is turning off")

	# Check for our Light
	if light_state.get() == "ON":
		print("Humidity is on")
		# globals
		global lightState
		lightState = True
		try:
			# start thread
			light_thread = Thread(target = light_publish_firebase)
			if not light_thread.isAlive():
				print("Starting up light thread")
				light_thread.start()
		except Exception as e:
			pass
	else:
		lightState = False

	# Check for soil
	if soil_state.get() == "ON":
		print("Soil is turning on")
		global soilState
		soilState = True

		try: 
			# start thread
			soil_thread = Thread(target = soil_publish_firebase)
			if not soil_thread.isAlive():
				print("Starting up the soil thread")
				soil_thread.start()
		except Exception as e:
			pass
	else:
		soilState = False
		

# PUBLISHING TO FIREBASE THE VALUES
# Publishing temperature
def temperature_publish_firebase():
	# get state of sensor atm
	rate = db.reference('Temperature/Information/rateLimit')
	rates = int(rate.get())

	# As long as our temperature state is on, keep on reading from our sensors for temperature
	while temperatureState:
		temp = temperature_sensor(rates)
		print(temp)
		temp1 = str(temp)
		update_fb = node.child("Temperature/Information/").update({'message' : temp})

# Publishing humidity
def humidity_publish_firebase():
	# get state of sensor atm
	rate = db.reference('Humidity/Information/rateLimit')
	rates = int(rate.get())

	# as long as our temperature state is on, keep reasding from our sensors
	while humidityState:
		hum = humidity_sensor(rates)
		temp1 = str(hum)
		update_fb = node.child("Humidity/Information/").update({'message' : hum})

# Publishing Light Sensor
def light_publish_firebase():
	rate = db.reference('Light/Information/rateLimit')
	rates = int(rate.get())

	while lightState:
		light = light_sensor(rates)
		temp1 = str(light)
		update_fb = node.child("Light/Information/").update({'message' : light})

# Publishing Soil Sensor
def soil_publish_firebase():
	rate = db.reference('Soil/Information/rateLimit')
	rates = int(rate.get())

	while soilState:
		soil = soil_sensor(rates)
		temp1 = str(soil)
		update_fb = node.child("Soil/Information/").update({'message' : soil})

# SINGLE GETTER CALLS TO OUR SENSORS
# Temperature Sensor
def temperature_sensor(rateLimit):
	time.sleep(rateLimit)
	ran = random.randint(1,20)
	return ran

# Humidity
def humidity_sensor(rateLimit):
	time.sleep(rateLimit)
	ran = random.randint(1,20)
	return ran

# Light
def light_sensor(rateLimit):
	time.sleep(rateLimit)
	ran = random.randint(1,20)
	return ran

# Soil
def soil_sensor(rateLimit):
	time.sleep(rateLimit)
	ran = random.randint(1,20)
	return ran


listener_thread = Thread(target = listener(), args=(temperature_publish_firebase,))
listener_thread.start()
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

set_up_firebase()
# management
# Check if the user has pressed a button for which state they want
lcd_date = db.reference('Temperature/Information/date')
print(lcd_date)
d = float(lcd_date.get())
last_watered_time = datetime.datetime.fromtimestamp(d/1000.0)

print(last_watered_time)


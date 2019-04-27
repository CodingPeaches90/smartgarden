import RPi.GPIO as gp
import time
import firebase_admin

gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)

time.sleep(1)
gp.output(7, gp.LOW)

time.sleep(1)

gp.output(7, gp.HIGH)

time.sleep(1)

gp.cleanup()

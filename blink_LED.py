import RPi.GPIO as GPIO
import time
# blinking function
def blink (pin) :
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
    return
# to use Rasburry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
# set up GPIO output channel
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.output(17,GPIO.HIGH)
GPIO.output(4,GPIO.HIGH)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
time.sleep(20)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10,GPIO.HIGH)

for i in range (0,50):
   blink(10)
   
GPIO.cleanup()

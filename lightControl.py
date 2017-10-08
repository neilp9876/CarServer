#!/usr/bin/python

from PWM.Adafruit_PWM_Servo_Driver import PWM
import time
import threading


# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 4000  # Max pulse length out of 4096
lightMax = 4000

HEADLIGHT = 4
SPOTLIGHT = 5
REVERSE_LIGHT = 6
LEFT_INDICATOR = 7

RIGHT_INDICATOR = 8
FOGLIGHT = 9
TAILLIGHT = 10
BRAKELIGHT = 11

GEAR_SERVO = 10
THROTTLE_SERVO = 12
STEERING_SERVO = 13 # Need another pin!!!

HAZARDS = 99

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def Initialise():
    pwm.setPWMFreq(5000)                        # Set frequency to 60 Hz
    for x in range(0, 15):
        pwm.setPWM(x, 0, 0)
    
def TurnLightsOn(led):
    intensity = 0
    while (intensity < lightMax):
        intensity = intensity + 10
        pwm.setPWM(led, 0, intensity)

def TurnLightsOff(led):
    intensity = lightMax
    while (intensity > 0):
        intensity = intensity - 10
        pwm.setPWM(led, 0, intensity)

def TurnLightsOnImmediate(led):
    pwm.setPWM(led, 0, lightMax)

def TurnLightsOffImmediate(led):
    pwm.setPWM(led, 0, 0)

ledRunning = []
ledStopEvent = []

def LightFlashing(led):
    if led in ledRunning:
        return True
    else:
        return False

def StopFlashing(led):
    index = ledRunning.index(led)
    ledRunning.pop(index)
    return ledStopEvent.pop(index)

def FlashLightsOn(led):
    if LightFlashing(led) == False:
        print "Starting flash on %d" % led
       
        # Create stop event
        stopFlag = threading.Event()

        # Record the details
        ledRunning.append(led)
        ledStopEvent.append(stopFlag)

        # Start the new flashing thread
        thread = FlashingThread(stopFlag, led)
        thread.start()
    else:
        print "Already flashing %d, ignoring" % led
        
def FlashLightsOff(led):
    if LightFlashing(led) == True:
        print "Stopping flash on %d" % led
        event = StopFlashing(led)
        event.set()
    else:
        print "Not flashing on %d, ignoring" % led

class FlashingThread(threading.Thread):
    def __init__(self, event, led):
        threading.Thread.__init__(self)
        self.stopped = event
        self.led = led

    def run(self):
        lightOn = 0
        while not self.stopped.wait(0.5):
            if lightOn == 0:
                #print "Lights On"
                if self.led == HAZARDS:
                    TurnLightsOnImmediate(LEFT_INDICATOR)
                    TurnLightsOnImmediate(RIGHT_INDICATOR)
                else:
                    TurnLightsOn(self.led)
                lightOn = 1
            else:
                #print "Lights Off"
                if self.led == HAZARDS:
                    TurnLightsOffImmediate(LEFT_INDICATOR)
                    TurnLightsOffImmediate(RIGHT_INDICATOR)
                else:
                    TurnLightsOff(self.led)
                lightOn = 0
            
      


"""
while (True):
  print "lights on"
  TurnLightsOn(4)
  TurnLightsOn(5)
  TurnLightsOn(7)
  time.sleep(5)
  print "lights off"
  TurnLightsOff(4)
  TurnLightsOff(5)
  TurnLightsOff(7)
  time.sleep(5)
"""

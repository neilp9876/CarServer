#!/usr/bin/python

from PWM.Adafruit_PWM_Servo_Driver import PWM
import time
import threading


# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

#servoMin = 150  # Min pulse length out of 4096
#servoMax = 4000  # Max pulse length out of 4096
lightMax = 4000

HEADLIGHT = 4
SPOTLIGHT = 5
REVERSE_LIGHT = 6
LEFT_INDICATOR = 7

RIGHT_INDICATOR = 8
FOGLIGHT = 9
TAILLIGHT = 10
BRAKELIGHT = 11

GEAR_SERVO = 12
THROTTLE_SERVO = 14
STEERING_SERVO = 13
TEST_SERVO = 15

HAZARDS = 99

GEAR_1 = 170
GEAR_2 = 220
GEAR_3 = 400

CENTER = 5  # Direction is based on a range of 1 to 9. 5 is centre
currentDirection = 190.0

SERVO_MIN = 460  # Min pulse length, us (tick 184/4096)
SERVO_MAX = 2100  # Max pulse length, us  (tick 430/4096)
SERVO_MID = SERVO_MAX - ((SERVO_MAX - SERVO_MIN)/2) # Midpoint pulse length, us
FREQUENCY = 50 # cycle length, Hz

pulseLength = 1000000 / FREQUENCY
tick = pulseLength / 4096 # 12 bit resolution

# we need to convert us pulses to 12 bit ticks
def setServoPulse(channel, pulse):
  print "%d pulse, %d tick" % (pulse, tick)
  pwm.setPWM(channel, 0, pulse/tick)

#pwm.setPWMFreq(cycle) # Set frequency

#while (True):
  # cycle servo
#  print "%d pulse" % pulse
#  setServoPulse(TEST_SERVO, pulse)
#  time.sleep(1)
#  pulse += 20
#  setServoPulse(TEST_SERVO, servoMin)
#  time.sleep(1)
#  setServoPulse(TEST_SERVO, servoMid)
#  time.sleep(1)
#  setServoPulse(TEST_SERVO, servoMax)
#  time.sleep(1)


#def setServoPulse(channel, pulse):
#  pulseLength = 1000000                   # 1,000,000 us per second
#  pulseLength /= 50                       # 50 Hz
#  print "%d us per period" % pulseLength
#  pulseLength /= 4096                     # 12 bits of resolution - 1 tick
#  print "%d us per bit" % pulseLength
#  pulse *= 1000
#  pulse /= pulseLength
#  pwm.setPWM(channel, 0, pulse)

def Initialise():
    currentDirection = 190
    pwm.setPWMFreq(FREQUENCY)

    for x in range(0, 11):
        pwm.setPWM(x, 0, 0)
        
    ChangeGear(1)
    Steer(CENTER)
    
def TurnLightsOn(led):
    TurnLightsOnImmediate(led)
#    intensity = 0
#    while (intensity < lightMax):
#        intensity = intensity + 10
#        pwm.setPWM(led, 0, intensity)

def TurnLightsOff(led):
    TurnLightsOffImmediate(led)
#    intensity = lightMax
#    while (intensity > 0):
#        intensity = intensity - 10
#        pwm.setPWM(led, 0, intensity)

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
        TurnLightsOffImmediate(LEFT_INDICATOR)
        TurnLightsOffImmediate(RIGHT_INDICATOR)        
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
                    TurnLightsOnImmediate(self.led)
                lightOn = 1
            else:
                #print "Lights Off"
                if self.led == HAZARDS:
                    TurnLightsOffImmediate(LEFT_INDICATOR)
                    TurnLightsOffImmediate(RIGHT_INDICATOR)
                else:
                    TurnLightsOffImmediate(self.led)
                lightOn = 0
            
def ChangeGear(gearPos):
    if gearPos == 1:
      setServoPulse(TEST_SERVO, SERVO_MIN)
#      pwm.setPWM(GEAR_SERVO, 0, 120)
    elif gearPos == 2:
      setServoPulse(TEST_SERVO, SERVO_MID)
#      pwm.setPWM(GEAR_SERVO, 0, 200)
    elif gearPos == 3:
      setServoPulse(TEST_SERVO, SERVO_MAX)
#      pwm.setPWM(GEAR_SERVO, 0, 280)

def Steer(direction):
  global currentDirection

  # direction is range between 1 to 9
  
  if direction == CENTER:
    currentDirection = SERVO_MID
  else:
    # calculate iteration amount
    iteration = (SERVO_MAX - SERVO_MIN) / 8.0
    
    currentDirection = (iteration * (direction - 1.0)) + SERVO_MIN

    # Check limits
    if currentDirection < SERVO_MIN:
      currentDirection = SERVO_MIN
    elif currentDirection > SERVO_MAX:
      currentDirection = SERVO_MAX

  # Set the servo
  print "Direction = %d" % currentDirection
  setServoPulse(STEERING_SERVO, int(currentDirection))
#  pwm.setPWM(STEERING_SERVO, 0, int(currentDirection))
    
  
    
    

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

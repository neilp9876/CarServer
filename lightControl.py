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

STEERING_SERVO = 12
GEAR_SERVO = 13
THROTTLE_SERVO = 14
TEST_SERVO = 14

HAZARDS = 99

GEAR_3 = 1170
GEAR_1 = 1550
GEAR_2 = GEAR_3 - ((GEAR_3 - GEAR_1)/2)

THROTTLE_REV_MAX = 770
THROTTLE_OFF = 900
CRAWL = 1180
THROTTLE_MAX = 2150

STEERING_MIN = 460  # Min pulse length, us (tick 184/4096)
STEERING_MAX = 2100  # Max pulse length, us  (tick 430/4096)
STEERING_MID = STEERING_MAX - ((STEERING_MAX - STEERING_MIN)/2) # Midpoint pulse length, us
FREQUENCY = 50 # cycle length, Hz
CENTER = 5  # Direction is based on a range of 1 to 9. 5 is centre
currentDirection = STEERING_MID

pulseLength = 1000000 / FREQUENCY
tick = pulseLength / 4096 # 12 bit resolution

# we need to convert us pulses to 12 bit ticks
def setServoPulse(channel, pulse):
  print "%d pulse, %d tick" % (pulse, tick)
  pwm.setPWM(channel, 0, pulse/tick)

#pwm.setPWMFreq(FREQUENCY) # Set frequency

#pulse = THROTTLE_OFF
#while (True):
  # cycle servo
#  print "%d pulse" % pulse
#  setServoPulse(TEST_SERVO, pulse)
#  time.sleep(1)
#  pulse -= 10
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
    Throttle(0)
    
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
      setServoPulse(GEAR_SERVO, GEAR_1)
    elif gearPos == 2:
      setServoPulse(GEAR_SERVO, GEAR_2)
    elif gearPos == 3:
      setServoPulse(GEAR_SERVO, GEAR_3)

def Steer(direction):
  global currentDirection

  # direction is range between 1 to 9
  
  if direction == CENTER:
    currentDirection = STEERING_MID
  else:
    # calculate iteration amount
    iteration = (STEERING_MAX - STEERING_MIN) / 8.0
    
    currentDirection = (iteration * (direction - 1.0)) + STEERING_MIN

    # Check limits
    if currentDirection < STEERING_MIN:
      currentDirection = STEERING_MIN
    elif currentDirection > STEERING_MAX:
      currentDirection = STEERING_MAX

  # Set the servo
  print "Direction = %d" % currentDirection
  setServoPulse(STEERING_SERVO, int(currentDirection))
    
  
def Throttle(position):
  throttle = THROTTLE_OFF
  if position > 0:
    iteration = (THROTTLE_MAX - THROTTLE_OFF) / 8.0
    throttle = (iteration * (position - 1.0)) + THROTTLE_OFF

    # Check limits
    if throttle < THROTTLE_OFF:
      throttle = THROTTLE_OFF
    elif throttle > THROTTLE_MAX:
      throttle = THROTTLE_MAX

  elif position < 0:
    iteration = (THROTTLE_OFF - THROTTLE_REV_MAX) / 4.0
    throttle = THROTTLE_OFF - (iteration * ((position * -1) - 1.0))

    # Check Limits
    if throttle > THROTTLE_OFF:
      throttle = THROTTLE_OFF
    elif throttle < THROTTLE_REV_MAX:
      throttle = THROTTLE_REV_MAX
    
  # Set Servo
  print "Throttle = %d" % throttle
  setServoPulse(THROTTLE_SERVO, int(throttle))
    


#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 4000  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  #print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  #print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  print "%d PULSE" % pulse
  print "%d Pulse length" % pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(5)                        # Set frequency to 60 Hz
servoPos = 50

while (True):
  # Change speed of continuous servo on channel O
#  setServoPulse(15, servoPos)
  servoPos = 50
  pwm.setPWM(15, 0, servoPos)
  time.sleep(1)
  servoPos = servoPos = 190
  pwm.setPWM(15, 0, servoPos)
  time.sleep(1)
  servoPos = 330
  pwm.setPWM(15, 0, servoPos)
  time.sleep(1)
  
  print "Position = " + str(servoPos)
  #pwm.setPWM(15, 0, servoMax)
  #time.sleep(1)

while (servoPos > 50):
  # Change speed of continuous servo on channel O
  setServoPulse(15, servoPos)
#  pwm.setPWM(15, 0, servoPos)
  time.sleep(1)
  servoPos = servoPos - 10
  print "Position = " + str(servoPos)




